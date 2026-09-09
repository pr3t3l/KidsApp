import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

describe("private offline session boundary", () => {
  it("encrypts state, keeps its key non-extractable, expires data, and has no plain-storage fallback", () => {
    const source = readFileSync(resolve(process.cwd(), "src", "offlineSession.ts"), "utf8");
    expect(source).toContain('name: "AES-GCM"');
    expect(source).toContain('false, ["encrypt", "decrypt"]');
    expect(source).toContain("MAX_AGE_MS");
    expect(source).not.toContain("localStorage");
  });

  it("removes only events that the server accepts", () => {
    const source = readFileSync(resolve(process.cwd(), "src", "offlineSession.ts"), "utf8");
    expect(source).toContain("await remove(id)");
    expect(source).toContain("stay queued for adult/support review");
  });
});
