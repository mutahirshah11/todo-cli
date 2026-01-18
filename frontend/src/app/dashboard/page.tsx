'use client';

import React, { useEffect, useState } from 'react';
import { useStore } from '@/lib/store';
import { TaskList } from '@/components/feature/TaskList';
import { DeleteConfirmationModal } from '@/components/feature/DeleteConfirmationModal';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Plus, LayoutDashboard, LogOut, Menu, ListTodo, Search, Bell, Zap, X } from 'lucide-react';
import Link from 'next/link';
import { useAuthContext } from '@/app/providers/auth-provider';
import { Loader } from '@/components/ui/loader';
import { motion, AnimatePresence } from 'framer-motion';
import { AmbientBackground } from '@/components/ui/ambient-background';
import { cn } from '@/lib/utils';
import { TaskItem } from '@/components/feature/TaskItem';
import { TickwenLogo } from '@/components/ui/tickwen-logo';

export default function DashboardPage() {
  const {
    tasks,
    isLoading,
    error,
    filterQuery,
    setFilterQuery,
    fetchTasks,
    toggleTask,
    deleteTask,
    isAuthenticated,
    user
  } = useStore();
  
  const { logout } = useAuthContext();
  const [selectedTaskId, setSelectedTaskId] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isFocusMode, setIsFocusMode] = useState(false);

  useEffect(() => {
    if (isAuthenticated()) {
      fetchTasks();
    }
  }, []);

  const handleDeleteClick = (taskId: string, taskTitle: string) => {
    setSelectedTaskId(taskId);
    setIsModalOpen(true);
  };

  const handleConfirmDelete = () => {
    if (selectedTaskId) {
      deleteTask(selectedTaskId);
      setIsModalOpen(false);
      setSelectedTaskId(null);
    }
  };

  if (!isAuthenticated()) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loader />
      </div>
    );
  }

  // Calculate stats
  const completedTasks = tasks.filter(t => t.is_completed).length;
  const totalTasks = tasks.length;
  const progress = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;
  
  // Focus Mode Task (First uncompleted)
  const focusTask = tasks.find(t => !t.is_completed);

  return (
    <div className="flex h-screen bg-transparent overflow-hidden text-foreground relative">
      <AmbientBackground />
      
      {/* Focus Mode Overlay */}
      <AnimatePresence>
        {isFocusMode && focusTask && (
          <motion.div 
            initial={{ opacity: 0, backdropFilter: "blur(0px)" }}
            animate={{ opacity: 1, backdropFilter: "blur(12px)" }}
            exit={{ opacity: 0, backdropFilter: "blur(0px)" }}
            className="fixed inset-0 z-[60] bg-black/80 flex flex-col items-center justify-center p-6"
          >
            <Button 
              variant="ghost" 
              className="absolute top-6 right-6 text-white/50 hover:text-white"
              onClick={() => setIsFocusMode(false)}
            >
              <X className="mr-2 h-4 w-4" /> Exit Focus
            </Button>
            
            <motion.div 
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.1 }}
              className="w-full max-w-2xl"
            >
              <h2 className="text-center text-primary font-medium mb-8 tracking-widest uppercase text-sm">Current Objective</h2>
              <div className="transform scale-125 origin-center">
                 <TaskItem 
                   task={focusTask} 
                   onToggle={(id) => {
                     toggleTask(id);
                     // Optional: Delay exit to show completion
                     setTimeout(() => setIsFocusMode(false), 500);
                   }}
                   onDelete={deleteTask}
                 />
              </div>
              <p className="text-center text-gray-500 mt-12 text-sm">
                "Concentrate all your thoughts upon the work at hand."
              </p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Sidebar Navigation - Desktop */}
      <aside className="hidden w-64 flex-col border-r border-white/5 bg-[#0a0f1c]/50 md:flex backdrop-blur-xl relative z-10">
        <div className="flex h-16 items-center border-b border-white/5 px-6">
          <Link href="/" className="flex items-center hover:opacity-80 transition-opacity">
            <TickwenLogo className="h-9 w-9" />
            <span className="font-bold text-xl tracking-tight text-white mt-1 -ml-[10px]">ickwen</span>
          </Link>
        </div>
        
        <div className="flex-1 overflow-y-auto py-6">
          <nav className="space-y-1 px-3">
            <Button variant="secondary" className="w-full justify-start font-medium text-primary bg-primary/10 hover:bg-primary/20 transition-all border border-primary/10">
              <LayoutDashboard className="mr-2 h-4 w-4" />
              Dashboard
            </Button>
            <Button variant="ghost" className="w-full justify-start text-gray-400 hover:text-white hover:bg-white/5 transition-all">
              <ListTodo className="mr-2 h-4 w-4" />
              My Tasks
            </Button>
          </nav>

          <div className="mt-8 px-4">
             <div className="rounded-xl border border-primary/20 bg-gradient-to-br from-primary/10 to-transparent p-4 relative overflow-hidden group">
                <div className="absolute inset-0 bg-primary/5 group-hover:bg-primary/10 transition-colors" />
                <h4 className="font-semibold text-sm mb-2 text-primary relative z-10">Pro Tip</h4>
                <p className="text-xs text-gray-400 relative z-10 leading-relaxed">
                  Press <kbd className="bg-black/30 px-1.5 py-0.5 rounded border border-white/10 text-white font-mono">⌘K</kbd> to open the Command Orb instantly.
                </p>
             </div>
          </div>
        </div>

        <div className="border-t border-white/5 p-4 bg-black/20">
          <div className="flex items-center gap-3 mb-4">
             <div className="h-9 w-9 rounded-full bg-gradient-to-tr from-primary to-blue-500 p-[1px]">
               <div className="h-full w-full rounded-full bg-[#0a0f1c] flex items-center justify-center text-xs font-bold text-white">
                 {user?.name?.charAt(0) || 'U'}
               </div>
             </div>
             <div className="flex-1 overflow-hidden">
                <p className="text-sm font-medium truncate text-gray-200">{user?.name}</p>
                <p className="text-xs text-gray-500 truncate">{user?.email}</p>
             </div>
          </div>
          <div className="space-y-2">
            <Link href="/">
              <Button variant="ghost" className="w-full justify-start text-gray-400 hover:text-white hover:bg-white/5 transition-all">
                <LayoutDashboard className="mr-2 h-4 w-4 rotate-180" /> {/* Reusing icon for visual context */}
                Back to Home
              </Button>
            </Link>
            <Button variant="outline" className="w-full justify-start border-white/10 text-gray-400 hover:bg-red-500/10 hover:text-red-400 hover:border-red-500/20 transition-all" onClick={() => logout()}>
              <LogOut className="mr-2 h-4 w-4" />
              Sign Out
            </Button>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex flex-1 flex-col overflow-hidden relative z-10">
        {/* Header */}
        <header className="flex h-16 items-center justify-between border-b border-white/5 px-6 bg-[#030712]/50 backdrop-blur-sm z-10">
           <div className="flex items-center gap-4 md:hidden">
              <Button variant="ghost" size="icon" onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}>
                <Menu className="h-5 w-5" />
              </Button>
              <div className="flex items-center">
                <TickwenLogo className="h-8 w-8" />
                <span className="font-bold text-lg mt-0.5 -ml-1">ickwen</span>
              </div>
           </div>
           
           <div className="hidden md:flex items-center gap-2 text-sm text-gray-400">
              <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/5 border border-white/5 text-xs font-medium">
                 <div className="h-1.5 w-1.5 rounded-full bg-green-500 animate-pulse shadow-[0_0_10px_rgba(34,197,94,0.5)]" />
                 System Operational
              </span>
           </div>

           <div className="flex items-center gap-4">
              <Button 
                variant="outline" 
                size="sm" 
                onClick={() => setIsFocusMode(true)}
                disabled={!focusTask}
                className={cn(
                  "hidden sm:flex border-primary/30 text-primary hover:bg-primary/10 hover:text-primary",
                  !focusTask && "opacity-50 cursor-not-allowed"
                )}
              >
                 <Zap className="mr-2 h-4 w-4" />
                 Focus Mode
              </Button>
              
              <Button variant="ghost" size="icon" className="text-gray-400 hover:text-white relative">
                 <Bell className="h-5 w-5" />
                 <span className="absolute top-2 right-2 h-2 w-2 rounded-full bg-red-500 border border-black" />
              </Button>

              <Link href="/create">
                <Button size="sm" className="bg-primary hover:bg-primary/90 text-primary-foreground font-medium shadow-lg shadow-primary/20">
                  <Plus className="mr-2 h-4 w-4" />
                  New Task
                </Button>
              </Link>
           </div>
        </header>

        <div className="flex-1 overflow-y-auto p-4 md:p-8 custom-scrollbar">
           <div className="max-w-5xl mx-auto space-y-8 pb-20">
              
              {/* Stats Overview */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                 <motion.div 
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3 }}
                    className="p-6 rounded-2xl bg-[#0a0f1c]/60 border border-white/5 shadow-lg backdrop-blur-sm hover:border-primary/20 transition-colors"
                 >
                    <p className="text-sm text-gray-500 font-medium mb-1">Total Tasks</p>
                    <h3 className="text-3xl font-bold tracking-tight text-white">{totalTasks}</h3>
                 </motion.div>
                 <motion.div 
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3, delay: 0.1 }}
                    className="p-6 rounded-2xl bg-[#0a0f1c]/60 border border-white/5 shadow-lg backdrop-blur-sm hover:border-primary/20 transition-colors"
                 >
                    <p className="text-sm text-gray-500 font-medium mb-1">Completed</p>
                    <div className="flex items-baseline gap-2">
                       <h3 className="text-3xl font-bold tracking-tight text-primary">{completedTasks}</h3>
                       <span className="text-sm text-gray-600">/ {totalTasks}</span>
                    </div>
                 </motion.div>
                 <motion.div 
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3, delay: 0.2 }}
                    className="p-6 rounded-2xl bg-[#0a0f1c]/60 border border-white/5 shadow-lg backdrop-blur-sm hover:border-primary/20 transition-colors flex flex-col justify-center"
                 >
                    <p className="text-sm text-gray-500 font-medium mb-2">Completion Rate</p>
                    <div className="h-2 w-full bg-black/40 rounded-full overflow-hidden border border-white/5">
                       <motion.div 
                          className="h-full bg-primary shadow-[0_0_10px_rgba(52,211,153,0.5)]" 
                          initial={{ width: 0 }}
                          animate={{ width: `${progress}%` }}
                          transition={{ duration: 1, ease: "circOut" }}
                       />
                    </div>
                    <p className="text-right text-xs text-gray-500 mt-2">{Math.round(progress)}%</p>
                 </motion.div>
              </div>

              {/* Task List Section */}
              <div className="space-y-4">
                 <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                    <div>
                       <h2 className="text-xl font-semibold tracking-tight text-white">Your Tasks</h2>
                       <p className="text-sm text-gray-500">Manage and track your daily activities</p>
                    </div>
                    <div className="relative w-full sm:w-64 group">
                       <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500 group-focus-within:text-primary transition-colors" />
                       <Input
                         placeholder="Filter tasks..."
                         value={filterQuery}
                         onChange={(e) => setFilterQuery(e.target.value)}
                         className="pl-9 bg-black/20 border-white/10 focus:border-primary/50 focus:ring-primary/20 transition-all text-sm h-9"
                       />
                    </div>
                 </div>

                 <div className="bg-[#0a0f1c]/40 border border-white/5 rounded-2xl overflow-hidden min-h-[400px] relative backdrop-blur-md">
                    {isLoading ? (
                       <div className="absolute inset-0 flex items-center justify-center bg-black/20 z-10">
                          <Loader />
                       </div>
                    ) : (
                       <div className="p-4">
                          {error && (
                             <div className="mb-4 p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
                                {error}
                             </div>
                          )}
                          <TaskList
                             tasks={tasks}
                             filterQuery={filterQuery}
                             onToggle={toggleTask}
                             onDelete={(id) => {
                                const task = tasks.find(t => t.id === id);
                                handleDeleteClick(id, task?.title || '');
                             }}
                          />
                       </div>
                    )}
                 </div>
              </div>
           </div>
        </div>
      </main>

      <DeleteConfirmationModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onConfirm={handleConfirmDelete}
        taskTitle={tasks.find(t => t.id === selectedTaskId)?.title}
      />

      {/* Mobile Sidebar Overlay */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsMobileMenuOpen(false)}
              className="fixed inset-0 z-40 bg-black/80 backdrop-blur-sm md:hidden"
            />
            <motion.aside
              initial={{ x: "-100%" }}
              animate={{ x: 0 }}
              exit={{ x: "-100%" }}
              transition={{ type: "spring", damping: 25, stiffness: 200 }}
              className="fixed inset-y-0 left-0 z-50 w-72 border-r border-white/5 bg-[#0a0f1c] p-6 shadow-2xl md:hidden"
            >
              <div className="flex items-center justify-between mb-8">
                <Link href="/" className="flex items-center hover:opacity-80 transition-opacity">
                   <TickwenLogo className="h-9 w-9" />
                   <span className="font-bold text-xl tracking-tight text-white mt-1 -ml-[10px]">ickwen</span>
                </Link>
                <Button variant="ghost" size="icon" onClick={() => setIsMobileMenuOpen(false)}>
                  <X className="h-5 w-5 text-gray-400" />
                </Button>
              </div>

              <div className="space-y-6">
                 <nav className="space-y-1">
                  <Button variant="secondary" className="w-full justify-start font-medium text-primary bg-primary/10 border border-primary/10">
                    <LayoutDashboard className="mr-2 h-4 w-4" />
                    Dashboard
                  </Button>
                  <Button variant="ghost" className="w-full justify-start text-gray-400 hover:text-white hover:bg-white/5">
                    <ListTodo className="mr-2 h-4 w-4" />
                    My Tasks
                  </Button>
                 </nav>

                 <div className="pt-6 border-t border-white/5">
                    <div className="flex items-center gap-3 mb-6">
                       <div className="h-10 w-10 rounded-full bg-gradient-to-tr from-primary to-blue-500 p-[1px]">
                         <div className="h-full w-full rounded-full bg-[#0a0f1c] flex items-center justify-center text-sm font-bold text-white">
                           {user?.name?.charAt(0) || 'U'}
                         </div>
                       </div>
                       <div>
                          <p className="text-sm font-medium text-gray-200">{user?.name}</p>
                          <p className="text-xs text-gray-500">{user?.email}</p>
                       </div>
                    </div>
                    
                    <div className="space-y-2">
                      <Link href="/" onClick={() => setIsMobileMenuOpen(false)}>
                        <Button variant="ghost" className="w-full justify-start text-gray-400 hover:text-white hover:bg-white/5">
                          <LayoutDashboard className="mr-2 h-4 w-4 rotate-180" />
                          Back to Home
                        </Button>
                      </Link>
                      <Button variant="outline" className="w-full justify-start border-white/10 text-gray-400 hover:bg-red-500/10 hover:text-red-400" onClick={() => logout()}>
                        <LogOut className="mr-2 h-4 w-4" />
                        Sign Out
                      </Button>
                    </div>
                 </div>
              </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>
    </div>
  );
}