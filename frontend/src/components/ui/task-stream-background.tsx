'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { CheckSquare } from 'lucide-react';

const taskData = [
  { title: "Buy groceries for week", type: "Personal" },
  { title: "Weekly Team Sync @ 10am", type: "Work" },
  { title: "Pay electricity bill", type: "Finance" },
  { title: "Gym: Leg Day", type: "Health" },
  { title: "Dentist Appointment", type: "Health" },
  { title: "Submit Q3 Report", type: "Work" },
  { title: "Call Mom", type: "Personal" },
  { title: "Pay Monthly rent", type: "Finance" },
  { title: "Book flights for vacation", type: "Travel" },
  { title: "Walk the dog", type: "Personal" },
  { title: "Review Project Proposal", type: "Work" },
  { title: "Car Service @ 2pm", type: "Errand" },
  { title: "Buy Birthday Gift", type: "Personal" },
  { title: "Update Resume", type: "Career" },
  { title: "Meditation - 15 mins", type: "Health" },
  { title: "Clean the Garage", type: "Home" },
  { title: "Cancel unused subscription", type: "Finance" },
  { title: "Design Review Meeting", type: "Work" },
  { title: "Water the plants", type: "Home" },
  { title: "Pick up dry cleaning", type: "Errand" },
  { title: "Read 20 pages", type: "Personal" },
  { title: "Schedule annual checkup", type: "Health" },
  { title: "Fix kitchen sink", type: "Home" },
  { title: "Client Presentation", type: "Work" },
  { title: "Transfer savings", type: "Finance" },
  { title: "Clean the Garage", type: "Home" },
  { title: "Cancel unused subscription", type: "Finance" },
  { title: "Design Review Meeting", type: "Work" },
  { title: "Water the plants", type: "Home" },
  { title: "Pick up dry cleaning", type: "Errand" },
  { title: "Read 20 pages", type: "Personal" },
  { title: "Schedule annual checkup", type: "Health" },
  { title: "Fix kitchen sink", type: "Home" },
  { title: "Client Presentation", type: "Work" },
  { title: "Transfer savings", type: "Finance" },
  
];

const FloatingCard = ({ delay, x, duration, scale, taskIndex }: { delay: number, x: string, duration: number, scale: number, taskIndex: number }) => {
  const task = taskData[taskIndex % taskData.length];
  
  return (
    <motion.div
      initial={{ y: "110vh", opacity: 0 }}
      animate={{ y: "-20vh", opacity: [0, 0.40, 0.40, 0] }}
      transition={{ 
        duration: duration, 
        repeat: Infinity, 
        delay: delay,
        ease: 'linear' 
      }}
      className="absolute top-0 w-60 p-4 rounded-xl border border-white/5 bg-[#1e293b]/25 backdrop-blur-md shadow-2xl"
      style={{ 
        left: x,
        scale: scale,
        rotate: Math.random() * 10 - 5,
        zIndex: 1
      }}
    >
      <div className="flex justify-center items-center gap-[5px]">
        <div className="mt-2 m-3 h-5 w-5 rounded border-2 border-primary/50 flex items-center justify-center">
           <CheckSquare className="h-5 w-3 text-primary" />
        </div>
        <div className="flex-1">
          <h4 className="text-sm font-medium text-white/90 leading-tight">{task.title}</h4>
          <div className="flex items-center gap-2 mt-2">
             <span className="text-[10px] px-2 py-0.5 rounded-full bg-white/10 text-white/60 border border-white/5">
               {task.type}
             </span>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export const TaskStreamBackground = () => {
  const [streams, setStreams] = React.useState<Array<{id: number, delay: number, x: string, duration: number, scale: number, taskIndex: number}>>([]);

  React.useEffect(() => {
    // Generate streams only on client side to avoid hydration mismatch
    const count = 22;
    const slots = Array.from({ length: count }, (_, i) => i);
    
    // Shuffle slots for random distribution but even spacing
    for (let i = slots.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [slots[i], slots[j]] = [slots[j], slots[i]];
    }

    const newStreams = slots.map((slot, i) => ({
      id: i,
      delay: Math.random() * -40, // Negative delay to start mid-animation
      // Distribute across 95% of width, using slots to prevent clumping
      // 5% margin on sides, slot width approx 6%
      x: `${2 + (slot * (96 / count)) + (Math.random() * 2)}%`,
      duration: 18 + Math.random() * 12, // Slightly faster: between 18s and 30s
      scale: 0.7 + Math.random() * 0.3,
      taskIndex: Math.floor(Math.random() * taskData.length)
    }));
    setStreams(newStreams);
  }, []);

  if (streams.length === 0) return null;

  return (
    <div className="absolute inset-5 overflow-hidden select-none pointer-events-none">
      {/* Cards Container */}
      <div className="absolute inset-0 m-1">
        {streams.map((s) => (
          <FloatingCard 
            key={s.id} 
            delay={s.delay} 
            x={s.x} 
            duration={s.duration} 
            scale={s.scale}
            taskIndex={s.taskIndex}
          />
        ))}
      </div>
      
      {/* Top fade to handle the "fading above before the navbar" */}
      <div className="absolute top-0 left-0 right-0 h-32 bg-gradient-to-b from-[#030712] to-transparent z-10" />
      
      {/* Bottom fade for smooth entry */}
      <div className="absolute bottom-0 left-0 right-0 h-40 bg-gradient-to-t from-[#030712] via-[#030712]/40 to-transparent z-10" />
      
      {/* Side fades */}
      <div className="absolute inset-y-0 left-0 w-32 bg-gradient-to-r from-[#030712] to-transparent z-10" />
      <div className="absolute inset-y-0 right-0 w-32 bg-gradient-to-l from-[#030712] to-transparent z-10" />
    </div>
  );
};
