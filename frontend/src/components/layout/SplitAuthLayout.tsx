import React from 'react';
import { Sparkles } from 'lucide-react';
import Link from 'next/link';
import { TickwenLogo } from '@/components/ui/tickwen-logo';

interface SplitAuthLayoutProps {
  children: React.ReactNode;
}

export function SplitAuthLayout({ children }: SplitAuthLayoutProps) {
  return (
    <div className="flex min-h-screen w-full bg-[#030712] text-white">
      {/* Left Panel - Product Side / Branding */}
      <div className="hidden w-1/2 flex-col justify-between bg-[#0a0f1c] p-12 lg:flex relative overflow-hidden border-r border-white/5">
        {/* Abstract Background Shapes */}
        <div className="absolute top-0 right-0 h-[500px] w-[500px] translate-x-1/3 -translate-y-1/4 rounded-full bg-primary/10 blur-[120px]" />
        <div className="absolute bottom-0 left-0 h-[500px] w-[500px] -translate-x-1/3 translate-y-1/4 rounded-full bg-blue-600/5 blur-[120px]" />
        
        <div className="relative z-10">
          <Link href="/" className="flex items-center font-bold text-4xl text-white tracking-tighter">
            <TickwenLogo className="h-16 w-16" />
            <span className="mt-1.5 -ml-[18px]">ickwen</span>
          </Link>
        </div>

        <div className="relative z-10 max-w-lg">
          <div className="mb-8 inline-flex items-center rounded-full border border-primary/20 bg-primary/5 px-3 py-1 text-sm font-medium text-primary backdrop-blur-sm">
            <Sparkles className="mr-2 h-3.5 w-3.5 animate-pulse" />
            <span>AI-First Productivity</span>
          </div>
          <h1 className="mb-6 text-4xl font-bold leading-tight tracking-tight lg:text-5xl text-white">
            Focus on what matters,<br />
            let <span className="text-primary">AI</span> handle the rest.
          </h1>
          <p className="text-lg text-gray-400">
            Experience the power of conversational task management. 
            No more endless clicking through forms and menus.
          </p>
        </div>

        <div className="relative z-10 text-sm text-gray-500">
          Trusted by forward-thinking teams everywhere.
        </div>
      </div>

      {/* Right Panel - Auth Forms */}
      <div className="flex w-full flex-col items-center justify-center bg-[#030712] p-8 lg:w-1/2 relative">
        <Link href="/" className="absolute top-8 left-8 text-gray-400 hover:text-white lg:hidden flex items-center gap-2 text-sm font-medium transition-colors">
          ← Back
        </Link>
        <div className="w-full max-w-[400px]">
          {children}
        </div>
      </div>
    </div>
  );
}
