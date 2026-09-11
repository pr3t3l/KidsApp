import { describe, expect, it } from "vitest";

import { isProviderSlug, PROVIDER_BASE_URLS, requirePassedProviderHealth } from "./providerConfig";

describe("provider connection configuration", () => {
  it("keeps each direct provider on its own credential origin", () => {
    expect(PROVIDER_BASE_URLS.openrouter).toBe("https://openrouter.ai/api/v1");
    expect(PROVIDER_BASE_URLS.openai).toBe("https://api.openai.com/v1");
    expect(PROVIDER_BASE_URLS.anthropic).toBe("https://api.anthropic.com/v1");
    expect(new Set(Object.values(PROVIDER_BASE_URLS))).toHaveLength(3);
  });

  it("rejects unknown provider slugs", () => {
    expect(isProviderSlug("openai")).toBe(true);
    expect(isProviderSlug("custom-proxy")).toBe(false);
  });

  it("does not present a failed provider health check as successful", () => {
    expect(() => requirePassedProviderHealth({
      status: "failed",
      checkedAt: "2026-09-11T14:00:00Z",
      detail: "Provider returned HTTP 401",
    })).toThrow("Provider returned HTTP 401");
    expect(requirePassedProviderHealth({
      status: "passed",
      checkedAt: "2026-09-11T14:00:00Z",
      detail: "Provider returned HTTP 200",
    })).toBe("2026-09-11T14:00:00Z");
  });
});
