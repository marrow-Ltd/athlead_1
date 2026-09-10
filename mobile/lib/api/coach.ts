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

/** `file` should be a DocumentPicker/ImagePicker result shaped as { uri, name, type }. */
export function uploadCsv(file: { uri: string; name: string; type: string }) {
  const formData = new FormData();
  // @ts-expect-error React Native's FormData accepts this URI-based shape.
  formData.append("file", { uri: file.uri, name: file.name, type: file.type });
  return apiUpload<any>("/api/coach/upload-csv", formData);
}
