"use client";

import { useEffect, useState } from "react";
import { listMyStudents } from "@/lib/api/coach";
import { Card } from "@/components/ui/Card";
import Link from "next/link";

export default function CoachDashboardPage() {
  const [students, setStudents] = useState<any[]>([]);

  useEffect(() => {
    listMyStudents().then(setStudents);
  }, []);

  return (
    <main className="mx-auto max-w-3xl px-6 py-10">
      <h1 className="text-2xl font-bold text-brand">Coach Dashboard</h1>

      <div className="mt-6 grid grid-cols-2 gap-4">
        <Card>
          <p className="text-3xl font-bold">{students.length}</p>
          <p className="text-xs text-gray-500">Active students</p>
        </Card>
      </div>

      <nav className="mt-8 flex gap-4 text-sm font-semibold text-brand">
        <Link href="/coach/students">Students</Link>
        <Link href="/coach/upload-csv">Upload CSV</Link>
        <Link href="/coach/assignments">Assignments</Link>
      </nav>
    </main>
  );
}
