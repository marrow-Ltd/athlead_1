import { useEffect, useState } from "react";
import { ScrollView, Text, View, Pressable } from "react-native";
import { router } from "expo-router";
import { listMyStudents } from "@/lib/api/coach";
import { Card } from "@/components/ui/Card";

export default function CoachDashboardScreen() {
  const [students, setStudents] = useState<any[]>([]);

  useEffect(() => {
    listMyStudents().then(setStudents);
  }, []);

  return (
    <ScrollView contentContainerStyle={{ padding: 20, gap: 12 }}>
      <Text style={{ fontSize: 22, fontWeight: "800", color: "#0F1729" }}>Coach Dashboard</Text>

      <Card>
        <Text style={{ fontSize: 28, fontWeight: "800" }}>{students.length}</Text>
        <Text style={{ fontSize: 12, color: "#6B7280" }}>Active students</Text>
      </Card>

      <View style={{ flexDirection: "row", gap: 20, marginTop: 8 }}>
        <Pressable onPress={() => router.push("/coach/students")}>
          <Text style={{ color: "#0F1729", fontWeight: "700", fontSize: 13 }}>Students</Text>
        </Pressable>
        <Pressable onPress={() => router.push("/coach/upload-csv")}>
          <Text style={{ color: "#0F1729", fontWeight: "700", fontSize: 13 }}>Upload CSV</Text>
        </Pressable>
      </View>
    </ScrollView>
  );
}
