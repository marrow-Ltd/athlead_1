"use client";

import { useState } from "react";
import { updateAssignment } from "@/lib/api/training";
import { Button } from "@/components/ui/Button";

export default function DrillVideoPage({ params }: { params: { assignmentId: string } }) {
  const [saving, setSaving] = useState(false);

  async function complete() {
    setSaving(true);
    await updateAssignment(params.assignmentId, { status: "completed" });
    setSaving(false);
  }

  return (
    <main className="mx-auto max-w-2xl px-6 py-10">
      <h1 className="text-xl font-bold text-brand">Drill / Video</h1>
      <div className="mt-4 aspect-video w-full rounded-xl bg-black" />
      <div className="mt-6">
        <Button onClick={complete} disabled={saving}>
          {saving ? "Saving…" : "Mark drill as completed"}
        </Button>
      </div>
    </main>
  );
}
