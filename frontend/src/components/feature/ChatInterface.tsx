import React, { useState, useRef, useEffect } from 'react';
import { Bot, Send, Sparkles, User, StopCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card } from '@/components/ui/card';
import { cn } from '../../lib/utils';
import { useStore } from '../../lib/store';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  isTyping?: boolean;
}

export function ChatInterface({ className }: { className?: string }) {
  const { user } = useStore();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: `Hello ${user?.name || 'there'}! I'm Tickwen AI. 

You can ask me to create tasks, set reminders, or organize your schedule. Just type naturally.`,
      timestamp: new Date(),
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isAiThinking, setIsAiThinking] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isAiThinking]);

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!inputValue.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsAiThinking(true);

    // Simulate AI response
    setTimeout(() => {
      setIsAiThinking(false);
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: "I've noted that down. While I'm currently in 'Visual Preview' mode, I'm designed to parse your request and update your task list automatically.",
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, aiResponse]);
    }, 2000);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className={cn("flex flex-col h-full bg-background rounded-xl border shadow-sm overflow-hidden", className)}>
      {/* Header */}
      <div className="flex items-center px-6 py-4 border-b bg-muted/30">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10 text-primary mr-3">
          <Bot className="h-5 w-5" />
        </div>
        <div>
          <h3 className="font-semibold text-sm">Tickwen Assistant</h3>
          <div className="flex items-center text-xs text-muted-foreground">
            <span className="relative flex h-2 w-2 mr-1.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
            </span>
            Online
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-50/50 dark:bg-transparent">
        {messages.map((message) => (
          <div
            key={message.id}
            className={cn(
              "flex w-full gap-4 max-w-3xl mx-auto",
              message.role === 'user' ? "justify-end" : "justify-start"
            )}
          >
            {message.role === 'assistant' && (
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary border border-primary/20">
                <Bot className="h-4 w-4" />
              </div>
            )}
            
            <div className={cn(
              "relative px-5 py-3.5 text-sm shadow-sm",
              message.role === 'user' 
                ? "bg-primary text-primary-foreground rounded-2xl rounded-tr-sm" 
                : "bg-card border text-card-foreground rounded-2xl rounded-tl-sm"
            )}>
              <div className="whitespace-pre-wrap">{message.content}</div>
              <div className={cn(
                "text-[10px] mt-1 opacity-50",
                message.role === 'user' ? "text-primary-foreground" : "text-muted-foreground"
              )}>
                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>

            {message.role === 'user' && (
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-muted text-muted-foreground border">
                <User className="h-4 w-4" />
              </div>
            )}
          </div>
        ))}

        {isAiThinking && (
          <div className="flex w-full gap-4 max-w-3xl mx-auto justify-start">
             <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary border border-primary/20">
                <Bot className="h-4 w-4" />
              </div>
            <div className="bg-card border px-5 py-4 rounded-2xl rounded-tl-sm shadow-sm flex items-center gap-2">
               <div className="flex space-x-1">
                <div className="w-2 h-2 bg-primary/40 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                <div className="w-2 h-2 bg-primary/40 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                <div className="w-2 h-2 bg-primary/40 rounded-full animate-bounce"></div>
              </div>
              <span className="text-xs text-muted-foreground ml-2">Thinking...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 border-t bg-background">
        <div className="max-w-3xl mx-auto relative flex items-end gap-2 p-2 rounded-xl border bg-muted/30 focus-within:ring-1 focus-within:ring-primary/20 focus-within:border-primary/50 transition-all">
          <Button variant="ghost" size="icon" className="shrink-0 rounded-lg text-muted-foreground hover:text-primary">
            <Sparkles className="h-5 w-5" />
          </Button>
          
          <Textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe a task or ask me anything..."
            className="min-h-[20px] max-h-[120px] border-0 shadow-none bg-transparent resize-none py-3 focus-visible:ring-0"
            rows={1}
          />
          
          <Button 
            onClick={() => handleSubmit()} 
            disabled={!inputValue.trim() || isAiThinking}
            size="icon" 
            className={cn(
              "shrink-0 rounded-lg transition-all",
              inputValue.trim() ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"
            )}
          >
            {isAiThinking ? <StopCircle className="h-5 w-5" /> : <Send className="h-5 w-5" />}
          </Button>
        </div>
        <div className="text-center mt-2">
          <span className="text-[10px] text-muted-foreground">
            Tickwen AI can make mistakes. Please verify important tasks.
          </span>
        </div>
      </div>
    </div>
  );
}
