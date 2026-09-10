import { useState } from "react";
import { View, Text, Pressable, KeyboardAvoidingView, Platform, ScrollView } from "react-native";
import { router, Link } from "expo-router";
import { login, saveToken } from "@/lib/api/auth";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

type Role = "student" | "coach";

export default function LoginScreen() {
  const [role, setRole] = useState<Role>("coach");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    setError(null);
    setLoading(true);
    try {
      const token = await login(email, password);
      await saveToken(token);
      router.replace(role === "coach" ? "/coach/dashboard" : "/student/dashboard");
    } catch (err: any) {
      setError(err.message ?? "Login failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <View style={{ flex: 1, backgroundColor: "#0F1729" }}>
      <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : undefined} style={{ flex: 1 }}>
        <ScrollView contentContainerStyle={{ flexGrow: 1, justifyContent: "flex-end" }}>
          <View style={{ alignItems: "center", paddingTop: 80, paddingHorizontal: 24 }}>
            <Text style={{ color: "#fff", fontSize: 22, fontWeight: "800" }}>AthliQ</Text>
            <Text style={{ color: "#fff", fontSize: 26, fontWeight: "800", marginTop: 32, textAlign: "center" }}>
              WELCOME BACK
            </Text>
            <Text style={{ color: "rgba(255,255,255,0.7)", fontSize: 13, marginTop: 8, textAlign: "center" }}>
              Sign in to manage your athletes & sessions
            </Text>
          </View>

          <View
            style={{
              backgroundColor: "rgba(255,255,255,0.97)",
              borderTopLeftRadius: 28,
              borderTopRightRadius: 28,
              padding: 24,
              marginTop: 32,
              gap: 16,
            }}
          >
            <View style={{ flexDirection: "row", backgroundColor: "#F3F4F6", borderRadius: 999, padding: 4 }}>
              {(["student", "coach"] as Role[]).map((r) => (
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
                  <Text
                    style={{
                      color: role === r ? "#fff" : "#6B7280",
                      fontSize: 11,
                      fontWeight: "700",
                      letterSpacing: 0.5,
                    }}
                  >
                    {r === "student" ? "ATHLETE" : "COACH"}
                  </Text>
                </Pressable>
              ))}
            </View>

            <View style={{ gap: 10 }}>
              <Button title="Continue with Google" variant="outline" onPress={() => {}} />
              <Button title="Continue with Apple" variant="outline" onPress={() => {}} />
            </View>

            <Text style={{ textAlign: "center", fontSize: 11, color: "#9CA3AF", letterSpacing: 0.5 }}>
              OR CONTINUE WITH EMAIL
            </Text>

            <View style={{ gap: 4 }}>
              <Text style={{ fontSize: 11, fontWeight: "700", color: "#6B7280" }}>EMAIL ADDRESS</Text>
              <Input
                value={email}
                onChangeText={setEmail}
                autoCapitalize="none"
                keyboardType="email-address"
                placeholder={role === "coach" ? "coach@athliq.com" : "athlete@athliq.com"}
              />
            </View>

            <View style={{ gap: 4 }}>
              <Text style={{ fontSize: 11, fontWeight: "700", color: "#6B7280" }}>PASSWORD</Text>
              <View>
                <Input value={password} onChangeText={setPassword} secureTextEntry={!showPassword} />
                <Pressable onPress={() => setShowPassword((v) => !v)} style={{ position: "absolute", right: 14, top: 12 }}>
                  <Text style={{ fontSize: 11, color: "#9CA3AF" }}>{showPassword ? "Hide" : "Show"}</Text>
                </Pressable>
              </View>
            </View>

            {error && <Text style={{ color: "#EF4444", fontSize: 12 }}>{error}</Text>}

            <Button title={loading ? "SIGNING IN…" : "SIGN IN"} onPress={handleSubmit} loading={loading} />

            <View style={{ flexDirection: "row", justifyContent: "center", gap: 4 }}>
              <Text style={{ fontSize: 12, color: "#6B7280" }}>Don&apos;t have an account?</Text>
              <Link href="/register">
                <Text style={{ fontSize: 12, fontWeight: "700", color: "#0F1729" }}>Sign Up</Text>
              </Link>
            </View>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </View>
  );
}
