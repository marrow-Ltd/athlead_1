import { useEffect, useState } from "react";
import { ScrollView, Text, View } from "react-native";
import { getMyProgress } from "@/lib/api/progress";
import type { StudentSkillProgress } from "@/lib/types/progress";
import { Card } from "@/components/ui/Card";

export default function ProgressScreen() {
  const [progress, setProgress] = useState<StudentSkillProgress[]>([]);

  useEffect(() => {
    getMyProgress().then(setProgress);
  }, []);

  return (
    <ScrollView contentContainerStyle={{ padding: 20, gap: 12 }}>
      <Text style={{ fontSize: 20, fontWeight: "800", color: "#0F1729" }}>Progress</Text>
      {progress.map((p) => {
        const pct = Math.round(p.mastery_score * 100);
        return (
          <Card key={p.id} style={{ gap: 8 }}>
            <View style={{ flexDirection: "row", justifyContent: "space-between" }}>
              <Text style={{ fontWeight: "700" }}>{p.proficiency_level ?? "Skill"}</Text>
              <Text style={{ color: "#6B7280" }}>{pct}%</Text>
            </View>
            <View style={{ height: 8, borderRadius: 999, backgroundColor: "#F3F4F6" }}>
              <View style={{ height: 8, borderRadius: 999, width: `${pct}%`, backgroundColor: "#0F1729" }} />
            </View>
          </Card>
        );
      })}
      {progress.length === 0 && <Text style={{ fontSize: 13, color: "#9CA3AF" }}>No progress recorded yet.</Text>}
    </ScrollView>
  );
}
