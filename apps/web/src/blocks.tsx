import type { ReactNode } from "react";
import type { ContentBlock } from "./types";

type Renderer = (payload: Record<string, unknown>) => ReactNode;
const text = (payload: Record<string, unknown>, key: string) => typeof payload[key] === "string" ? payload[key] as string : "";

export const blockRenderers: Record<ContentBlock["type"], Renderer> = {
  safety_notice: (payload) => <article className="block safety-block" aria-label="Safety notice"><span className="block-icon" aria-hidden="true">!</span><div><p className="eyebrow">Safety first</p><h3>{text(payload,"title")}</h3><p>{text(payload,"text")}</p></div></article>,
  instruction: (payload) => <article className="block instruction-block"><p className="eyebrow">{text(payload,"eyebrow")}</p><h3>{text(payload,"title")}</h3><p>{text(payload,"text")}</p></article>,
  timer: (payload) => <article className="block"><p className="eyebrow">Timer</p><strong>{text(payload,"duration")}</strong></article>,
  question: (payload) => <article className="block question-block"><p className="eyebrow">Notice together</p><h3>{text(payload,"prompt")}</h3></article>,
  choice: (payload) => <article className="block"><p>{text(payload,"prompt")}</p></article>,
  evidence: (payload) => <article className="block"><p>{text(payload,"prompt")}</p></article>,
  result: (payload) => <article className="block result-block"><h3>{text(payload,"title")}</h3><p>{text(payload,"text")}</p></article>
};

export function renderBlock(block: ContentBlock): ReactNode {
  const renderer = blockRenderers[block.type];
  if (!renderer) {
    if (block.required) throw new Error(`Unsupported required block: ${block.type}`);
    return null;
  }
  return renderer(block.payload);
}
