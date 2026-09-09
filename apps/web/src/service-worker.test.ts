import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

describe("offline boundary", () => {
  it("never caches API, auth, storage, or cross-origin responses", () => {
    const worker = readFileSync(resolve(process.cwd(), "public", "sw.js"), "utf8");
    expect(worker).toContain("url.origin !== self.location.origin");
    for (const path of ["/v1/", "/rest/", "/auth/", "/storage/", "/realtime/"]) expect(worker).toContain(path);
    expect(worker).toContain("no-store|private");
  });
});
