import { useEffect, useState } from "react";
import { ScrollView, Text } from "react-native";
import { listMyPlans } from "@/lib/api/training";
import type { TrainingPlan } from "@/lib/types/training";
import { Card } from "@/components/ui/Card";

export default function TrainingCalendarScreen() {
  const [plans, setPlans] = useState<TrainingPlan[]>([]);

  useEffect(() => {
    listMyPlans().then(setPlans);
  }, []);

  return (
    <ScrollView contentContainerStyle={{ padding: 20, gap: 12 }}>
      <Text style={{ fontSize: 20, fontWeight: "800", color: "#0F1729" }}>Training Calendar</Text>
      {plans.map((p) => (
        <Card key={p.id}>
          <Text style={{ fontWeight: "700" }}>{p.title}</Text>
          <Text style={{ fontSize: 12, color: "#6B7280" }}>
            {p.start_date ?? "—"} to {p.end_date ?? "—"} · {p.status}
          </Text>
        </Card>
      ))}
    </ScrollView>
  );
}
