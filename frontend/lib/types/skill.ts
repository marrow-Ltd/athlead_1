export interface Skill {
  id: string;
  sport_id: string;
  parent_skill_id: string | null;
  name: string;
  description: string | null;
  skill_level: string | null;
  created_at: string;
}
