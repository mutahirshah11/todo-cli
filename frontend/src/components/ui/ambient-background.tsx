'use client';

import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { useStore } from '@/lib/store';

export const AmbientBackground = () => {
  const { tasks } = useStore();
  const [moodColor, setMoodColor] = useState('rgba(52, 211, 153, 0.15)'); // Default Green

  useEffect(() => {
    if (tasks.length === 0) {
      setMoodColor('rgba(52, 211, 153, 0.15)'); // Calm Green
      return;
    }

    const uncompleted = tasks.filter(t => !t.is_completed).length;
    const total = tasks.length;
    const ratio = uncompleted / total;

    if (uncompleted === 0) {
       setMoodColor('rgba(59, 130, 246, 0.15)'); // Blue (All Done)
    } else if (ratio > 0.7) {
       setMoodColor('rgba(239, 68, 68, 0.1)'); // Red tint (High workload)
    } else if (ratio > 0.4) {
       setMoodColor('rgba(245, 158, 11, 0.1)'); // Orange tint (Moderate)
    } else {
       setMoodColor('rgba(52, 211, 153, 0.1)'); // Green tint (Good)
    }
  }, [tasks]);

  return (
    <div className="fixed inset-0 z-0 pointer-events-none overflow-hidden">
      <motion.div
        className="absolute top-[-20%] left-[-10%] w-[70vw] h-[70vw] rounded-full blur-[120px] mix-blend-screen"
        animate={{
          backgroundColor: moodColor,
        }}
        transition={{ duration: 2, ease: "easeInOut" }}
      />
      <motion.div
        className="absolute bottom-[-20%] right-[-10%] w-[60vw] h-[60vw] rounded-full blur-[120px] mix-blend-screen opacity-50"
        animate={{
          backgroundColor: moodColor,
        }}
        transition={{ duration: 3, ease: "easeInOut", delay: 0.5 }}
      />
    </div>
  );
};
