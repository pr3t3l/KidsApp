import { afterEach, describe, expect, it, vi } from "vitest";
import { apiRequest, getCatalog } from "./api";

afterEach(() => {
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

describe("administrative authorization failures", () => {
  it("never resubmits a write-only secret automatically after an MFA failure", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response('{"detail":"MFA verification required"}', { status: 403 }));

    await expect(apiRequest<{ saved: boolean }>("/v1/admin/ai/connections", {
      method: "POST",
      body: '{"apiKey":"write-only"}'
    })).rejects.toThrow("La sesión administrativa ya no tiene MFA válido");
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });
});
