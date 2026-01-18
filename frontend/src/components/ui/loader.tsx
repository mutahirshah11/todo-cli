'use client';

import React from 'react';
import { motion } from 'framer-motion';

export const Loader = () => {
  return (
    <div className="flex items-center justify-center gap-1.5 h-full w-full min-h-[40px]">
      {[0, 1, 2, 3].map((index) => (
        <motion.div
          key={index}
          className="h-8 w-2 bg-primary/80 rounded-full"
          animate={{
            scaleY: [1, 1.5, 1],
            opacity: [0.5, 1, 0.5],
          }}
          transition={{
            duration: 1,
            repeat: Infinity,
            delay: index * 0.15,
            ease: "easeInOut",
          }}
        />
      ))}
    </div>
  );
};

export const LoaderSmall = () => {
  return (
    <div className="flex items-center justify-center gap-1">
      {[0, 1, 2].map((index) => (
        <motion.div
          key={index}
          className="h-1.5 w-1.5 bg-current rounded-full"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.6, 1, 0.6],
          }}
          transition={{
            duration: 0.8,
            repeat: Infinity,
            delay: index * 0.2,
          }}
        />
      ))}
    </div>
  );
};
