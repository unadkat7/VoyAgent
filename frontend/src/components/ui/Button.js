"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import Spinner from "./Spinner";

/**
 * Reusable Button component with multiple variants and sizes.
 *
 * @param {string}  variant   - "primary" | "secondary" | "outline" | "ghost"
 * @param {string}  size      - "sm" | "md" | "lg"
 * @param {boolean} loading   - Shows a spinner and disables the button
 * @param {React.ReactNode} children
 * @param {string}  className - Extra classes
 * @param {object}  props     - Any other props (onClick, type, etc.)
 */
export default function Button({
  variant = "primary",
  size = "md",
  loading = false,
  children,
  className,
  ...props
}) {
  // --- Variant Styles ---
  const variants = {
    primary:
      "bg-gradient-to-r from-primary to-violet text-white shadow-lg shadow-primary/25 hover:shadow-primary/40 hover:brightness-110",
    secondary:
      "bg-surface-light text-foreground border border-border hover:bg-surface-light/80 hover:border-border-light",
    outline:
      "bg-transparent text-foreground border border-border-light hover:bg-white/5",
    ghost:
      "bg-transparent text-muted hover:text-foreground hover:bg-white/5",
  };

  // --- Size Styles ---
  const sizes = {
    sm: "px-4 py-2 text-sm rounded-lg gap-1.5",
    md: "px-6 py-2.5 text-sm rounded-xl gap-2",
    lg: "px-8 py-3 text-base rounded-xl gap-2.5",
  };

  return (
    <motion.button
      whileTap={{ scale: 0.97 }}
      whileHover={{ scale: 1.02 }}
      transition={{ type: "spring", stiffness: 400, damping: 17 }}
      disabled={loading || props.disabled}
      className={cn(
        "inline-flex items-center justify-center font-medium transition-all duration-200 cursor-pointer",
        "disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none",
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    >
      {loading && <Spinner size="sm" />}
      {children}
    </motion.button>
  );
}
