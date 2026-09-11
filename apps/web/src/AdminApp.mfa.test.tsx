import { act, cleanup, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

const authMocks = vi.hoisted(() => ({
  listener: undefined as undefined | ((event: string, session: { access_token: string } | null) => void),
  loadIdentity: vi.fn(),
  loadData: vi.fn(),
}));

vi.mock("./api", async () => {
  const actual = await vi.importActual<typeof import("./api")>("./api");
  return {
    ...actual,
    DEMO_MODE: false,
    cancelAdminMfaRequests: vi.fn(),
    resumeAdminMfaRequests: vi.fn(),
  };
});

vi.mock("./auth", () => ({
  supabase: {
    auth: {
      getSession: vi.fn(async () => ({ data: { session: { access_token: "signed-test-token" } }, error: null })),
      onAuthStateChange: vi.fn((listener: typeof authMocks.listener) => {
        authMocks.listener = listener;
        return { data: { subscription: { unsubscribe: vi.fn() } } };
      }),
    },
  },
  deferAuthStateWork: (work: () => void | Promise<void>) => {
    void work();
    return 0;
  },
  prepareAdminMfa: vi.fn(async () => ({ factorId: "factor-test", existing: true })),
  signOut: vi.fn(async () => undefined),
  verifyAdminMfa: vi.fn(async () => undefined),
}));

vi.mock("./adminData", async () => {
  const actual = await vi.importActual<typeof import("./adminData")>("./adminData");
  authMocks.loadIdentity.mockResolvedValue({
    userId: "00000000-0000-0000-0000-000000000001",
    roles: ["platform_owner"],
    mfa: true,
  });
  authMocks.loadData.mockImplementation(async () => structuredClone(actual.demoAdminData));
  return {
    ...actual,
    loadAdminIdentity: authMocks.loadIdentity,
    loadAdminData: authMocks.loadData,
  };
});

import AdminApp from "./AdminApp";

afterEach(() => {
  cleanup();
  authMocks.listener = undefined;
  authMocks.loadIdentity.mockClear();
  authMocks.loadData.mockClear();
  localStorage.clear();
});

describe("administrative sensitive-action MFA", () => {
  it("does not let a Supabase session event dismiss the pending TOTP overlay", async () => {
    render(<AdminApp />);
    expect(await screen.findByRole("heading", { name: "Resumen" })).toBeTruthy();

    act(() => window.dispatchEvent(new Event("kids:mfa-required")));
    expect(await screen.findByRole("heading", { name: "Verificación en dos pasos" })).toBeTruthy();
    const identityCallsBeforeRefresh = authMocks.loadIdentity.mock.calls.length;

    act(() => authMocks.listener?.("TOKEN_REFRESHED", { access_token: "refreshed-test-token" }));
    await waitFor(() => expect(authMocks.loadIdentity.mock.calls.length).toBeGreaterThan(identityCallsBeforeRefresh));

    expect(screen.getByRole("heading", { name: "Verificación en dos pasos" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "Autorizar y continuar" })).toBeTruthy();
  });
});
