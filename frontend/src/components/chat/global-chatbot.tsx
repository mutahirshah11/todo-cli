"use client";

import { useAuthContext } from "@/app/providers/auth-provider";
import { FloatingChatbot } from "./floating-chatbot";

export function GlobalChatbot() {
  const { isAuthenticated } = useAuthContext();

  if (!isAuthenticated) {
    return null;
  }

  return <FloatingChatbot />;
}
