import { Stack } from "expo-router";

export default function CoachLayout() {
  return <Stack screenOptions={{ headerShown: true, headerBackTitle: "Back" }} />;
}
