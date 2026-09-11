import { describe, expect, it } from "vitest";
import { initialAdminMfaState, reduceAdminMfaState } from "./adminMfaState";

describe("administrative MFA state", () => {
  it("keeps a sensitive-action challenge open across identity and token refreshes", () => {
    const challenged = reduceAdminMfaState(initialAdminMfaState, { type: "sensitive-action-required" });
    const identityReloaded = reduceAdminMfaState(challenged, { type: "identity-loaded", hasAal2: true });
    const tokenRefreshed = reduceAdminMfaState(identityReloaded, { type: "identity-loaded", hasAal2: true });

    expect(tokenRefreshed).toEqual({ required: true, forced: true });
  });

  it("closes a forced challenge only after verification", () => {
    const challenged = reduceAdminMfaState(initialAdminMfaState, { type: "sensitive-action-required" });
    const verified = reduceAdminMfaState(challenged, { type: "verified" });

    expect(verified).toEqual(initialAdminMfaState);
    expect(reduceAdminMfaState(verified, { type: "identity-loaded", hasAal2: true })).toEqual(initialAdminMfaState);
  });

  it("still requires the normal login challenge when the session is only AAL1", () => {
    expect(reduceAdminMfaState(initialAdminMfaState, { type: "identity-loaded", hasAal2: false }))
      .toEqual({ required: true, forced: false });
  });
});
