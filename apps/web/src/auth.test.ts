import { afterEach, describe, expect, it, vi } from "vitest";
import { deferAuthStateWork } from "./auth";

afterEach(() => vi.useRealTimers());

describe("Supabase auth state follow-up", () => {
  it("runs follow-up work only after the auth callback can return", () => {
    vi.useFakeTimers();
    const work = vi.fn();

    deferAuthStateWork(work);

    expect(work).not.toHaveBeenCalled();
    vi.runAllTimers();
    expect(work).toHaveBeenCalledOnce();
  });
});
