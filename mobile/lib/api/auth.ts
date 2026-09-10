import AsyncStorage from "@react-native-async-storage/async-storage";
import type { AuthToken, User } from "@/lib/types/user";
import { apiFetch, TOKEN_KEY, USER_KEY } from "./client";

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

export function me() {
  return apiFetch<User>("/api/auth/me");
}

export async function saveToken(token: AuthToken) {
  await AsyncStorage.setItem(TOKEN_KEY, token.access_token);
  await AsyncStorage.setItem(USER_KEY, JSON.stringify(token.user));
}

export async function loadStoredUser(): Promise<User | null> {
  const raw = await AsyncStorage.getItem(USER_KEY);
  return raw ? (JSON.parse(raw) as User) : null;
}

export async function logout() {
  await AsyncStorage.removeItem(TOKEN_KEY);
  await AsyncStorage.removeItem(USER_KEY);
}
