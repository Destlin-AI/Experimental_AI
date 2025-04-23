export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export async function fetchCurrentFragments() {
  try {
    const res = await fetch(`${API_BASE}/api/fragments/current`);
    if (!res.ok) throw new Error("Failed to fetch fragments");
    return await res.json();
  } catch (err) {
    console.error("[API ERROR]", err);
    return [];
  }
}