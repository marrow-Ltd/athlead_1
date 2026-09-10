"use client";

import { useTodaysTraining } from "@/lib/hooks/useTrainingPlan";
import { Card } from "@/components/ui/Card";
import Link from "next/link";

export default function StudentDashboardPage() {
  const { assignments, loading, error } = useTodaysTraining();

  return (
    <main className="mx-auto max-w-3xl px-6 py-10">
      <h1 className="text-2xl font-bold text-brand">Your Dashboard</h1>

      <section className="mt-6">
        <h2 className="text-sm font-semibold uppercase text-gray-500">Today&apos;s training</h2>
        {loading && <p className="mt-2 text-sm text-gray-400">Loading…</p>}
        {error && <p className="mt-2 text-sm text-red-500">{error}</p>}
        <div className="mt-3 space-y-3">
          {assignments.map((a) => (
            <Card key={a.id} className="flex items-center justify-between">
              <div>
                <p className="font-semibold">Drill #{a.drill_id.slice(0, 8)}</p>
                <p className="text-xs text-gray-500">
                  {a.sets ?? "-"} sets × {a.reps ?? "-"} reps
                </p>
              </div>
              <span className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium capitalize">
                {a.status.replace("_", " ")}
              </span>
            </Card>
          ))}
          {!loading && assignments.length === 0 && (
            <p className="text-sm text-gray-400">Nothing scheduled for today yet.</p>
          )}
        </div>
      </section>

      <nav className="mt-8 flex gap-4 text-sm font-semibold text-brand">
        <Link href="/student/training/calendar">Calendar</Link>
        <Link href="/student/progress">Progress</Link>
      </nav>
    </main>
  );
}
