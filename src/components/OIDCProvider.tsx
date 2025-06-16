"use client";

import { AuthProvider } from "react-oidc-context";
import { ReactNode } from "react";

const baseUrl = typeof window !== "undefined" ? window.location.origin : "";

const oidcConfig = {
  authority:
    `https://cognito-idp.${process.env.NEXT_PUBLIC_COGNITO_REGION}.amazonaws.com/${process.env.NEXT_PUBLIC_COGNITO_USER_POOL_ID}`,
  client_id: process.env.NEXT_PUBLIC_COGNITO_CLIENT_ID!,
  redirect_uri: baseUrl + "/callback",
  post_logout_redirect_uri: baseUrl + "/signout",
  response_type: "code",
  scope: "openid email phone",
};

export function OIDCProvider({ children }: { children: ReactNode }) {
  return <AuthProvider {...oidcConfig}>{children}</AuthProvider>;
}
