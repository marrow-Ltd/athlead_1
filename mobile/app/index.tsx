import { Redirect } from "expo-router";

export default function Index() {
  // Entry point — send everyone to login; each dashboard screen itself
  // reads the stored session and redirects onward once loaded.
  return <Redirect href="/login" />;
}
