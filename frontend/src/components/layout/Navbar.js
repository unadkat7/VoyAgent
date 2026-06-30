"use client";

import { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { Compass, Sparkles, Menu, X } from "lucide-react";
import Button from "@/components/ui/Button";

/**
 * Sticky glassmorphic Navbar with mobile hamburger menu.
 */

const NAV_LINKS = [
  { label: "Features", href: "#features" },
  { label: "How it Works", href: "#how-it-works" },
  { label: "Demo", href: "#demo" },
];

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 glass border-b border-border">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* --- Logo --- */}
          <Link href="/" className="flex items-center gap-2 group">
            <div className="relative">
              <Compass className="h-7 w-7 text-primary transition-transform duration-300 group-hover:rotate-45" />
              <Sparkles className="absolute -top-1 -right-1 h-3 w-3 text-accent" />
            </div>
            <span className="text-xl font-bold text-gradient">VoyAgent</span>
          </Link>

          {/* --- Desktop Links --- */}
          <div className="hidden md:flex items-center gap-8">
            {NAV_LINKS.map((link) => (
              <a
                key={link.label}
                href={link.href}
                className="text-sm text-muted hover:text-foreground transition-colors duration-200"
              >
                {link.label}
              </a>
            ))}
          </div>

          {/* --- Desktop Actions --- */}
          <div className="hidden md:flex items-center gap-3">
            <Button variant="ghost" size="sm">
              Sign In
            </Button>
            <Button variant="primary" size="sm">
              Plan a Trip
            </Button>
          </div>

          {/* --- Mobile Hamburger --- */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden p-2 text-muted hover:text-foreground transition-colors"
            aria-label="Toggle menu"
          >
            {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {/* --- Mobile Menu --- */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.2 }}
            className="md:hidden glass border-t border-border overflow-hidden"
          >
            <div className="px-4 py-4 space-y-3">
              {NAV_LINKS.map((link) => (
                <a
                  key={link.label}
                  href={link.href}
                  onClick={() => setMobileOpen(false)}
                  className="block text-sm text-muted hover:text-foreground transition-colors py-2"
                >
                  {link.label}
                </a>
              ))}
              <div className="pt-3 border-t border-border flex flex-col gap-2">
                <Button variant="ghost" size="sm" className="w-full">
                  Sign In
                </Button>
                <Button variant="primary" size="sm" className="w-full">
                  Plan a Trip
                </Button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}
