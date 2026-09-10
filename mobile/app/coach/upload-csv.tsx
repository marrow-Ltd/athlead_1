import { useState } from "react";
import { ScrollView, Text, View } from "react-native";
import * as DocumentPicker from "expo-document-picker";
import { uploadCsv } from "@/lib/api/coach";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";

export default function UploadCsvScreen() {
  const [fileName, setFileName] = useState<string | null>(null);
  const [fileAsset, setFileAsset] = useState<{ uri: string; name: string; type: string } | null>(null);
  const [result, setResult] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function pickFile() {
    const res = await DocumentPicker.getDocumentAsync({ type: "text/csv" });
    if (res.canceled || !res.assets?.length) return;
    const asset = res.assets[0];
    setFileName(asset.name);
    setFileAsset({ uri: asset.uri, name: asset.name, type: asset.mimeType ?? "text/csv" });
  }

  async function handleUpload() {
    if (!fileAsset) return;
    setLoading(true);
    setError(null);
    try {
      const res = await uploadCsv(fileAsset);
      setResult(res);
    } catch (err: any) {
      setError(err.message ?? "Upload failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <ScrollView contentContainerStyle={{ padding: 20, gap: 12 }}>
      <Text style={{ fontSize: 20, fontWeight: "800", color: "#0F1729" }}>Upload Student/Drill CSV</Text>
      <Text style={{ fontSize: 12, color: "#6B7280" }}>
        Expected columns: sport_name, drill_name, skill_level, day_number, sets, reps, video_url, student_email
      </Text>

      <Button title={fileName ?? "Choose CSV file"} variant="outline" onPress={pickFile} />
      <Button title={loading ? "Uploading…" : "Upload"} onPress={handleUpload} disabled={!fileAsset} loading={loading} />

      {error && <Text style={{ color: "#EF4444", fontSize: 12 }}>{error}</Text>}

      {result && (
        <Card style={{ gap: 8 }}>
          <Text style={{ fontSize: 13 }}>
            {result.inserted} inserted · {result.failed} failed out of {result.total_rows} rows
          </Text>
          {result.row_errors?.map((re: any) => (
            <Text key={re.row_number} style={{ fontSize: 11, color: "#EF4444" }}>
              Row {re.row_number}: {re.errors.join(", ")}
            </Text>
          ))}
        </Card>
      )}
    </ScrollView>
  );
}
