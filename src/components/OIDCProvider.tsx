"use client";

import { AuthProvider } from "react-oidc-context";
import { ReactNode } from "react";

const baseUrl = typeof window !== "undefined" ? window.location.origin : "";

const oidcConfig = {
  authority:
  response_type: "code",
  scope: "email openid phone",
  post_logout_redirect_uri: "http://localhost:3000/signout",
};

export function OIDCProvider({ children }: { children: ReactNode }) {
  return <AuthProvider {...oidcConfig}>{children}</AuthProvider>;
}
