import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ThemeToggle } from '@/components/ui/theme-toggle';
import { useStore } from '@/lib/store';

export function Navbar() {
  const { user, logout, isAuthenticated } = useStore();

  const handleLogout = () => {
    logout();
  };

  return (
    <header className="border-b">
      <div className="container flex h-16 items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <Link href="/" className="text-xl font-bold">
            Tickwen
          </Link>
        </div>

        <div className="flex items-center gap-4">
          <ThemeToggle />

          {isAuthenticated() ? (
            <div className="flex items-center gap-2">
              <span className="text-sm">Welcome, {user?.username}</span>
              <Button variant="outline" size="sm" onClick={handleLogout}>
                Logout
              </Button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Link href="/login">
                <Button variant="outline" size="sm">
                  Login
                </Button>
              </Link>
              <Link href="/register">
                <Button size="sm">
                  Sign Up
                </Button>
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}