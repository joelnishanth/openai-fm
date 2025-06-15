"use client";

import { AuthProvider } from "react-oidc-context";
import { ReactNode } from "react";

const oidcConfig = {
  authority:
    "https://cognito-idp.us-west-2.amazonaws.com/us-west-2_2fafEaDIB",
  client_id: "1rdijil48c7vq90gjofs9r9n74",
  redirect_uri: "http://localhost:3000/callback",
  response_type: "code",
  scope: "email openid phone",
  post_logout_redirect_uri: "http://localhost:3000/signout",
};

export function OIDCProvider({ children }: { children: ReactNode }) {
  return <AuthProvider {...oidcConfig}>{children}</AuthProvider>;
}
