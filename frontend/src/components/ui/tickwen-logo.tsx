'use client';

import React from 'react';
import Image from 'next/image';
import { cn } from '@/lib/utils';

export const TickwenLogo = ({ className }: { className?: string }) => {
  return (
    <div className={cn("relative flex items-center justify-center h-10 w-10 overflow-hidden", className)}>
      <Image
        src="/Tlogo.png"
        alt="T"
        fill
        className="object-contain"
        priority
      />
    </div>
  );
};

export const TickwenLogoSmall = ({ className }: { className?: string }) => {
  return (
    <div className={cn("relative flex items-center justify-center h-8 w-8 overflow-hidden", className)}>
      <Image
        src="/Tlogo.png"
        alt="T"
        fill
        className="object-contain"
        priority
      />
    </div>
  );
};
