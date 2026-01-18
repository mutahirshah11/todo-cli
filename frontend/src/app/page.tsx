'use client';

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, CheckCircle2, Command, MessageSquare, Sparkles, Zap, Brain, Shield, Rocket, LayoutDashboard } from "lucide-react";
import { motion } from "framer-motion";
import { TickwenLogo } from "@/components/ui/tickwen-logo";
import { useAuthContext } from "@/app/providers/auth-provider";
import { useEffect, useState } from "react";
import { TaskStreamBackground } from "@/components/ui/task-stream-background";
import { IntelligencePipeline } from "@/components/ui/intelligence-pipeline";

const fadeIn = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

export default function Home() {
  const { isAuthenticated, user } = useAuthContext();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div className="flex min-h-screen flex-col bg-[#030712] text-white selection:bg-primary/30 selection:text-primary-foreground overflow-x-hidden relative">
      
      {/* Navbar */}
      <header className="sticky top-0 z-50 w-full border-b border-white/5 bg-[#030712]/80 backdrop-blur-xl">
        <div className="container flex h-16 items-center justify-between px-6">
          <div className="flex items-center font-bold text-2xl tracking-tight">
            <TickwenLogo className="h-10 w-10" />
            <span className="mt-1 -ml-[10px]">ickwen</span>
          </div>
          <nav className="flex items-center gap-6">
            {mounted && isAuthenticated ? (
              <div className="flex items-center gap-4">
                 <div className="hidden md:flex items-center gap-3 text-sm font-medium text-gray-300">
                    <span>Welcome, {user?.name?.split(' ')[0]}</span>
                    <div className="h-8 w-8 rounded-full bg-primary/20 border border-primary/30 flex items-center justify-center text-primary font-bold">
                       {user?.name?.charAt(0)}
                    </div>
                 </div>
                 <Link href="/dashboard">
                   <Button size="sm" className="rounded-full px-6 bg-white text-black hover:bg-gray-200 font-semibold shadow-[0_0_15px_-5px_rgba(255,255,255,0.3)] transition-all">
                     <LayoutDashboard className="mr-2 h-4 w-4" />
                     Dashboard
                   </Button>
                 </Link>
              </div>
            ) : (
              <>
                <Link href="/login" className="text-sm font-medium text-gray-400 transition-colors hover:text-white">
                  Sign In
                </Link>
                <Link href="/register">
                  <Button size="sm" className="rounded-full px-6 bg-primary hover:bg-primary/90 text-black font-semibold shadow-[0_0_20px_-5px_rgba(16,185,129,0.4)] transition-all hover:shadow-[0_0_25px_-5px_rgba(16,185,129,0.6)]">
                    Get Started
                  </Button>
                </Link>
              </>
            )}
          </nav>
        </div>
      </header>

      <main className="flex-1 relative z-10">
        {/* Hero Section */}
        <section className="relative pt-10 pb-40 px-7 min-h-[80vh] flex items-center ">
          <div className="absolute inset-0 z-0 gap-4">
            <TaskStreamBackground />
          </div>
          <div className="container mx-auto text-center max-w-10xl relative z-10 ">
            <motion.div 
              initial="hidden"
              animate="visible"
              variants={staggerContainer}
              className="space-y-8"
            >
              <motion.div variants={fadeIn} className="flex justify-center">
                <div className="inline-flex items-center rounded-full border border-primary/20 bg-primary/5 px-4 py-1.5 text-sm font-medium text-primary backdrop-blur-sm">
                  <Sparkles className="mr-2 h-3.5 w-3.5 animate-pulse" />
                  <span>The Future of Task Management</span>
                </div>
              </motion.div>
              
              <motion.h1 variants={fadeIn} className="mx-auto max-w-4xl text-5xl font-bold tracking-tight md:text-7xl lg:text-8xl leading-[1.1]">
                Task management <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary via-emerald-200 to-primary">
                  reimagined by AI.
                </span>
              </motion.h1>
              
              <motion.p variants={fadeIn} className="mx-auto max-w-2xl text-lg text-gray-400 md:text-xl leading-relaxed">
                Tickwen isn't just a todo list. It's an intelligent system that organizes, prioritizes, and manages your life through simple conversation.
              </motion.p>
              
              <motion.div variants={fadeIn} className="flex flex-col items-center justify-center gap-4 sm:flex-row pt-4">
                <Link href={mounted && isAuthenticated ? "/dashboard" : "/register"}>
                  <Button size="lg" className="h-14 min-w-[200px] rounded-full text-base bg-white text-black hover:bg-gray-100 font-semibold shadow-lg hover:scale-105 transition-all duration-300">
                    {mounted && isAuthenticated ? "Go to Dashboard" : "Start Building Free"} <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              </motion.div>
            </motion.div>
            
          </div>
        </section>

        {/* Intelligence Pipeline (The Core) */}
        <section className="py-24 relative border-t border-white/5 bg-white/[0.02] overflow-hidden">
           {/* Background Glow */}
           <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] bg-primary/5 blur-[120px] rounded-full -z-10" />
           <IntelligencePipeline />
        </section>

        {/* CTA Section */}
        <section className="py-32 relative overflow-hidden">
          <div className="absolute inset-0 bg-primary/5" />
          <div className="container px-6 mx-auto relative z-10 text-center">
            <motion.div
               initial={{ opacity: 0, scale: 0.95 }}
               whileInView={{ opacity: 1, scale: 1 }}
               viewport={{ once: true }}
               transition={{ duration: 0.5 }}
               className="max-w-4xl mx-auto rounded-3xl border border-white/10 bg-[#0a0f1c]/80 backdrop-blur-xl p-12 md:p-20 shadow-2xl"
            >
              <h2 className="mb-6 text-3xl font-bold tracking-tight md:text-5xl text-white">
                Ready to upgrade your workflow?
              </h2>
              <p className="mx-auto mb-10 max-w-2xl text-gray-400 md:text-lg">
                Join thousands of high-performers who trust Tickwen to manage their most important work.
              </p>
              <Link href={mounted && isAuthenticated ? "/dashboard" : "/register"}>
                <Button size="lg" className="h-14 min-w-[200px] rounded-full text-base bg-primary hover:bg-primary/90 text-black font-bold shadow-[0_0_20px_-5px_rgba(16,185,129,0.5)] hover:shadow-[0_0_30px_-5px_rgba(16,185,129,0.7)] transition-all">
                  {mounted && isAuthenticated ? "Go to Dashboard" : "Get Started Now"}
                </Button>
              </Link>
            </motion.div>
          </div>
        </section>
      </main>

      <footer className="border-t border-white/10 bg-[#030712] py-12">
        <div className="container px-6 mx-auto">
          <div className="flex flex-col items-center justify-between gap-6 md:flex-row">
            <div className="flex items-center font-bold text-2xl text-gray-200 tracking-tighter">
              <TickwenLogo className="h-10 w-10" />
              <span className="mt-1 -ml-[10px]">ickwen</span>
            </div>
            <p className="text-sm text-gray-500">
              © {new Date().getFullYear()} Tickwen Inc. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
