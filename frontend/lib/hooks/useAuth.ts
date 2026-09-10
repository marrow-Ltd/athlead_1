"use client";

import { useEffect, useState } from "react";
import type { User } from "@/lib/types/user";

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const raw = window.localStorage.getItem("athliq_user");
    setUser(raw ? (JSON.parse(raw) as User) : null);
    setLoading(false);
  }, []);

  return { user, loading, isAuthenticated: !!user };
}
