import { ButtonHTMLAttributes } from "react";

type Variant = "primary" | "secondary" | "outline";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
}

const variantClasses: Record<Variant, string> = {
  primary: "bg-brand text-white hover:bg-brand-light",
  secondary: "bg-gray-100 text-brand hover:bg-gray-200",
  outline: "border border-gray-300 text-brand hover:bg-gray-50",
};

export function Button({ variant = "primary", className = "", ...props }: ButtonProps) {
  return (
    <button
      className={`w-full rounded-xl px-4 py-3 text-sm font-semibold tracking-wide transition-colors ${variantClasses[variant]} ${className}`}
      {...props}
    />
  );
}
