import { useCallback, useState } from "react";
import { ScrollView, Text, View } from "react-native";
import { useFocusEffect } from "expo-router";
import { getTrainingToday, updateAssignment } from "@/lib/api/training";
import type { TrainingAssignment } from "@/lib/types/training";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

export default function TrainingTodayScreen() {
  const [assignments, setAssignments] = useState<TrainingAssignment[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(() => {
    setLoading(true);
    getTrainingToday()
      .then(setAssignments)
      .finally(() => setLoading(false));
  }, []);

  useFocusEffect(load);

  async function markDone(id: string) {
    await updateAssignment(id, { status: "completed" });
    load();
  }

  return (
    <ScrollView contentContainerStyle={{ padding: 20, gap: 12 }}>
      <Text style={{ fontSize: 20, fontWeight: "800", color: "#0F1729" }}>Today&apos;s Practice</Text>
      {assignments.map((a) => (
        <Card key={a.id} style={{ gap: 8 }}>
          <Text style={{ fontWeight: "700" }}>Drill #{a.drill_id.slice(0, 8)}</Text>
          <Text style={{ fontSize: 12, color: "#6B7280" }}>
            {a.sets ?? "-"} sets × {a.reps ?? "-"} reps
          </Text>
          {a.status !== "completed" ? (
            <Button title="Mark done" onPress={() => markDone(a.id)} />
          ) : (
            <Text style={{ fontSize: 12, fontWeight: "700", color: "#16A34A" }}>Completed</Text>
          )}
        </Card>
      ))}
      {!loading && assignments.length === 0 && (
        <Text style={{ fontSize: 13, color: "#9CA3AF" }}>Nothing scheduled for today.</Text>
      )}
    </ScrollView>
  );
}
