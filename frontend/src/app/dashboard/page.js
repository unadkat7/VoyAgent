"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import {
  getCurrentUser,
  logout,
} from "@/services/auth.service";

export default function DashboardPage() {
  const router = useRouter();

  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const data = await getCurrentUser();

      setUser(data.user);
    } catch (error) {
      router.replace("/login");
      return;
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await logout();

      router.replace("/login");
    } catch (error) {
      console.log(error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-xl">
        Loading...
      </div>
    );
  }

  // VERY IMPORTANT
  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-black text-white p-10">
      <h1 className="text-4xl font-bold">
        Welcome {user.name} 👋
      </h1>

      <p className="mt-4 text-zinc-400">
        VoyAgent Dashboard
      </p>

      <button
        onClick={handleLogout}
        className="mt-8 bg-red-600 px-4 py-2 rounded-lg"
      >
        Logout
      </button>
    </div>
  );
}