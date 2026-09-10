import Link from "next/link";
import { Button } from "@/components/ui/Button";

export default function LandingPage() {
  return (
    <main className="mx-auto max-w-3xl px-6 py-20 text-center">
      <h1 className="text-4xl font-extrabold text-brand">AthliQ</h1>
      <p className="mt-4 text-gray-600">
        Train with AI, or connect with a verified coach — one athlete profile, every sport.
      </p>
      <div className="mt-8 flex justify-center gap-4">
        <Link href="/login" className="w-40"><Button>Sign In</Button></Link>
        <Link href="/register" className="w-40"><Button variant="outline">Sign Up</Button></Link>
      </div>
    </main>
  );
}
