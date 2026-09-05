import { createClient } from "@supabase/supabase-js";

const url = import.meta.env.VITE_SUPABASE_URL;
const publishableKey = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY;

export const supabase = url && publishableKey ? createClient(url, publishableKey) : null;

export async function sendMagicLink(email: string): Promise<void> {
  if (!supabase) throw new Error("Supabase authentication is not configured.");
  const { error } = await supabase.auth.signInWithOtp({
    email,
    options: { emailRedirectTo: window.location.origin }
  });
  if (error) throw error;
}

export async function persistCurrentAccessToken(): Promise<void> {
  if (!supabase) return;
  const { data } = await supabase.auth.getSession();
  if (data.session?.access_token) window.localStorage.setItem("kids.access_token", data.session.access_token);
}
