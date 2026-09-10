export interface StudentSkillProgress {
  id: string;
  student_id: string;
  skill_id: string;
  mastery_score: number;
  proficiency_level: string | null;
  last_practiced_at: string | null;
  updated_at: string;
}
