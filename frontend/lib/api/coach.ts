import { apiFetch, apiUpload } from "./client";

export function listMyStudents() {
  return apiFetch<any[]>("/api/coach/students");
}

export function addStudent(studentEmail: string) {
  return apiFetch<any>("/api/coach/students", {
    method: "POST",
    body: JSON.stringify({ student_email: studentEmail }),
  });
}

export function uploadCsv(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  return apiUpload<any>("/api/coach/upload-csv", formData);
}
