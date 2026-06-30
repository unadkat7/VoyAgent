"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

/**
 * Reusable Section component for page layouts.
 * Provides consistent spacing, optional badge, title, and subtitle.
 *
 * @param {string}  badge     - Small label above the title (e.g. "AI POWERED")
 * @param {string}  title     - Main heading text
 * @param {string}  subtitle  - Description below the title
 * @param {boolean} centered  - Center-align text (default: true)
 * @param {React.ReactNode} children - Section content
 * @param {string}  className - Extra classes
 */
export default function Section({
  badge,
  title,
  subtitle,
  centered = true,
  children,
  className,
  id,
}) {
  return (
    <section
      id={id}
      className={cn("py-20 md:py-28 px-4 sm:px-6 lg:px-8", className)}
    >
      <div className="max-w-6xl mx-auto">
        {/* Section Header */}
        {(badge || title || subtitle) && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.5 }}
            className={cn("mb-12 md:mb-16", centered && "text-center")}
          >
            {/* Badge */}
            {badge && (
              <span className="inline-block px-4 py-1.5 text-xs font-semibold tracking-widest uppercase rounded-full bg-primary/10 text-primary-light border border-primary/20 mb-4">
                {badge}
              </span>
            )}

            {/* Title */}
            {title && (
              <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold tracking-tight text-gradient">
                {title}
              </h2>
            )}

            {/* Subtitle */}
            {subtitle && (
              <p className={cn("mt-4 text-lg text-muted max-w-2xl", centered && "mx-auto")}>
                {subtitle}
              </p>
            )}
          </motion.div>
        )}

        {/* Section Body */}
        {children}
      </div>
    </section>
  );
}
