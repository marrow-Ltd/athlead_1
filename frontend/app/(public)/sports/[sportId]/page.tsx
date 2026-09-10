"use client";

import { useEffect, useState } from "react";
import { getSport } from "@/lib/api/sports";
import type { Sport } from "@/lib/types/sport";

export default function SportDetailPage({ params }: { params: { sportId: string } }) {
  const [sport, setSport] = useState<Sport | null>(null);

  useEffect(() => {
    getSport(params.sportId).then(setSport);
  }, [params.sportId]);

  if (!sport) return <main className="p-10 text-sm text-gray-400">Loading…</main>;

  return (
    <main className="mx-auto max-w-3xl px-6 py-10">
      <h1 className="text-2xl font-bold text-brand">{sport.name}</h1>
      <p className="mt-2 text-gray-600">{sport.description}</p>
    </main>
  );
}
