import { describe, expect, it } from "vitest";
import { getCatalog } from "./api";

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
