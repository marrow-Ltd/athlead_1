import { LoginForm } from "@/components/auth/LoginForm";

export default function LoginPage() {
  return (
    <main
      className="min-h-screen bg-brand bg-cover bg-center"
      style={{ backgroundImage: "linear-gradient(180deg, rgba(15,23,41,0.9), rgba(15,23,41,0.6))" }}
    >
      <div className="mx-auto flex max-w-md flex-col items-center pt-16 text-white">
        <h1 className="text-3xl font-extrabold tracking-tight">AthliQ</h1>
        <p className="mt-8 text-center text-3xl font-extrabold">WELCOME BACK</p>
        <p className="mt-2 text-sm text-white/70">Sign in to manage your athletes &amp; sessions</p>
      </div>
      <LoginForm />
    </main>
  );
}
