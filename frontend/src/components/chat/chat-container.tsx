"use client";

import { useState, useRef, useEffect } from "react";
import { toast } from "sonner";
import { cn } from "@/lib/utils";
import { Loader2, Send, User, Bot, Sparkles } from "lucide-react";
import { useAuthContext } from "@/app/providers/auth-provider";
import { useStore } from "@/lib/store";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export function ChatContainer({ isFloating }: { isFloating?: boolean }) {
  const { user, isAuthenticated } = useAuthContext();
  const { fetchTasks } = useStore();
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "Hello! I'm your AI Task Assistant. I can help you add, remove, and manage your tasks. Just ask me!" }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;
    
    // Safety check: Don't allow guest chat if we want sync
    if (!user?.id) {
      toast.error("Please login to sync your tasks with the AI.");
      return;
    }

    const userMessage = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setIsLoading(true);

    try {
      console.log(`[Chat] Sending message for user: ${user.id}`);
      
      const headers: Record<string, string> = {
        "Content-Type": "application/json"
      };
      
      // Add token if available (it should be, due to the check above)
      const token = localStorage.getItem('auth_token'); // Or get from context if available
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }

      const res = await fetch("/api/chat/message", {
        method: "POST",
        headers,
        body: JSON.stringify({ 
          message: userMessage, 
          history: messages.slice(-5),
          user_id: user.id // Keeping this for now as fallback, but backend will prefer token
        }),
      });

      if (!res.ok) throw new Error("Backend connection failed");

      const data = await res.json();
      setMessages((prev) => [...prev, { role: "assistant", content: data.response }]);
      
      // Refresh tasks after AI action to sync dashboard
      fetchTasks();
    } catch (error) {
      console.error("Chat error:", error);
      toast.error("AI is busy right now");
      setMessages((prev) => [...prev, { role: "assistant", content: "I'm having trouble connecting to my brain. Please make sure the backend server is running." }]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="flex flex-col items-center justify-center h-full p-8 text-center space-y-4">
        <Bot size={48} className="text-muted-foreground opacity-20" />
        <p className="text-sm text-muted-foreground">Please sign in to talk to your AI Assistant.</p>
      </div>
    );
  }

  return (
    <div className={cn(
      "flex flex-col w-full h-full bg-background",
      !isFloating && "border rounded-xl shadow-sm max-w-4xl mx-auto h-[600px]"
    )}>
      {/* Messages */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-4 space-y-6 scroll-smooth"
      >
        {messages.map((msg, i) => (
          <div key={i} className={cn(
            "flex items-start gap-3 animate-in fade-in slide-in-from-bottom-1 duration-300",
            msg.role === "user" ? "flex-row-reverse" : "flex-row"
          )}>
            <div className={cn(
              "w-8 h-8 rounded-full flex items-center justify-center shrink-0 border shadow-sm",
              msg.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted text-primary"
            )}>
              {msg.role === "user" ? <User size={14} /> : <Bot size={14} />}
            </div>
            <div className={cn(
              "max-w-[80%] p-3 rounded-2xl text-sm leading-relaxed shadow-sm transition-all",
              msg.role === "user" 
                ? "bg-primary text-primary-foreground rounded-tr-none" 
                : "bg-muted/50 text-foreground border border-border/50 rounded-tl-none"
            )}>
              {msg.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex items-start gap-3 animate-in fade-in slide-in-from-bottom-2">
            <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center border shadow-sm">
              <Sparkles size={14} className="text-primary animate-pulse" />
            </div>
            <div className="bg-muted/30 p-3 rounded-2xl rounded-tl-none border border-dashed flex items-center gap-3">
              <Loader2 size={14} className="animate-spin text-muted-foreground" />
              <span className="text-[10px] uppercase tracking-widest font-bold text-muted-foreground">Thinking</span>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-4 border-t bg-muted/10">
        <div className="relative group">
          <input
            className="w-full bg-background border border-border/60 rounded-xl py-3 px-4 pr-12 text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary/50 transition-all shadow-sm group-hover:border-border"
            placeholder="Type your command..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-primary hover:bg-primary/10 rounded-lg transition-all disabled:opacity-30"
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
