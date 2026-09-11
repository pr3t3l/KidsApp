export type AdminMfaState = {
  required: boolean;
  forced: boolean;
};

export type AdminMfaAction =
  | { type: "identity-loaded"; hasAal2: boolean }
  | { type: "sensitive-action-required" }
  | { type: "verified" }
  | { type: "signed-out" };

export const initialAdminMfaState: AdminMfaState = {
  required: false,
  forced: false,
};

/**
 * Keeps a sensitive-action challenge open across Supabase auth events.
 *
 * Supabase can emit SIGNED_IN or TOKEN_REFRESHED while a TOTP overlay is
 * visible. Those events reload the user's identity as AAL2, but they are not
 * proof that the new step-up challenge was completed. Only `verified` or
 * `signed-out` may clear a forced challenge.
 */
export function reduceAdminMfaState(state: AdminMfaState, action: AdminMfaAction): AdminMfaState {
  switch (action.type) {
    case "sensitive-action-required":
      return { required: true, forced: true };
    case "verified":
    case "signed-out":
      return initialAdminMfaState;
    case "identity-loaded":
      if (state.forced) return state;
      return { required: !action.hasAal2, forced: false };
  }
}
