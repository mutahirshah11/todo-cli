"use client";

import { useState } from "react";
import { ChatKit, useChatKit } from "@openai/chatkit-react";
import { toast } from "sonner";
import { cn } from "@/lib/utils";
import { Loader2 } from "lucide-react";

export function ChatContainer({ isFloating }: { isFloating?: boolean }) {
  const [isReady, setIsReady] = useState(false);

  const { control } = useChatKit({
    api: {
      getClientSecret: async () => {
        try {
          const res = await fetch("/api/chat/session", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
          });

          if (!res.ok) {
            throw new Error(`Session creation failed: ${res.statusText}`);
          }

          const { client_secret } = await res.json();
          // Debug log
          console.log("Client secret received:", client_secret ? "Yes" : "No");
          return client_secret;
        } catch (error) {
          console.error("Failed to get client secret", error);
          toast.error("Failed to initialize chat session");
          throw error;
        }
      },
    },
    onReady: () => {
      console.log("ChatKit is ready");
      setIsReady(true);
    },
    onError: ({ error }) => {
      console.error("ChatKit error:", error);
      toast.error(error.message || "An error occurred in the chat");
    },
  });

  return (
    <div className={cn(
      "w-full h-full bg-background relative",
      !isFloating && "border rounded-xl shadow-sm p-4 max-w-4xl mx-auto"
    )}>
      {!isReady && (
        <div className="absolute inset-0 flex items-center justify-center bg-background/80 z-10">
          <div className="flex flex-col items-center gap-2 text-muted-foreground">
            <Loader2 className="h-6 w-6 animate-spin" />
            <span className="text-sm">Initializing ChatKit...</span>
          </div>
        </div>
      )}
      
      {/* 
        NOTE: ChatKit might be invisible without a valid session. 
        If you see this message below the spinner, ChatKit is mounted.
      */}
      <ChatKit 
        control={control} 
        className="h-full w-full"
      />
    </div>
  );
}
