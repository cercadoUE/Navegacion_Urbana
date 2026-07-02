export interface LatLng {
  lat: number;
  lon: number;
}

export interface RouteResult {
  path: LatLng[];
  distance_m: number;
  distance_km: number;
  time_s: number;
  nodes_explored: number;
  nodes_in_path: number;
}

export interface RouteResponse {
  dijkstra: RouteResult;
  astar: RouteResult;
  origin: LatLng;
  dest: LatLng;
}

export interface GraphInfo {
  status: string;
  city: string;
  nodes: number;
  edges: number;
}

export interface PlacesData {
  places: Record<string, string>;
}

export interface VisualizeAlgorithmResult {
  visited: LatLng[];
  path: LatLng[];
  distance_km: number;
  time_s: number;
  nodes_explored: number;
  nodes_in_path: number;
}

export interface VisualizeResponse {
  dijkstra: VisualizeAlgorithmResult;
  astar: VisualizeAlgorithmResult;
  origin: LatLng;
  dest: LatLng;
}
