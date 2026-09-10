export default function StudentDetailPage({ params }: { params: { studentId: string } }) {
  return (
    <main className="mx-auto max-w-3xl px-6 py-10">
      <h1 className="text-2xl font-bold text-brand">Student detail</h1>
      <p className="mt-2 text-sm text-gray-500">Student ID: {params.studentId}</p>
    </main>
  );
}
