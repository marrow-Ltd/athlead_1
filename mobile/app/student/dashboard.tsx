import { useEffect, useState } from "react";
import { ScrollView, Text, View, ActivityIndicator, Pressable } from "react-native";
import { router } from "expo-router";
import { getTrainingToday } from "@/lib/api/training";
import type { TrainingAssignment } from "@/lib/types/training";
import { Card } from "@/components/ui/Card";

export default function StudentDashboardScreen() {
  const [assignments, setAssignments] = useState<TrainingAssignment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getTrainingToday()
      .then(setAssignments)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <ScrollView contentContainerStyle={{ padding: 20, gap: 12 }}>
      <Text style={{ fontSize: 22, fontWeight: "800", color: "#0F1729" }}>Your Dashboard</Text>
      <Text style={{ fontSize: 12, fontWeight: "700", color: "#6B7280", textTransform: "uppercase" }}>
        Today&apos;s training
      </Text>

      {loading && <ActivityIndicator />}
      {error && <Text style={{ color: "#EF4444", fontSize: 12 }}>{error}</Text>}

      {assignments.map((a) => (
        <Card key={a.id} style={{ flexDirection: "row", justifyContent: "space-between", alignItems: "center" }}>
          <View>
            <Text style={{ fontWeight: "700" }}>Drill #{a.drill_id.slice(0, 8)}</Text>
            <Text style={{ fontSize: 12, color: "#6B7280" }}>
              {a.sets ?? "-"} sets × {a.reps ?? "-"} reps
            </Text>
          </View>
          <View style={{ backgroundColor: "#F3F4F6", borderRadius: 999, paddingHorizontal: 10, paddingVertical: 4 }}>
            <Text style={{ fontSize: 11, fontWeight: "600", textTransform: "capitalize" }}>
              {a.status.replace("_", " ")}
            </Text>
          </View>
        </Card>
      ))}

      {!loading && assignments.length === 0 && (
        <Text style={{ fontSize: 13, color: "#9CA3AF" }}>Nothing scheduled for today yet.</Text>
      )}

      <View style={{ flexDirection: "row", gap: 20, marginTop: 12 }}>
        <Pressable onPress={() => router.push("/student/calendar")}>
          <Text style={{ color: "#0F1729", fontWeight: "700", fontSize: 13 }}>Calendar</Text>
        </Pressable>
        <Pressable onPress={() => router.push("/student/progress")}>
          <Text style={{ color: "#0F1729", fontWeight: "700", fontSize: 13 }}>Progress</Text>
        </Pressable>
      </View>
    </ScrollView>
  );
}
