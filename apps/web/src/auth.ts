import { createClient } from "@supabase/supabase-js";

const url = import.meta.env.VITE_SUPABASE_URL;
const publishableKey = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY;
const apiUrl = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export const supabase = url && publishableKey ? createClient(url, publishableKey) : null;

/**
 * Supabase currently warns that starting another async client call directly
 * inside `onAuthStateChange` can deadlock the auth client's internal lock.
 * Move follow-up work onto the next task so the auth callback can finish first.
 */
export function deferAuthStateWork(work: () => void | Promise<void>): number {
  return window.setTimeout(() => { void work(); }, 0);
}

export async function sendMagicLink(email: string, redirectTo = `${window.location.origin}${window.location.pathname}`): Promise<void> {
  if (!supabase) throw new Error("Supabase authentication is not configured.");
  const { error } = await supabase.auth.signInWithOtp({
    email,
    options: { emailRedirectTo: redirectTo, shouldCreateUser: false }
  });
  if (error) throw error;
}

export type AdminMfaSetup = { factorId: string; existing: boolean; qrCode?: string; secret?: string };

export async function prepareAdminMfa(forceChallenge = false): Promise<AdminMfaSetup | null> {
  if (!supabase) throw new Error("Supabase authentication is not configured.");
  const assurance = await supabase.auth.mfa.getAuthenticatorAssuranceLevel();
  if (assurance.error) throw assurance.error;
  if (assurance.data.currentLevel === "aal2" && !forceChallenge) return null;
  const listed = await supabase.auth.mfa.listFactors();
  if (listed.error) throw listed.error;
  const verified = listed.data.totp.find((factor) => factor.status === "verified");
  if (verified) return { factorId: verified.id, existing: true };
  const enrolled = await supabase.auth.mfa.enroll({ factorType: "totp", friendlyName: "Kids Learning admin" });
  if (enrolled.error) throw enrolled.error;
  return { factorId: enrolled.data.id, existing: false, qrCode: enrolled.data.totp.qr_code, secret: enrolled.data.totp.secret };
}

export async function verifyAdminMfa(factorId: string, code: string, forceChallenge = false): Promise<void> {
  if (!supabase) throw new Error("Supabase authentication is not configured.");
  if (!forceChallenge) {
    const result = await supabase.auth.mfa.challengeAndVerify({ factorId, code });
    if (result.error) throw result.error;
    await persistCurrentAccessToken();
    return;
  }

  const current = await supabase.auth.getSession();
  if (current.error || !current.data.session) throw current.error ?? new Error("Administrative session is unavailable.");
  const response = await fetch(`${apiUrl}/v1/admin/mfa/reauthenticate`, {
    method: "POST",
    cache: "no-store",
    headers: { "Authorization": `Bearer ${current.data.session.access_token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ factorId, code })
  });
  if (!response.ok) {
    const body = await response.text();
    throw new Error(response.status === 422 ? "El código expiró o no es válido." : body || "No pudimos verificar MFA.");
  }
  const session = await response.json() as { accessToken: string; refreshToken: string };
  const updated = await supabase.auth.setSession({ access_token: session.accessToken, refresh_token: session.refreshToken });
  if (updated.error) throw updated.error;
  await persistCurrentAccessToken();
}

export async function signOut(): Promise<void> {
  if (supabase) await supabase.auth.signOut();
  window.localStorage.removeItem("kids.access_token");
  window.localStorage.removeItem("kids.family_id");
}

export async function requestReauthentication(): Promise<void> {
  if (!supabase) throw new Error("Supabase authentication is not configured.");
  const current = await supabase.auth.getUser();
  if (current.error || !current.data.user.email) throw current.error ?? new Error("No adult email is available for reauthentication.");
  const result = await supabase.auth.signInWithOtp({
    email: current.data.user.email,
    options: { emailRedirectTo: `${window.location.origin}/?reauth=privacy`, shouldCreateUser: false }
  });
  if (result.error) throw result.error;
}

export async function persistCurrentAccessToken(): Promise<void> {
  if (!supabase) return;
  const { data } = await supabase.auth.getSession();
  if (data.session?.access_token) window.localStorage.setItem("kids.access_token", data.session.access_token);
}
