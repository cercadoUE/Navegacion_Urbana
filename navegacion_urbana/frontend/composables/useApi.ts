import type { RouteResponse, GraphInfo } from "~/types";

const API_BASE = "http://localhost:8000";

export function useApi() {
  async function getGraphInfo(): Promise<GraphInfo> {
    const res = await fetch(`${API_BASE}/api/graph-info`);
    return res.json();
  }

  async function findRoute(
    originLat: number,
    originLon: number,
    destLat: number,
    destLon: number
  ): Promise<RouteResponse> {
    const res = await fetch(`${API_BASE}/api/route`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        origin_lat: originLat,
        origin_lon: originLon,
        dest_lat: destLat,
        dest_lon: destLon,
      }),
    });
    return res.json();
  }

  return { getGraphInfo, findRoute };
}
