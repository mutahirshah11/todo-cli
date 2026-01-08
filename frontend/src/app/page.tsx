import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-muted">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            Streamline Your Tasks with <span className="text-primary">Tickwen</span>
          </h1>

          <p className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto">
            A premium task management application designed to help you organize, track, and complete your goals efficiently.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/dashboard">
              <Button size="lg" className="px-8 py-3 text-lg">
                Go to Dashboard
              </Button>
            </Link>

            <Link href="/login">
              <Button variant="outline" size="lg" className="px-8 py-3 text-lg">
                Sign In
              </Button>
            </Link>
          </div>

          <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-card p-6 rounded-lg border">
              <h3 className="text-xl font-semibold mb-2">Organize</h3>
              <p className="text-muted-foreground">
                Create and categorize tasks to keep everything in order.
              </p>
            </div>

            <div className="bg-card p-6 rounded-lg border">
              <h3 className="text-xl font-semibold mb-2">Track</h3>
              <p className="text-muted-foreground">
                Monitor your progress and stay on top of deadlines.
              </p>
            </div>

            <div className="bg-card p-6 rounded-lg border">
              <h3 className="text-xl font-semibold mb-2">Complete</h3>
              <p className="text-muted-foreground">
                Mark tasks as done and celebrate your achievements.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
