import { ActivityIndicator, Pressable, Text } from "react-native";

type Variant = "primary" | "outline";

interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: Variant;
  loading?: boolean;
  disabled?: boolean;
}

export function Button({ title, onPress, variant = "primary", loading, disabled }: ButtonProps) {
  const isPrimary = variant === "primary";
  return (
    <Pressable
      onPress={onPress}
      disabled={disabled || loading}
      style={{
        backgroundColor: isPrimary ? "#0F1729" : "#fff",
        borderWidth: isPrimary ? 0 : 1,
        borderColor: "#D1D5DB",
        borderRadius: 12,
        paddingVertical: 14,
        alignItems: "center",
        opacity: disabled || loading ? 0.6 : 1,
      }}
    >
      {loading ? (
        <ActivityIndicator color={isPrimary ? "#fff" : "#0F1729"} />
      ) : (
        <Text
          style={{
            color: isPrimary ? "#fff" : "#0F1729",
            fontWeight: "700",
            fontSize: 13,
            letterSpacing: 0.5,
          }}
        >
          {title}
        </Text>
      )}
    </Pressable>
  );
}
