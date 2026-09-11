export const PROVIDER_BASE_URLS = {
  openrouter: "https://openrouter.ai/api/v1",
  openai: "https://api.openai.com/v1",
  anthropic: "https://api.anthropic.com/v1",
} as const;

export type ProviderSlug = keyof typeof PROVIDER_BASE_URLS;

export function isProviderSlug(value: string): value is ProviderSlug {
  return value in PROVIDER_BASE_URLS;
}
