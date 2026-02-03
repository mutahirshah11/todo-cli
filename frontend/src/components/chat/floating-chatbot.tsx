"use client";

import { useState } from "react";
import { MessageSquare, X, Bot } from "lucide-react";
import { ChatContainer } from "./chat-container";
import { cn } from "@/lib/utils";

export function FloatingChatbot() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {/* Chat Window */}
      <div
        className={cn(
          "fixed bottom-24 right-6 z-50 mb-0 w-[400px] h-[600px] max-h-[80vh] max-w-[calc(100vw-2rem)] transition-all duration-300 ease-in-out transform origin-bottom-right shadow-2xl rounded-2xl border bg-background overflow-hidden flex flex-col",
          isOpen 
            ? "opacity-100 scale-100 translate-y-0" 
            : "opacity-0 scale-95 translate-y-4 pointer-events-none"
        )}
      >
        <div className="flex items-center justify-between p-4 border-b bg-muted/50">
          <div className="flex items-center gap-2 font-medium">
            <Bot className="w-5 h-5 text-primary" />
            <span>AI Assistant</span>
          </div>
          <button 
            onClick={() => setIsOpen(false)}
            className="p-1 hover:bg-muted rounded-md transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <div className="flex-1 overflow-hidden relative">
          <ChatContainer isFloating />
        </div>
      </div>

      {/* Floating Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={cn(
          "fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full shadow-lg flex items-center justify-center transition-all duration-300 active:scale-95",
          isOpen 
            ? "bg-muted text-foreground rotate-90" 
            : "bg-primary text-primary-foreground hover:scale-110"
        )}
      >
        {isOpen ? (
          <X className="w-6 h-6" />
        ) : (
          <MessageSquare className="w-6 h-6" />
        )}
      </button>
    </>
  );
}
