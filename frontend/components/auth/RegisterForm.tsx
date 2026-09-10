"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { register, saveToken } from "@/lib/api/auth";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

export function RegisterForm() {
  const router = useRouter();
  const [role, setRole] = useState<"student" | "coach">("student");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const token = await register(name, email, password, role);
      saveToken(token);
      document.cookie = `athliq_token=${token.access_token}; path=/`;
      router.push(role === "coach" ? "/coach/dashboard" : "/student/dashboard");
    } catch (err: any) {
      setError(err.message ?? "Registration failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="mx-auto max-w-md space-y-4 p-6">
      <div className="flex rounded-full bg-gray-100 p-1">
        <button
          type="button"
          onClick={() => setRole("student")}
          className={`flex-1 rounded-full py-2 text-xs font-semibold ${role === "student" ? "bg-brand text-white" : "text-gray-500"}`}
        >
          ATHLETE
        </button>
        <button
          type="button"
          onClick={() => setRole("coach")}
          className={`flex-1 rounded-full py-2 text-xs font-semibold ${role === "coach" ? "bg-brand text-white" : "text-gray-500"}`}
        >
          COACH
        </button>
      </div>
      <Input placeholder="Full name" value={name} onChange={(e) => setName(e.target.value)} required />
      <Input type="email" placeholder="Email address" value={email} onChange={(e) => setEmail(e.target.value)} required />
      <Input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
      {error && <p className="text-xs text-red-500">{error}</p>}
      <Button type="submit" disabled={loading}>
        {loading ? "Creating account…" : "CREATE ACCOUNT"}
      </Button>
    </form>
  );
}
