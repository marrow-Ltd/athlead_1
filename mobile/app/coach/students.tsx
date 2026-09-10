import { useState, useCallback } from "react";
import { ScrollView, Text, View } from "react-native";
import { useFocusEffect } from "expo-router";
import { addStudent, listMyStudents } from "@/lib/api/coach";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";

export default function CoachStudentsScreen() {
  const [students, setStudents] = useState<any[]>([]);
  const [email, setEmail] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const refresh = useCallback(() => {
    listMyStudents().then(setStudents);
  }, []);

  useFocusEffect(refresh);

  async function handleAdd() {
    setError(null);
    setLoading(true);
    try {
      await addStudent(email);
      setEmail("");
      refresh();
    } catch (err: any) {
      setError(err.message ?? "Could not add student.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <ScrollView contentContainerStyle={{ padding: 20, gap: 12 }}>
      <Text style={{ fontSize: 20, fontWeight: "800", color: "#0F1729" }}>Students</Text>

      <View style={{ gap: 8 }}>
        <Input
          placeholder="Student's email"
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address"
        />
        <Button title="Add student" onPress={handleAdd} loading={loading} disabled={!email} />
      </View>
      {error && <Text style={{ color: "#EF4444", fontSize: 12 }}>{error}</Text>}

      {students.map((s) => (
        <Card key={s.id}>
          <Text style={{ fontSize: 12, color: "#6B7280" }}>Student ID: {s.student_id}</Text>
          <Text style={{ fontSize: 12, color: "#6B7280", textTransform: "capitalize" }}>Status: {s.status}</Text>
        </Card>
      ))}
    </ScrollView>
  );
}
