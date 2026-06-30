"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Sparkles,
  User,
  Mail,
  Lock,
  Eye,
  EyeOff,
} from "lucide-react";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";

import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { signup } from "@/services/auth.service";

export default function SignupPage() {
  const router = useRouter();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] =
    useState(false);

  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!name || !email || !password || !confirmPassword) {
      return toast.error("Please fill all fields");
    }

    if (password !== confirmPassword) {
      return toast.error("Passwords do not match");
    }

    try {
      setLoading(true);

      const data = await signup({
        name,
        email,
        password,
      });

      toast.success(data.message);

      router.push("/login");
    } catch (error) {
      toast.error(
        error.response?.data?.message ||
          "Something went wrong"
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
      <div className="w-full max-w-md bg-[#121216]/80 border border-white/10 rounded-3xl p-6 sm:p-8 backdrop-blur-xl shadow-2xl relative z-10 flex flex-col gap-6 my-8">

        {/* Header */}
        <div className="flex flex-col items-center text-center gap-2">
          <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-1">
            <Sparkles className="w-6 h-6" />
          </div>

          <h1 className="text-xl font-semibold tracking-tight">
            VoyAgent
          </h1>

          <h2 className="text-2xl sm:text-3xl font-bold">
            Create an Account
          </h2>

          <p className="text-sm text-zinc-400">
            Get started with AI-powered travel planning.
          </p>
        </div>

        {/* Form */}
        <form
          onSubmit={handleSubmit}
          className="flex flex-col gap-4 mt-2"
        >
          <Input
            label="Full Name"
            id="name"
            type="text"
            placeholder="John Doe"
            value={name}
            onChange={(e) => setName(e.target.value)}
            icon={User}
            required
          />

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

          <Input
            label="Confirm Password"
            id="confirmPassword"
            type={
              showConfirmPassword ? "text" : "password"
            }
            placeholder="••••••••"
            value={confirmPassword}
            onChange={(e) =>
              setConfirmPassword(e.target.value)
            }
            icon={Lock}
            required
            rightElement={
              <button
                type="button"
                onClick={() =>
                  setShowConfirmPassword(
                    !showConfirmPassword
                  )
                }
                className="text-zinc-500 hover:text-zinc-300"
              >
                {showConfirmPassword ? (
                  <EyeOff size={18} />
                ) : (
                  <Eye size={18} />
                )}
              </button>
            }
          />

          <Button
            type="submit"
            loading={loading}
            disabled={loading}
            className="mt-3"
          >
            {loading
              ? "Creating Account..."
              : "Create Account"}
          </Button>
        </form>

        {/* Footer */}
        <div className="border-t border-white/5 pt-6 text-center text-sm text-zinc-400">
          Already have an account?{" "}
          <Link
            href="/login"
            className="text-white font-medium hover:underline"
          >
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}