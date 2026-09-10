import { TextInput, TextInputProps } from "react-native";

export function Input(props: TextInputProps) {
  return (
    <TextInput
      placeholderTextColor="#9CA3AF"
      {...props}
      style={[
        {
          borderWidth: 1,
          borderColor: "#E5E7EB",
          borderRadius: 12,
          paddingHorizontal: 16,
          paddingVertical: 12,
          fontSize: 14,
          backgroundColor: "#fff",
        },
        props.style,
      ]}
    />
  );
}
