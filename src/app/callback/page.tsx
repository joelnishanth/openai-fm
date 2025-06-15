"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "react-oidc-context";

export default function CallbackPage() {
  const auth = useAuth();
  const router = useRouter();

  useEffect(() => {
    auth
      .signinRedirectCallback()
      .then(() => router.replace("/"))
      .catch(() => router.replace("/login"));
  }, [auth, router]);

  return <div className="min-h-screen flex items-center justify-center">Signing you in...</div>;
}