export type TrainingPlanSourceType = "system" | "ai" | "coach";
export type TrainingPlanStatus = "active" | "completed" | "archived";
export type AssignmentStatus = "pending" | "in_progress" | "completed" | "skipped";

export interface TrainingPlan {
  id: string;
  student_id: string;
  sport_id: string;
  source_type: TrainingPlanSourceType;
  title: string;
  description: string | null;
  start_date: string | null;
  end_date: string | null;
  status: TrainingPlanStatus;
  created_at: string;
}

export interface TrainingAssignment {
  id: string;
  training_plan_id: string;
  student_id: string;
  day_number: number | null;
  scheduled_date: string | null;
  drill_id: string;
  sets: number | null;
  reps: number | null;
  status: AssignmentStatus;
  notes: string | null;
}
