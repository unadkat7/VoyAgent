"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Sparkles, Mail, Lock, Eye, EyeOff } from "lucide-react";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";

import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { login } from "@/services/auth.service";

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email || !password) {
      return toast.error("Please fill all fields");
    }

    try {
      setLoading(true);

      const data = await login({
        email,
        password,
      });

      toast.success(data.message);

      router.push("/dashboard");
    } catch (error) {
      toast.error(
        error.response?.data?.message || "Something went wrong"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0c] text-white flex flex-col justify-center items-center p-4 sm:p-6 relative overflow-hidden">
      {/* Background */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-indigo-600/10 rounded-full blur-[120px] pointer-events-none" />

      {/* Card */}
      <div className="w-full max-w-md bg-[#121216]/80 border border-white/10 rounded-3xl p-6 sm:p-8 backdrop-blur-xl shadow-2xl relative z-10 flex flex-col gap-6">

        {/* Header */}
        <div className="flex flex-col items-center text-center gap-2">
          <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-1">
            <Sparkles className="w-6 h-6" />
          </div>

          <h1 className="text-xl font-semibold tracking-tight text-white">
            VoyAgent
          </h1>

          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight">
            Welcome Back
          </h2>

          <p className="text-sm text-zinc-400">
            Sign in to continue planning your next adventure.
          </p>
        </div>

        {/* Form */}
        <form
          onSubmit={handleSubmit}
          className="flex flex-col gap-4 mt-2"
        >
          <Input
            label="Email"
            id="email"
            type="email"
            placeholder="name@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            icon={Mail}
            required
          />

          <Input
            label="Password"
            id="password"
            type={showPassword ? "text" : "password"}
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            icon={Lock}
            required
            rightElement={
              <button
                type="button"
                onClick={() =>
                  setShowPassword(!showPassword)
                }
                className="text-zinc-500 hover:text-zinc-300"
              >
                {showPassword ? (
                  <EyeOff size={18} />
                ) : (
                  <Eye size={18} />
                )}
              </button>
            }
          />

          <div className="flex justify-end">
            <button
              type="button"
              className="text-sm text-indigo-400 hover:text-indigo-300"
            >
              Forgot Password?
            </button>
          </div>

          <Button
            type="submit"
            loading={loading}
            disabled={loading}
            className="mt-2"
          >
            {loading ? "Logging in..." : "Login"}
          </Button>
        </form>

        {/* Footer */}
        <div className="border-t border-white/5 pt-6 text-center text-sm text-zinc-400">
          Don't have an account?{" "}
          <Link
            href="/signup"
            className="text-white font-medium hover:underline"
          >
            Sign Up
          </Link>
        </div>
      </div>
    </div>
  );
}