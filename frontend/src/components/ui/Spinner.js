"use client";

import { cn } from "@/lib/utils";

/**
 * Loading Spinner component.
 *
 * @param {string} size - "sm" | "md" | "lg" (default: "md")
 * @param {string} className - Extra classes to apply
 */
export default function Spinner({ size = "md", className }) {
  const sizes = {
    sm: "h-4 w-4 border-2",
    md: "h-8 w-8 border-[3px]",
    lg: "h-12 w-12 border-4",
  };

  return (
    <div
      className={cn(
        "animate-spin rounded-full border-primary/30 border-t-primary",
        sizes[size],
        className
      )}
      role="status"
      aria-label="Loading"
    >
      <span className="sr-only">Loading...</span>
    </div>
  );
}
