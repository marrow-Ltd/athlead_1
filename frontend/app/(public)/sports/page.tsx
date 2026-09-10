"use client";

import { useEffect, useState } from "react";
import { searchSports } from "@/lib/api/sports";
import type { Sport } from "@/lib/types/sport";
import { Input } from "@/components/ui/Input";
import { Card } from "@/components/ui/Card";

export default function SportsDiscoveryPage() {
  const [query, setQuery] = useState("");
  const [sports, setSports] = useState<Sport[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    searchSports(query)
      .then((res) => setSports(res.system))
      .finally(() => setLoading(false));
  }, [query]);

  return (
    <main className="mx-auto max-w-3xl px-6 py-10">
      <h1 className="text-2xl font-bold text-brand">Discover a sport</h1>
      <div className="mt-4">
        <Input placeholder="Search your sport…" value={query} onChange={(e) => setQuery(e.target.value)} />
      </div>
      <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-3">
        {loading && <p className="col-span-full text-sm text-gray-400">Loading…</p>}
        {sports.map((sport) => (
          <Card key={sport.id} className="text-center">
            <p className="font-semibold">{sport.name}</p>
          </Card>
        ))}
      </div>
    </main>
  );
}
