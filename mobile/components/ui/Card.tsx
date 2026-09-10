import { View, ViewProps } from "react-native";

export function Card({ style, ...props }: ViewProps) {
  return (
    <View
      style={[
        {
          borderRadius: 16,
          backgroundColor: "#fff",
          padding: 16,
          shadowColor: "#000",
          shadowOpacity: 0.05,
          shadowRadius: 6,
          shadowOffset: { width: 0, height: 2 },
          elevation: 1,
        },
        style,
      ]}
      {...props}
    />
  );
}
