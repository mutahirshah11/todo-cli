'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Calendar, ArrowRight, CheckCircle2, Zap, Clock, Target, Mic } from 'lucide-react';
import { cn } from '@/lib/utils';

const Waveform = () => (
  <div className="flex items-end gap-[2px] h-4">
    {[1, 2, 3, 4, 5, 4, 3, 2, 1].map((h, i) => (
      <motion.div
        key={i}
        animate={{ height: [4, h * 3, 4] }}
        transition={{ duration: 1, repeat: Infinity, delay: i * 0.1 }}
        className="w-[2px] bg-blue-400/60 rounded-full"
      />
    ))}
  </div>
);

const fullText = "Hey Tickwen, remind me to sync with the design team about the new dashboard assets this Friday at 3pm.";

export const IntelligencePipeline = () => {
  const [displayText, setDisplayText] = useState("");
  const [isTypingDone, setIsTypingDone] = useState(false);
  const [startAnimation, setStartAnimation] = useState(false);

  useEffect(() => {
    if (!startAnimation) return;

    let i = 0;
    const interval = setInterval(() => {
      setDisplayText(fullText.slice(0, i));
      i++;
      if (i > fullText.length) {
        clearInterval(interval);
        setTimeout(() => setIsTypingDone(true), 500);
      }
    }, 30);

    return () => clearInterval(interval);
  }, [startAnimation]);

  return (
    <div className="w-full max-w-7xl mx-auto py-32 px-4 md:px-6 relative overflow-hidden">
      {/* Background Depth */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[500px] bg-primary/5 blur-[140px] rounded-full -z-10" />
      
      <motion.div 
        onViewportEnter={() => setStartAnimation(true)}
        className="text-center mb-24 relative z-10"
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-[10px] font-bold tracking-[0.2em] text-gray-400 uppercase mb-4"
        >
          <Zap className="w-3 h-3 text-primary" />
          The Process
        </motion.div>
        <h2 className="text-4xl font-bold tracking-tight md:text-6xl mb-6 text-white">
          Natural Intelligence
        </h2>
        <p className="text-gray-400 text-lg max-w-2xl mx-auto">
          From voice command to scheduled event in milliseconds. Experience the future of task management.
        </p>
      </motion.div>

      <div className="flex flex-col lg:flex-row items-center justify-center gap-12 lg:gap-8 relative z-10 min-h-[400px]">
        
        {/* Stage 1: The Input (Natural Language) */}
        <div className="flex flex-col items-center gap-6 w-full max-w-[340px]">
          <div className="flex items-center gap-3 text-xs font-mono text-gray-500 uppercase tracking-widest">
            <span className="w-8 h-[1px] bg-gray-800" />
            01. Capturing
            <span className="w-8 h-[1px] bg-gray-800" />
          </div>
          
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ type: "spring", damping: 20 }}
            viewport={{ once: true }}
            className="w-full bg-[#111827]/80 backdrop-blur-xl rounded-3xl p-6 border border-white/10 shadow-2xl relative min-h-[160px]"
          >
            <div className="flex items-start gap-4">
               <div className="relative shrink-0">
                  <div className="h-10 w-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-xs font-bold text-white shadow-lg shadow-blue-500/20">
                    JD
                  </div>
                  <div className="absolute -bottom-1 -right-1 h-4 w-4 rounded-full bg-[#111827] border border-white/10 flex items-center justify-center">
                    <Mic className="w-2 h-2 text-red-400" />
                  </div>
               </div>
               <div className="flex-1 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold text-gray-500 uppercase tracking-tighter">Voice Input</span>
                    <Waveform />
                  </div>
                  <p className="text-base text-gray-200 leading-relaxed font-medium min-h-[3.5em]">
                    "{displayText}<span className={cn("inline-block w-[2px] h-[1.2em] bg-primary ml-1 -mb-1", isTypingDone ? "hidden" : "animate-pulse")}>|</span>"
                  </p>
               </div>
            </div>
          </motion.div>
        </div>

        {/* Connector 1 */}
        <div className="hidden lg:flex items-center opacity-20">
          <ArrowRight className="w-6 h-6 text-white" />
        </div>

        {/* Stage 2: The Logic (Understanding) */}
        <div className="flex flex-col items-center gap-6 w-full max-w-[340px]">
          <div className="flex items-center gap-3 text-xs font-mono text-gray-500 uppercase tracking-widest">
            <span className="w-8 h-[1px] bg-gray-800" />
            02. Extracting
            <span className="w-8 h-[1px] bg-gray-800" />
          </div>
          
          <AnimatePresence>
            {isTypingDone && (
              <motion.div 
                 initial={{ opacity: 0, scale: 0.95, y: 10 }}
                 animate={{ opacity: 1, scale: 1, y: 0 }}
                 exit={{ opacity: 0, scale: 0.95 }}
                 transition={{ type: "spring", damping: 20 }}
                 className="w-full bg-[#0a0f1c]/60 backdrop-blur-xl rounded-3xl p-6 border border-white/10 shadow-2xl space-y-4"
              >
                 <div className="space-y-4">
                    <div className="relative group">
                       <div className="flex items-center gap-3 mb-1">
                          <Zap className="w-3 h-3 text-primary" />
                          <span className="text-[10px] text-primary/80 font-bold uppercase tracking-widest">Intent</span>
                       </div>
                       <motion.div 
                        initial={{ width: 0 }} animate={{ width: "100%" }}
                        className="text-green-100 bg-primary/5 border border-primary/20 rounded-xl px-3 py-2 text-sm text-primary-foreground font-medium flex items-center justify-between overflow-hidden whitespace-nowrap"
                       >
                          Create Reminder
                          <CheckCircle2 className="w-3 h-3 text-primary opacity-50" />
                       </motion.div>
                    </div>

                    <div className="relative group ml-4">
                       <div className="flex items-center gap-3 mb-1">
                          <Target className="w-3 h-3 text-blue-400" />
                          <span className="text-[10px] text-blue-400/80 font-bold uppercase tracking-widest">Entity</span>
                       </div>
                       <motion.div 
                        initial={{ width: 0 }} animate={{ width: "100%" }} transition={{ delay: 0.2 }}
                        className="bg-blue-400/5 border border-blue-400/20 rounded-xl px-3 py-2 text-sm text-blue-100 font-medium overflow-hidden whitespace-nowrap"
                       >
                          Design Sync (Assets)
                       </motion.div>
                    </div>

                    <div className="relative group ml-8">
                       <div className="flex items-center gap-3 mb-1">
                          <Clock className="w-3 h-3 text-purple-400" />
                          <span className="text-[10px] text-purple-400/80 font-bold uppercase tracking-widest">Schedule</span>
                       </div>
                       <motion.div 
                        initial={{ width: 0 }} animate={{ width: "100%" }} transition={{ delay: 0.4 }}
                        className="bg-purple-400/5 border border-purple-400/20 rounded-xl px-3 py-2 text-sm text-purple-100 font-medium overflow-hidden whitespace-nowrap"
                       >
                          Friday, 3:00 PM
                       </motion.div>
                    </div>
                 </div>
              </motion.div>
            )}
          </AnimatePresence>
          {!isTypingDone && <div className="h-[236px] w-full border border-dashed border-white/5 rounded-3xl flex items-center justify-center text-[10px] text-gray-700 font-mono">WAITING_FOR_INPUT...</div>}
        </div>

        {/* Connector 2 */}
        <div className="hidden lg:flex items-center opacity-20">
          <ArrowRight className="w-6 h-6 text-white" />
        </div>

        {/* Stage 3: The Result (Action) */}
        <div className="flex flex-col items-center gap-6 w-full max-w-[340px]">
          <div className="flex items-center gap-3 text-xs font-mono text-gray-500 uppercase tracking-widest">
            <span className="w-8 h-[1px] bg-gray-800" />
            03. Executing
            <span className="w-8 h-[1px] bg-gray-800" />
          </div>
          
          <AnimatePresence>
            {isTypingDone && (
              <motion.div 
                 initial={{ opacity: 0, x: 20 }}
                 animate={{ opacity: 1, x: 0 }}
                 transition={{ type: "spring", damping: 20, delay: 0.6 }}
                 className="w-full relative group"
              >
                 <div className="absolute -inset-1 bg-gradient-to-r from-primary/20 via-blue-500/20 to-purple-500/20 rounded-[2rem] blur-xl opacity-50 group-hover:opacity-100 transition duration-1000" />
                 <div className="relative bg-[#0f172a] rounded-[2rem] border border-white/10 overflow-hidden shadow-2xl">
                    <div className="h-1.5 w-full bg-gradient-to-r from-primary via-blue-500 to-purple-500" />
                    <div className="p-7">
                       <div className="flex items-start justify-between mb-6">
                          <div className="flex items-center gap-4">
                             <div className="h-12 w-12 rounded-2xl bg-white/5 flex items-center justify-center border border-white/10 shadow-inner">
                                <Calendar className="h-6 w-6 text-white" />
                             </div>
                             <div>
                                <h4 className="text-base font-bold text-white tracking-tight">Design Sync</h4>
                                <p className="text-xs text-gray-400">Dashboard Assets</p>
                             </div>
                          </div>
                          <div className="h-2 w-2 rounded-full bg-primary shadow-[0_0_12px_rgba(16,185,129,0.8)] animate-pulse" />
                       </div>

                       <div className="bg-white/[0.03] rounded-2xl p-4 flex items-center gap-4 border border-white/5 mb-6">
                          <div className="flex flex-col items-center justify-center px-3 border-r border-white/10">
                             <span className="text-[10px] text-primary font-bold uppercase tracking-widest">Fri</span>
                             <span className="text-xl font-black text-white">27</span>
                          </div>
                          <div className="flex flex-col">
                             <span className="text-sm font-semibold text-gray-200">03:00 PM</span>
                             <span className="text-[10px] text-gray-500 font-medium">Auto-confirmed</span>
                          </div>
                       </div>
                       
                       <div className="flex items-center justify-between">
                          <div className="flex -space-x-2">
                             {[1, 2].map((i) => (
                               <div key={i} className="h-6 w-6 rounded-full border-2 border-[#0f172a] bg-gray-800" />
                             ))}
                             <div className="h-6 w-6 rounded-full border-2 border-[#0f172a] bg-primary/10 flex items-center justify-center text-[8px] font-bold text-primary">+1</div>
                          </div>
                          <span className="text-[10px] bg-primary/10 text-primary px-3 py-1 rounded-full border border-primary/20 font-bold uppercase tracking-wider">
                            Scheduled
                          </span>
                       </div>
                    </div>
                 </div>
              </motion.div>
            )}
          </AnimatePresence>
          {!isTypingDone && <div className="h-[250px] w-full border border-dashed border-white/5 rounded-[2rem] flex items-center justify-center text-[10px] text-gray-700 font-mono">IDLE...</div>}
        </div>

      </div>
    </div>
  );
};
