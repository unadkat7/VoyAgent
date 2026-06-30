"use client";

import Link from "next/link";
import { Compass, Sparkles, Globe, Mail, Share2, Heart } from "lucide-react";

/**
 * Premium footer with links, social icons, and newsletter CTA.
 */

const FOOTER_LINKS = {
  Product: [
    { label: "Features", href: "#features" },
    { label: "How it Works", href: "#how-it-works" },
    { label: "Pricing", href: "#" },
    { label: "Demo", href: "#demo" },
  ],
  Company: [
    { label: "About", href: "#" },
    { label: "Blog", href: "#" },
    { label: "Careers", href: "#" },
    { label: "Contact", href: "#" },
  ],
  Legal: [
    { label: "Privacy Policy", href: "#" },
    { label: "Terms of Service", href: "#" },
    { label: "Cookie Policy", href: "#" },
  ],
};

const SOCIAL_LINKS = [
  { icon: Globe, href: "https://github.com", label: "Website" },
  { icon: Mail, href: "mailto:hello@voyagent.ai", label: "Email" },
  { icon: Share2, href: "#", label: "Share" },
];

export default function Footer() {
  return (
    <footer className="border-t border-border bg-surface/40">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* --- Main Grid --- */}
        <div className="py-12 md:py-16 grid grid-cols-2 md:grid-cols-5 gap-8">
          {/* Brand Column */}
          <div className="col-span-2">
            <Link href="/" className="flex items-center gap-2 mb-4">
              <div className="relative">
                <Compass className="h-7 w-7 text-primary" />
                <Sparkles className="absolute -top-1 -right-1 h-3 w-3 text-accent" />
              </div>
              <span className="text-xl font-bold text-gradient">VoyAgent</span>
            </Link>
            <p className="text-sm text-muted max-w-xs leading-relaxed">
              Your AI-powered travel concierge. Plan unforgettable trips with intelligent
              itineraries, smart budgets, and personalized recommendations.
            </p>

            {/* Social Icons */}
            <div className="flex items-center gap-3 mt-6">
              {SOCIAL_LINKS.map((social) => (
                <a
                  key={social.label}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={social.label}
                  className="p-2 rounded-lg text-muted hover:text-foreground hover:bg-white/5 transition-all duration-200"
                >
                  <social.icon className="h-5 w-5" />
                </a>
              ))}
            </div>
          </div>

          {/* Link Columns */}
          {Object.entries(FOOTER_LINKS).map(([category, links]) => (
            <div key={category}>
              <h4 className="text-sm font-semibold text-foreground mb-4">
                {category}
              </h4>
              <ul className="space-y-2.5">
                {links.map((link) => (
                  <li key={link.label}>
                    <a
                      href={link.href}
                      className="text-sm text-muted hover:text-foreground transition-colors duration-200"
                    >
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* --- Bottom Bar --- */}
        <div className="py-6 border-t border-border flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-muted">
            © {new Date().getFullYear()} VoyAgent. All rights reserved.
          </p>
          <p className="text-xs text-muted flex items-center gap-1">
            Built with <Heart className="h-3 w-3 text-red-400 fill-red-400" /> and AI
          </p>
        </div>
      </div>
    </footer>
  );
}
