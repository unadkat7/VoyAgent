"use client";

import React from "react";
import { motion } from "framer-motion";

export default function Button({
  children,
  type = "button",
  onClick,
  disabled = false,
  loading = false,
  className = "",
}) {
  return (
    <motion.button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      whileTap={disabled || loading ? {} : { scale: 0.98 }}
      className={`w-full flex items-center justify-center gap-2 py-3 px-4 rounded-xl font-medium text-sm text-white transition-all duration-200 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-60 disabled:cursor-not-allowed shadow-lg shadow-indigo-600/20 ${className}`}
    >
      {loading && (
        <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
      )}
      {children}
    </motion.button>
  );
}
