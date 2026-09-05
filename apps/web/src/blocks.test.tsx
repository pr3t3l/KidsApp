import { describe, expect, it } from "vitest";
import { renderBlock } from "./blocks";
import type { ContentBlock } from "./types";

describe("block registry", () => {
  it("renders a supported instruction", () => { const block: ContentBlock = { id: "one", type: "instruction", required: true, payload: { title: "Build" } }; expect(renderBlock(block)).not.toBeNull(); });
  it("fails closed for an unknown required block", () => { const block = { id: "future", type: "future_block", required: true, payload: {} } as unknown as ContentBlock; expect(() => renderBlock(block)).toThrow("Unsupported required block"); });
  it("ignores an unknown optional block", () => { const block = { id: "future", type: "future_block", required: false, payload: {} } as unknown as ContentBlock; expect(renderBlock(block)).toBeNull(); });
});
