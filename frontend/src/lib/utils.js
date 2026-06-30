/**
 * Utility function to combine CSS class names.
 * Filters out falsy values (null, undefined, false, "").
 *
 * Usage: cn("base-class", isActive && "active-class", "another-class")
 */
export function cn(...classes) {
  return classes.filter(Boolean).join(" ");
}
