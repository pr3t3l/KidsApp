import { closeFamilySession, updateSessionProgress } from "./api";
import type { ExperienceView, FamilySession } from "./types";

const DB_NAME = "kids-learning-private-v1";
const STORE = "encrypted-records";
const KEY_ID = "device-key";
const ACTIVE_ID = "active-session";
const MAX_AGE_MS = 7 * 24 * 60 * 60 * 1000;

type EncryptedRecord = { id: string; iv: ArrayBuffer; cipher: ArrayBuffer; savedAt: number };
type OfflineEvent =
  | { id: string; kind: "progress"; sessionId: string; blockId: string; status: "active" | "paused" | "completed" | "interrupted"; createdAt: string }
  | { id: string; kind: "closeout"; sessionId: string; outcome: "worked" | "partly" | "not_today"; observation: string; durationMinutes: number; createdAt: string };

export type OfflineSession = { record: FamilySession; experience: ExperienceView; savedAt: string };

function available() {
  return typeof indexedDB !== "undefined" && Boolean(globalThis.crypto?.subtle);
}

function requestResult<T>(request: IDBRequest<T>): Promise<T> {
  return new Promise((resolve, reject) => {
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error ?? new Error("IndexedDB request failed"));
  });
}

async function database(): Promise<IDBDatabase> {
  const request = indexedDB.open(DB_NAME, 1);
  request.onupgradeneeded = () => request.result.createObjectStore(STORE, { keyPath: "id" });
  return requestResult(request);
}

async function transaction<T>(mode: IDBTransactionMode, action: (store: IDBObjectStore) => IDBRequest<T>): Promise<T> {
  const db = await database();
  try { return await requestResult(action(db.transaction(STORE, mode).objectStore(STORE))); }
  finally { db.close(); }
}

async function deviceKey(): Promise<CryptoKey> {
  const existing = await transaction("readonly", store => store.get(KEY_ID)) as { id: string; key: CryptoKey } | undefined;
  if (existing?.key) return existing.key;
  const key = await crypto.subtle.generateKey({ name: "AES-GCM", length: 256 }, false, ["encrypt", "decrypt"]);
  await transaction("readwrite", store => store.put({ id: KEY_ID, key }));
  return key;
}

async function putEncrypted(id: string, value: unknown): Promise<void> {
  if (!available()) return;
  const key = await deviceKey();
  const iv = new Uint8Array(new ArrayBuffer(12));
  crypto.getRandomValues(iv);
  const plain = new TextEncoder().encode(JSON.stringify(value));
  const cipher = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, plain);
  await transaction("readwrite", store => store.put({ id, iv: iv.buffer, cipher, savedAt: Date.now() } satisfies EncryptedRecord));
}

async function readEncrypted<T>(id: string): Promise<T | null> {
  if (!available()) return null;
  const row = await transaction("readonly", store => store.get(id)) as EncryptedRecord | undefined;
  if (!row) return null;
  if (Date.now() - row.savedAt > MAX_AGE_MS) { await remove(id); return null; }
  try {
    const plain = await crypto.subtle.decrypt({ name: "AES-GCM", iv: row.iv }, await deviceKey(), row.cipher);
    return JSON.parse(new TextDecoder().decode(plain)) as T;
  } catch {
    await remove(id);
    return null;
  }
}

async function remove(id: string): Promise<void> {
  if (available()) await transaction("readwrite", store => store.delete(id));
}

async function eventIds(): Promise<string[]> {
  if (!available()) return [];
  const keys = await transaction("readonly", store => store.getAllKeys());
  return keys.map(String).filter(key => key.startsWith("event:"));
}

export function isNetworkFailure(reason: unknown): boolean {
  return !navigator.onLine || reason instanceof TypeError || reason instanceof DOMException && reason.name === "NetworkError";
}

export async function saveActiveSession(record: FamilySession, experience: ExperienceView): Promise<void> {
  await putEncrypted(ACTIVE_ID, { record, experience, savedAt: new Date().toISOString() } satisfies OfflineSession);
}

export async function loadActiveSession(): Promise<OfflineSession | null> {
  return readEncrypted<OfflineSession>(ACTIVE_ID);
}

export async function clearActiveSession(): Promise<void> {
  await remove(ACTIVE_ID);
}

export async function queueProgress(sessionId: string, blockId: string, status: "active" | "paused" | "completed" | "interrupted"): Promise<void> {
  const event: OfflineEvent = { id: `progress:${sessionId}`, kind: "progress", sessionId, blockId, status, createdAt: new Date().toISOString() };
  await putEncrypted(`event:${event.id}`, event);
}

export async function queueCloseout(sessionId: string, outcome: "worked" | "partly" | "not_today", observation: string, durationMinutes: number): Promise<void> {
  const event: OfflineEvent = { id: `closeout:${sessionId}`, kind: "closeout", sessionId, outcome, observation, durationMinutes, createdAt: new Date().toISOString() };
  await putEncrypted(`event:${event.id}`, event);
  await remove(`event:progress:${sessionId}`);
}

export async function pendingOfflineEvents(): Promise<number> {
  return (await eventIds()).length;
}

export async function flushOfflineEvents(): Promise<{ synced: number; remaining: number }> {
  if (!navigator.onLine) return { synced: 0, remaining: await pendingOfflineEvents() };
  let synced = 0;
  const ids = await eventIds();
  for (const id of ids.sort()) {
    const event = await readEncrypted<OfflineEvent>(id);
    if (!event) continue;
    try {
      if (event.kind === "progress") await updateSessionProgress(event.sessionId, event.blockId, event.status);
      else await closeFamilySession(event.sessionId, event.outcome, event.observation, event.durationMinutes);
      await remove(id);
      synced += 1;
    } catch (reason) {
      if (isNetworkFailure(reason)) break;
      // Authorization and invariant failures stay queued for adult/support review.
      break;
    }
  }
  return { synced, remaining: await pendingOfflineEvents() };
}
