import type { ReactNode } from "react";
import type { BlockKind, ContentBlock, Locale } from "./types";

type Renderer = (payload: Record<string, unknown>, locale: Locale) => ReactNode;
const text = (payload: Record<string, unknown>, key: string) => typeof payload[key] === "string" ? payload[key] as string : "";
const label = (locale: Locale, english: string, spanish: string) => locale === "es-US" ? spanish : english;

export const blockRenderers: Record<BlockKind, Renderer> = {
  prep: (payload, locale) => <article className="block instruction-block"><p className="eyebrow">{label(locale,"Before you begin","Antes de empezar")}</p><h3>{text(payload,"title")}</h3><p>{text(payload,"text")}</p></article>,
  purpose: (payload, locale) => <article className="block question-block"><p className="eyebrow">{label(locale,"Purpose","Propósito")}</p><h3>{text(payload,"title")}</h3><p>{text(payload,"text")}</p></article>,
  safety: (payload, locale) => <article className="block safety-block" aria-label={label(locale,"Safety notice","Aviso de seguridad")}><span className="block-icon" aria-hidden="true">!</span><div><p className="eyebrow">{label(locale,"Safety first","Seguridad primero")}</p><h3>{text(payload,"title")}</h3><p>{text(payload,"text")}</p></div></article>,
  safety_notice: (payload, locale) => <article className="block safety-block" aria-label={label(locale,"Safety notice","Aviso de seguridad")}><span className="block-icon" aria-hidden="true">!</span><div><p className="eyebrow">{label(locale,"Safety first","Seguridad primero")}</p><h3>{text(payload,"title")}</h3><p>{text(payload,"text")}</p></div></article>,
  contribution: (payload, locale) => <article className="block"><p className="eyebrow">{label(locale,"Participation","Participación")}</p><h3>{text(payload,"title")}</h3><p>{text(payload,"text")}</p></article>,
  instruction: (payload) => <article className="block instruction-block"><p className="eyebrow">{text(payload,"eyebrow")}</p><h3>{text(payload,"title")}</h3><p>{text(payload,"text")}</p></article>,
  timer: (payload, locale) => <article className="block"><p className="eyebrow">{label(locale,"Timer","Temporizador")}</p><strong>{text(payload,"duration")}</strong></article>,
  question: (payload, locale) => <article className="block question-block"><p className="eyebrow">{label(locale,"Notice together","Observen juntos")}</p><h3>{text(payload,"prompt")}</h3></article>,
  choice: (payload) => <article className="block"><p>{text(payload,"prompt")}</p></article>,
  evidence: (payload) => <article className="block"><p>{text(payload,"prompt")}</p></article>,
  result: (payload) => <article className="block result-block"><h3>{text(payload,"title")}</h3><p>{text(payload,"text")}</p></article>,
  closeout: (payload, locale) => <article className="block result-block"><p className="eyebrow">{label(locale,"Close-out","Cierre")}</p><h3>{text(payload,"title")}</h3><p>{text(payload,"text")}</p></article>
};

export function renderBlock(block: ContentBlock, locale: Locale = "en-US"): ReactNode {
  const kind = "kind" in block ? block.kind : block.type;
  const data = "data" in block ? block.data : block.payload;
  const renderer = blockRenderers[kind];
  if (!renderer) {
    if (block.required) throw new Error(`Unsupported required block: ${kind}`);
    return null;
  }
  return renderer(data, locale);
}
