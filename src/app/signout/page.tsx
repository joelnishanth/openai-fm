"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "react-oidc-context";

export default function SignOutPage() {
  const auth = useAuth();
  const router = useRouter();

  useEffect(() => {
    auth
      .signoutRedirectCallback()
      .catch(() => {})
      .finally(() => {
        router.replace("/login");
      });
  }, [auth, router]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      Signing you out...
    </div>
  );
}
