"use client";

import { useEffect, useState } from "react";
import { addStudent, listMyStudents } from "@/lib/api/coach";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";

export default function CoachStudentsPage() {
  const [students, setStudents] = useState<any[]>([]);
  const [email, setEmail] = useState("");
  const [error, setError] = useState<string | null>(null);

  function refresh() {
    listMyStudents().then(setStudents);
  }

  useEffect(refresh, []);

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await addStudent(email);
      setEmail("");
      refresh();
    } catch (err: any) {
      setError(err.message ?? "Could not add student.");
    }
  }

  return (
    <main className="mx-auto max-w-3xl px-6 py-10">
      <h1 className="text-2xl font-bold text-brand">Students</h1>

      <form onSubmit={handleAdd} className="mt-4 flex gap-2">
        <Input
          type="email"
          placeholder="Student's email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <Button type="submit" className="w-40">Add student</Button>
      </form>
      {error && <p className="mt-2 text-xs text-red-500">{error}</p>}

      <div className="mt-6 space-y-3">
        {students.map((s) => (
          <Card key={s.id}>
            <p className="text-xs text-gray-500">Student ID: {s.student_id}</p>
            <p className="text-xs capitalize text-gray-500">Status: {s.status}</p>
          </Card>
        ))}
      </div>
    </main>
  );
}
