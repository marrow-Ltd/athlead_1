import type { Drill } from "./drill";

export interface Sport {
  id: string;
  name: string;
  description: string | null;
  image_url: string | null;
  created_at: string;
}

export interface SportSearchResponse {
  system: Sport[];
  coach_custom_drills: Drill[];
}
