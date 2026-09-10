"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login, saveToken } from "@/lib/api/auth";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { GoogleButton } from "./GoogleButton";

type Role = "student" | "coach";

export function LoginForm() {
  const router = useRouter();
  const [role, setRole] = useState<Role>("coach");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const token = await login(email, password);
      saveToken(token);
      document.cookie = `athliq_token=${token.access_token}; path=/`;
      router.push(role === "coach" ? "/coach/dashboard" : "/student/dashboard");
    } catch (err: any) {
      setError(err.message ?? "Login failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto flex min-h-screen max-w-md flex-col justify-end">
      <div className="rounded-t-3xl bg-white/95 p-6 pt-8 shadow-xl backdrop-blur">
        <div className="mb-6 flex rounded-full bg-gray-100 p-1">
          <button
            type="button"
            onClick={() => setRole("student")}
            className={`flex-1 rounded-full py-2 text-xs font-semibold tracking-wide ${
              role === "student" ? "bg-brand text-white" : "text-gray-500"
            }`}
          >
            ATHLETE
          </button>
          <button
            type="button"
            onClick={() => setRole("coach")}
            className={`flex-1 rounded-full py-2 text-xs font-semibold tracking-wide ${
              role === "coach" ? "bg-brand text-white" : "text-gray-500"
            }`}
          >
            COACH
          </button>
        </div>

        <div className="space-y-3">
          <GoogleButton role={role} />
          <Button variant="outline" type="button">
            Continue with Apple
          </Button>
        </div>

        <div className="my-6 flex items-center gap-3 text-xs text-gray-400">
          <div className="h-px flex-1 bg-gray-200" />
          OR CONTINUE WITH EMAIL
          <div className="h-px flex-1 bg-gray-200" />
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="mb-1 block text-xs font-semibold text-gray-500">EMAIL ADDRESS</label>
            <Input
              type="email"
              placeholder={role === "coach" ? "coach@athliq.com" : "athlete@athliq.com"}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div>
            <label className="mb-1 block text-xs font-semibold text-gray-500">PASSWORD</label>
            <div className="relative">
              <Input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword((v) => !v)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-gray-400"
              >
                {showPassword ? "Hide" : "Show"}
              </button>
            </div>
          </div>

          <div className="flex items-center justify-between text-xs">
            <label className="flex items-center gap-2 text-gray-500">
              <input type="checkbox" className="rounded border-gray-300" />
              Remember me
            </label>
            <a href="#" className="font-semibold text-brand">
              Forgot password?
            </a>
          </div>

          {error && <p className="text-xs text-red-500">{error}</p>}

          <Button type="submit" disabled={loading}>
            {loading ? "Signing in…" : "SIGN IN"}
          </Button>
        </form>

        <p className="mt-6 text-center text-xs text-gray-500">
          Don&apos;t have an account?{" "}
          <a href="/register" className="font-semibold text-brand">
            Sign Up
          </a>
        </p>
      </div>
    </div>
  );
}