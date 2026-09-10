import { RegisterForm } from "@/components/auth/RegisterForm";

export default function RegisterPage() {
  return (
    <main className="min-h-screen bg-white">
      <div className="pt-12 text-center">
        <h1 className="text-2xl font-bold text-brand">Create your AthliQ account</h1>
      </div>
      <RegisterForm />
    </main>
  );
}
