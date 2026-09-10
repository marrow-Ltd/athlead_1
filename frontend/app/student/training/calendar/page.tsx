"use client";

import { useEffect, useState } from "react";
import { listMyPlans } from "@/lib/api/training";
import type { TrainingPlan } from "@/lib/types/training";
import { Card } from "@/components/ui/Card";

export default function TrainingCalendarPage() {
  const [plans, setPlans] = useState<TrainingPlan[]>([]);

  useEffect(() => {
    listMyPlans().then(setPlans);
  }, []);

  return (
    <main className="mx-auto max-w-3xl px-6 py-10">
      <h1 className="text-2xl font-bold text-brand">Training Calendar</h1>
      <div className="mt-4 space-y-3">
        {plans.map((p) => (
          <Card key={p.id}>
            <p className="font-semibold">{p.title}</p>
            <p className="text-xs text-gray-500">
              {p.start_date ?? "—"} to {p.end_date ?? "—"} · {p.status}
            </p>
          </Card>
        ))}
      </div>
    </main>
  );
}
