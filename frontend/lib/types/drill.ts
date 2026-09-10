export interface Drill {
  id: string;
  sport_id: string;
  skill_id: string | null;
  drill_name: string;
  description: string | null;
  skill_level: string | null;
  sets: number | null;
  reps: number | null;
  duration_minutes: number | null;
  video_url: string | null;
  is_custom: boolean;
  created_by_coach_id: string | null;
  created_at: string;
}
