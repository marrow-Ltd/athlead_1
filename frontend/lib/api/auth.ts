import type { AuthToken, User } from "@/lib/types/user";
import { apiFetch } from "./client";

export function register(name: string, email: string, password: string, role: "student" | "coach") {
  return apiFetch<AuthToken>("/api/auth/register", {
    method: "POST",
    body: JSON.stringify({ name, email, password, role }),
  });
}

export function login(email: string, password: string) {
  return apiFetch<AuthToken>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export function googleLogin(idToken: string, role: "student" | "coach") {
  return apiFetch<AuthToken>("/api/auth/google", {
    method: "POST",
    body: JSON.stringify({ id_token: idToken, role }),
  });
}

export function me() {
  return apiFetch<User>("/api/auth/me");
}

export function saveToken(token: AuthToken) {
  window.localStorage.setItem("athliq_token", token.access_token);
  window.localStorage.setItem("athliq_user", JSON.stringify(token.user));
}

export function logout() {
  window.localStorage.removeItem("athliq_token");
  window.localStorage.removeItem("athliq_user");
}