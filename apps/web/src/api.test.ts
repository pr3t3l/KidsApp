import { afterEach, describe, expect, it, vi } from "vitest";
import { apiRequest, cancelAdminMfaRequests, getCatalog, resumeAdminMfaRequests } from "./api";

afterEach(() => {
  cancelAdminMfaRequests();
  vi.restoreAllMocks();
});

describe("family catalog eligibility", () => {
  it("fails closed for risk C and D versions in both demo locales", async () => {
    for (const locale of ["es-US", "en-US"] as const) {
      const cards = await getCatalog(locale);

      expect(cards).toHaveLength(12);
      expect(cards.every(card => card.risk === "A" || card.risk === "B")).toBe(true);
      expect(cards.some(card => card.activityVersionId === "ACT-0003@1.0.0")).toBe(false);
      expect(cards.some(card => card.activityVersionId === "ACT-0013@1.0.0")).toBe(true);
    }
  });
});

describe("administrative MFA retry", () => {
  it("keeps a sensitive request pending and retries it after reauthentication", async () => {
    const mfaRequired = vi.fn();
    window.addEventListener("kids:mfa-required", mfaRequired);
    const fetchMock = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response('{"detail":"Recent MFA verification required"}', { status: 403 }))
      .mockResolvedValueOnce(new Response('{"saved":true}', { status: 200, headers: { "Content-Type": "application/json" } }));

    const pending = apiRequest<{ saved: boolean }>("/v1/admin/ai/connections", { method: "POST", body: '{"apiKey":"write-only"}' });
    await vi.waitFor(() => expect(mfaRequired).toHaveBeenCalledOnce());
    expect(fetchMock).toHaveBeenCalledTimes(1);

    resumeAdminMfaRequests();
    await expect(pending).resolves.toEqual({ saved: true });
    expect(fetchMock).toHaveBeenCalledTimes(2);
    window.removeEventListener("kids:mfa-required", mfaRequired);
  });
});
