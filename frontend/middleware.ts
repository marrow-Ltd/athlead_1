import { NextRequest, NextResponse } from "next/server";

/**
 * Route protection at the edge. Real role verification still happens
 * server-side on every API call (JWT) — this only improves UX by
 * redirecting obviously-unauthenticated navigations before the page loads.
 */
const STUDENT_PREFIX = "/student";
const COACH_PREFIX = "/coach";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("athliq_token")?.value;
  const { pathname } = request.nextUrl;

  const isProtected = pathname.startsWith(STUDENT_PREFIX) || pathname.startsWith(COACH_PREFIX);

  if (isProtected && !token) {
    const loginUrl = new URL("/login", request.url);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/student/:path*", "/coach/:path*"],
};
