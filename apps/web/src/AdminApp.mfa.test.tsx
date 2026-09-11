import { act, cleanup, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const authMocks = vi.hoisted(() => ({
  listener: undefined as undefined | ((event: string, session: { access_token: string } | null) => void),
  session: { access_token: "signed-test-token" } as { access_token: string } | null,
  getSession: vi.fn(),
  loadIdentity: vi.fn(),
  loadData: vi.fn(),
}));

vi.mock("./api", async () => {
  const actual = await vi.importActual<typeof import("./api")>("./api");
  return {
    ...actual,
    DEMO_MODE: false,
  };
});

vi.mock("./auth", () => ({
  supabase: {
    auth: {
      getSession: authMocks.getSession,
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

beforeEach(() => {
  authMocks.getSession.mockImplementation(async () => ({ data: { session: authMocks.session }, error: null }));
});

afterEach(() => {
  cleanup();
  authMocks.listener = undefined;
  authMocks.loadIdentity.mockClear();
  authMocks.loadData.mockClear();
  authMocks.getSession.mockReset();
  authMocks.session = { access_token: "signed-test-token" };
  localStorage.clear();
});

describe("administrative session initialization", () => {
  it("updates refreshed credentials without reloading an already-open workspace", async () => {
    render(<AdminApp />);
    expect(await screen.findByRole("heading", { name: "Resumen" })).toBeTruthy();
    const identityCalls = authMocks.loadIdentity.mock.calls.length;
    const dataCalls = authMocks.loadData.mock.calls.length;

    await act(async () => authMocks.listener?.("TOKEN_REFRESHED", { access_token: "refreshed-test-token" }));
    await act(async () => authMocks.listener?.("SIGNED_IN", { access_token: "refreshed-test-token" }));

    expect(localStorage.getItem("kids.access_token")).toBe("refreshed-test-token");
    expect(authMocks.loadIdentity).toHaveBeenCalledTimes(identityCalls);
    expect(authMocks.loadData).toHaveBeenCalledTimes(dataCalls);
    expect(screen.getByRole("heading", { name: "Resumen" })).toBeTruthy();
  });

  it("initializes once when a magic-link SIGNED_IN event arrives after an empty initial session", async () => {
    authMocks.session = null;
    render(<AdminApp />);
    await waitFor(() => expect(authMocks.listener).toBeTypeOf("function"));
    expect(authMocks.loadIdentity).not.toHaveBeenCalled();

    authMocks.session = { access_token: "magic-link-token" };
    act(() => authMocks.listener?.("SIGNED_IN", authMocks.session));

    expect(await screen.findByRole("heading", { name: "Resumen" })).toBeTruthy();
    expect(authMocks.loadIdentity).toHaveBeenCalledTimes(1);
    expect(authMocks.loadData).toHaveBeenCalledTimes(1);
  });

  it("rechecks the session when SIGNED_IN arrives during an unfinished empty-session check", async () => {
    type SessionResult = { data: { session: { access_token: string } | null }; error: null };
    let finishInitial!: (result: SessionResult) => void;
    const initial = new Promise<SessionResult>((resolve) => { finishInitial = resolve; });
    authMocks.session = null;
    authMocks.getSession
      .mockImplementationOnce(() => initial)
      .mockImplementation(async () => ({ data: { session: authMocks.session }, error: null }));

    render(<AdminApp />);
    await waitFor(() => expect(authMocks.listener).toBeTypeOf("function"));
    authMocks.session = { access_token: "racing-magic-link-token" };
    act(() => authMocks.listener?.("SIGNED_IN", authMocks.session));
    await act(async () => finishInitial({ data: { session: null }, error: null }));

    expect(await screen.findByRole("heading", { name: "Resumen" })).toBeTruthy();
    expect(authMocks.loadIdentity).toHaveBeenCalledTimes(1);
    expect(authMocks.loadData).toHaveBeenCalledTimes(1);
  });
});
