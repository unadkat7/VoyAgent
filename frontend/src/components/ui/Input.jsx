"use client";

import React from "react";

export default function Input({
  label,
  id,
  type = "text",
  placeholder,
  value,
  onChange,
  icon: Icon,
  rightElement,
  required = false,
  className = "",
}) {
  return (
    <div className="flex flex-col gap-1.5 w-full">
      {label && (
        <label htmlFor={id} className="text-xs font-medium text-zinc-400">
          {label}
        </label>
      )}
      <div className="relative flex items-center">
        {Icon && (
          <div className="absolute left-3.5 text-zinc-500 pointer-events-none flex items-center justify-center">
            <Icon className="w-4 h-4" />
          </div>
        )}
        <input
          id={id}
          type={type}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          required={required}
          className={`w-full bg-[#121214] border border-white/10 rounded-xl py-3 text-sm text-white placeholder-zinc-500 transition-all duration-200 focus:outline-none focus:border-indigo-500/60 focus:ring-1 focus:ring-indigo-500/30 ${
            Icon ? "pl-10" : "pl-4"
          } ${rightElement ? "pr-11" : "pr-4"} ${className}`}
        />
        {rightElement && (
          <div className="absolute right-3 flex items-center justify-center">
            {rightElement}
          </div>
        )}
      </div>
    </div>
  );
}
