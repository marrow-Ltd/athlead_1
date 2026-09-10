"use client";

import { useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api/client";
import { saveToken } from "@/lib/api/auth";
import type { AuthToken } from "@/lib/types/user";

declare global {
  interface Window {
    google?: any;
  }
}

interface GoogleButtonProps {
  role: "student" | "coach";
}

export function GoogleButton({ role }: GoogleButtonProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const router = useRouter();

  useEffect(() => {
    let cancelled = false;

    function init() {
      if (cancelled || !window.google || !containerRef.current) return;

      window.google.accounts.id.initialize({
        client_id: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID,
        callback: async (response: { credential: string }) => {
          try {
            const token = await apiFetch<AuthToken>("/api/auth/google", {
              method: "POST",
              body: JSON.stringify({ id_token: response.credential, role }),
            });
            saveToken(token);
            document.cookie = `athliq_token=${token.access_token}; path=/`;
            router.push(role === "coach" ? "/coach/dashboard" : "/student/dashboard");
          } catch (err) {
            console.error("Google sign-in failed:", err);
          }
        },
      });

      containerRef.current.innerHTML = "";
      window.google.accounts.id.renderButton(containerRef.current, {
        theme: "outline",
        size: "large",
        width: 320,
        text: "continue_with",
      });
    }

    // The GIS script loads async (see layout.tsx) — poll briefly until it's ready.
    if (window.google) {
      init();
    } else {
      const interval = setInterval(() => {
        if (window.google) {
          clearInterval(interval);
          init();
        }
      }, 100);
      return () => {
        cancelled = true;
        clearInterval(interval);
      };
    }
  }, [role, router]);

  return <div ref={containerRef} className="flex justify-center" />;
}