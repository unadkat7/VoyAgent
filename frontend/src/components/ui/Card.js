"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

/**
 * Glassmorphic Card component with composable sub-components.
 *
 * Usage:
 *   <Card>
 *     <CardHeader>
 *       <CardTitle>Title</CardTitle>
 *       <CardDescription>Subtitle</CardDescription>
 *     </CardHeader>
 *     <CardContent>...</CardContent>
 *     <CardFooter>...</CardFooter>
 *   </Card>
 */

// --- Main Card Wrapper ---
export function Card({ children, className, hover = true, ...props }) {
  return (
    <motion.div
      whileHover={hover ? { y: -4, scale: 1.01 } : {}}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
      className={cn(
        "rounded-2xl border border-border bg-surface/60 backdrop-blur-sm",
        "shadow-lg shadow-black/20",
        hover && "transition-shadow duration-300 hover:shadow-xl hover:shadow-primary/10 hover:border-border-light",
        className
      )}
      {...props}
    >
      {children}
    </motion.div>
  );
}

// --- Card Header ---
export function CardHeader({ children, className }) {
  return (
    <div className={cn("p-6 pb-2", className)}>
      {children}
    </div>
  );
}

// --- Card Title ---
export function CardTitle({ children, className }) {
  return (
    <h3 className={cn("text-lg font-semibold text-foreground", className)}>
      {children}
    </h3>
  );
}

// --- Card Description ---
export function CardDescription({ children, className }) {
  return (
    <p className={cn("text-sm text-muted mt-1", className)}>
      {children}
    </p>
  );
}

// --- Card Content ---
export function CardContent({ children, className }) {
  return (
    <div className={cn("p-6 pt-2", className)}>
      {children}
    </div>
  );
}

// --- Card Footer ---
export function CardFooter({ children, className }) {
  return (
    <div className={cn("p-6 pt-0 flex items-center gap-3", className)}>
      {children}
    </div>
  );
}
