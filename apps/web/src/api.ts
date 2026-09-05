import { demoExperience } from "./demo";
import type { CompanionResponse, ExperienceView } from "./types";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const DEMO_MODE = import.meta.env.VITE_DEMO_MODE !== "false";

function headers(): HeadersInit {
  const token = window.localStorage.getItem("kids.access_token");
  return {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  };
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, { ...init, headers: { ...headers(), ...init?.headers } });
  if (!response.ok) {
    const body = await response.text();
    throw new Error(body || `Request failed (${response.status})`);
  }
  return response.json() as Promise<T>;
}

export async function getExperience(contextId: string): Promise<ExperienceView> {
  if (DEMO_MODE) return structuredClone(demoExperience);
  return request<ExperienceView>(`/v1/experiences/${contextId}`);
}

export async function sendInteraction(contextId: string, message: string, locale: string): Promise<CompanionResponse> {
  return request<CompanionResponse>("/v1/companion/interactions", {
    method: "POST",
    body: JSON.stringify({ contextId, message, locale })
  });
}

export async function decideProposal(proposalId: string, decision: "confirm" | "reject", optionId?: string): Promise<ExperienceView> {
  return request<ExperienceView>(`/v1/companion/proposals/${proposalId}/decision`, {
    method: "POST",
    headers: { "Idempotency-Key": crypto.randomUUID() },
    body: JSON.stringify({ decision, optionId })
  });
}
