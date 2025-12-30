// features/stats/stats.api.ts

export async function fetchOverviewStats() {
  try {
    const res = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/stats/overview`,
      {
        credentials: "include",
        cache: "no-store", 
      }
    );

    if (!res.ok) {
      return null;
    }

    return await res.json();
  } catch (error) {
    return null;
  }
}