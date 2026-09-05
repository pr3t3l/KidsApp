import { describe, expect, it } from "vitest";
import { copy } from "./copy";

describe("bilingual product copy", () => {
  it("keeps the same key set in both locales", () => {
    expect(Object.keys(copy["es-US"]).sort()).toEqual(Object.keys(copy["en-US"]).sort());
  });
  it("localizes the single companion action", () => {
    expect(copy["en-US"].ask).toBe("Ask companion");
    expect(copy["es-US"].ask).toBe("Preguntar al asistente");
  });
});
