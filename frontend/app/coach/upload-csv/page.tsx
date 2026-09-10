"use client";

import { useState } from "react";
import { uploadCsv } from "@/lib/api/coach";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";

export default function UploadCsvPage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleUpload() {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const res = await uploadCsv(file);
      setResult(res);
    } catch (err: any) {
      setError(err.message ?? "Upload failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-3xl px-6 py-10">
      <h1 className="text-2xl font-bold text-brand">Upload Student/Drill CSV</h1>
      <p className="mt-2 text-sm text-gray-500">
        Expected columns: sport_name, drill_name, skill_level, day_number, sets, reps, video_url, student_email
      </p>

      <div className="mt-4 flex items-center gap-3">
        <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
        <Button className="w-40" onClick={handleUpload} disabled={!file || loading}>
          {loading ? "Uploading…" : "Upload"}
        </Button>
      </div>

      {error && <p className="mt-3 text-sm text-red-500">{error}</p>}

      {result && (
        <Card className="mt-6">
          <p className="text-sm">
            {result.inserted} inserted · {result.failed} failed out of {result.total_rows} rows
          </p>
          {result.row_errors?.length > 0 && (
            <ul className="mt-2 space-y-1 text-xs text-red-500">
              {result.row_errors.map((re: any) => (
                <li key={re.row_number}>
                  Row {re.row_number}: {re.errors.join(", ")}
                </li>
              ))}
            </ul>
          )}
        </Card>
      )}
    </main>
  );
}
