import { useState } from "react";
import { View, Text, Pressable, ScrollView } from "react-native";
import { router } from "expo-router";
import { register, saveToken } from "@/lib/api/auth";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

export default function RegisterScreen() {
  const [role, setRole] = useState<"student" | "coach">("student");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    setError(null);
    setLoading(true);
    try {
      const token = await register(name, email, password, role);
      await saveToken(token);
      router.replace(role === "coach" ? "/coach/dashboard" : "/student/dashboard");
    } catch (err: any) {
      setError(err.message ?? "Registration failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <ScrollView contentContainerStyle={{ padding: 24, gap: 16, paddingTop: 80 }}>
      <Text style={{ fontSize: 22, fontWeight: "800", color: "#0F1729", textAlign: "center" }}>
        Create your AthliQ account
      </Text>

      <View style={{ flexDirection: "row", backgroundColor: "#F3F4F6", borderRadius: 999, padding: 4 }}>
        {(["student", "coach"] as const).map((r) => (
          <Pressable
            key={r}
            onPress={() => setRole(r)}
            style={{
              flex: 1,
              paddingVertical: 10,
              borderRadius: 999,
              backgroundColor: role === r ? "#0F1729" : "transparent",
              alignItems: "center",
            }}
          >
            <Text style={{ color: role === r ? "#fff" : "#6B7280", fontSize: 11, fontWeight: "700" }}>
              {r === "student" ? "ATHLETE" : "COACH"}
            </Text>
          </Pressable>
        ))}
      </View>

      <Input placeholder="Full name" value={name} onChangeText={setName} />
      <Input placeholder="Email address" value={email} onChangeText={setEmail} autoCapitalize="none" keyboardType="email-address" />
      <Input placeholder="Password" value={password} onChangeText={setPassword} secureTextEntry />

      {error && <Text style={{ color: "#EF4444", fontSize: 12 }}>{error}</Text>}

      <Button title={loading ? "CREATING ACCOUNT…" : "CREATE ACCOUNT"} onPress={handleSubmit} loading={loading} />
    </ScrollView>
  );
}
