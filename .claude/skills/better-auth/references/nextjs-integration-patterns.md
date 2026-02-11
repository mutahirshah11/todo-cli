# Better-Auth Next.js Integration Patterns

## App Router Integration

### 1. Authentication Configuration
```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";
import { nextjs } from "@better-auth/next-js";

export const auth = betterAuth({
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL!,
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true,
  },
  session: {
    expiresIn: 7 * 24 * 60 * 60, // 7 days
    cookie: {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
    },
  },
});

export const { getServerSession, signIn, signOut } = nextjs(auth);
```

### 2. Route Handler Integration
```typescript
// app/api/auth/[...nextauth]/route.ts
import { auth } from "@/lib/auth";
import { nextjs } from "@better-auth/next-js";

export const { GET, POST } = nextjs(auth);
```

### 3. Server Component Authentication
```typescript
// app/dashboard/page.tsx
import { getServerSession } from "@/lib/auth";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await getServerSession();

  if (!session?.user) {
    redirect("/login");
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold">Welcome, {session.user.name || session.user.email}</h1>
      <p className="text-gray-600">Your account was created on {session.user.createdAt?.toString()}</p>
    </div>
  );
}
```

### 4. Client Component Authentication
```typescript
// components/user-profile.tsx
"use client";
import { useSession } from "better-auth/react";
import { signOut } from "@/lib/auth";

export function UserProfile() {
  const { data: session, isLoading, mutate } = useSession();

  if (isLoading) {
    return <div className="animate-pulse">Loading...</div>;
  }

  if (!session) {
    return (
      <div className="bg-red-100 p-4 rounded-md">
        <p>You need to log in to access this page.</p>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-2">User Profile</h2>
      <p><strong>Name:</strong> {session.user.name || "Not provided"}</p>
      <p><strong>Email:</strong> {session.user.email}</p>
      <p><strong>ID:</strong> {session.user.id}</p>
      <button
        onClick={() => signOut()}
        className="mt-4 bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
      >
        Sign Out
      </button>
    </div>
  );
}
```

## Middleware Integration

### 5. Authentication Middleware
```typescript
// middleware.ts
import { auth } from "@/lib/auth";

export default auth.middleware;

export const config = {
  matcher: [
    // Apply authentication to protected routes
    "/dashboard/:path*",
    "/admin/:path*",
    "/api/protected/:path*",
    // Exclude public routes
    "/((?!api|_next/static|_next/image|favicon.ico|login|register).*)",
  ],
};
```

### 6. Conditional Middleware
```typescript
// middleware.ts with custom logic
import { auth } from "@/lib/auth";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  // Custom authentication logic
  const isAuthenticated = checkAuth(request);

  if (request.nextUrl.pathname.startsWith('/admin')) {
    if (!isAuthenticated) {
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }

  return auth.middleware(request);
}

export const config = {
  matcher: ['/admin/:path*', '/dashboard/:path*'],
};

function checkAuth(request: NextRequest) {
  // Custom authentication check
  return true; // Replace with actual logic
}
```

## Form Integration

### 7. Sign Up Form
```typescript
// components/signup-form.tsx
"use client";
import { useState } from "react";
import { signUp } from "better-auth/client";

export function SignUpForm() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    name: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const result = await signUp.email({
        email: formData.email,
        password: formData.password,
        name: formData.name,
        callbackURL: "/dashboard", // Redirect after signup
      });

      if (!result.success) {
        setError(result.error?.message || "Sign up failed");
      }
    } catch (err) {
      setError("An unexpected error occurred");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="name" className="block text-sm font-medium">
          Full Name
        </label>
        <input
          id="name"
          type="text"
          value={formData.name}
          onChange={(e) => setFormData({...formData, name: e.target.value})}
          className="w-full px-3 py-2 border rounded-md"
          required
        />
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={formData.email}
          onChange={(e) => setFormData({...formData, email: e.target.value})}
          className="w-full px-3 py-2 border rounded-md"
          required
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={formData.password}
          onChange={(e) => setFormData({...formData, password: e.target.value})}
          className="w-full px-3 py-2 border rounded-md"
          required
          minLength={8}
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 disabled:opacity-50"
      >
        {loading ? "Creating Account..." : "Sign Up"}
      </button>

      {error && <p className="text-red-500 text-sm">{error}</p>}
    </form>
  );
}
```

### 8. Login Form
```typescript
// components/login-form.tsx
"use client";
import { useState } from "react";
import { signIn } from "better-auth/client";

export function LoginForm() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const result = await signIn.email({
        email: formData.email,
        password: formData.password,
        callbackURL: "/dashboard", // Redirect after login
      });

      if (!result.success) {
        setError(result.error?.message || "Login failed");
      }
    } catch (err) {
      setError("An unexpected error occurred");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={formData.email}
          onChange={(e) => setFormData({...formData, email: e.target.value})}
          className="w-full px-3 py-2 border rounded-md"
          required
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={formData.password}
          onChange={(e) => setFormData({...formData, password: e.target.value})}
          className="w-full px-3 py-2 border rounded-md"
          required
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-green-500 text-white py-2 rounded-md hover:bg-green-600 disabled:opacity-50"
      >
        {loading ? "Signing In..." : "Sign In"}
      </button>

      {error && <p className="text-red-500 text-sm">{error}</p>}
    </form>
  );
}
```

## OAuth Integration

### 9. OAuth Login Components
```typescript
// components/oauth-buttons.tsx
"use client";
import { signIn } from "better-auth/client";

export function OAuthButtons() {
  const handleOAuthLogin = async (provider: "google" | "github") => {
    try {
      await signIn.social({
        provider,
        callbackURL: "/dashboard",
      });
    } catch (error) {
      console.error(`${provider} login failed:`, error);
    }
  };

  return (
    <div className="flex flex-col space-y-2">
      <button
        onClick={() => handleOAuthLogin("google")}
        className="flex items-center justify-center gap-2 w-full bg-red-500 text-white py-2 px-4 rounded-md hover:bg-red-600"
      >
        <span>Sign in with Google</span>
      </button>

      <button
        onClick={() => handleOAuthLogin("github")}
        className="flex items-center justify-center gap-2 w-full bg-gray-800 text-white py-2 px-4 rounded-md hover:bg-gray-900"
      >
        <span>Sign in with GitHub</span>
      </button>
    </div>
  );
}
```

## Protected Route Patterns

### 10. Server-Side Protected Route
```typescript
// app/admin/page.tsx
import { getServerSession } from "@/lib/auth";
import { redirect } from "next/navigation";

export default async function AdminPage() {
  const session = await getServerSession();

  // Check if user exists and has admin role
  if (!session?.user || session.user.role !== "admin") {
    redirect("/unauthorized");
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Admin Dashboard</h1>
      <div className="bg-red-100 p-4 rounded-md">
        <p>This is a protected admin page.</p>
        <p>Current user: {session.user.email}</p>
      </div>
    </div>
  );
}
```

### 11. Client-Side Protected Component
```typescript
// components/protected-content.tsx
"use client";
import { useSession } from "better-auth/react";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

export function ProtectedContent({ children }: { children: React.ReactNode }) {
  const { data: session, isLoading } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !session) {
      router.push("/login");
    }
  }, [session, isLoading, router]);

  if (isLoading) {
    return <div className="animate-pulse">Loading...</div>;
  }

  if (!session) {
    return null; // Or redirect elsewhere
  }

  return <div>{children}</div>;
}
```

## API Route Integration

### 12. Protected API Routes
```typescript
// app/api/user/profile/route.ts
import { getServerSession } from "@/lib/auth";
import { NextResponse } from "next/server";

export async function GET() {
  const session = await getServerSession();

  if (!session?.user) {
    return NextResponse.json(
      { error: "Unauthorized" },
      { status: 401 }
    );
  }

  // Return user profile data
  return NextResponse.json({
    user: {
      id: session.user.id,
      email: session.user.email,
      name: session.user.name,
      role: session.user.role,
      createdAt: session.user.createdAt,
    },
  });
}

export async function PUT(request: Request) {
  const session = await getServerSession();

  if (!session?.user) {
    return NextResponse.json(
      { error: "Unauthorized" },
      { status: 401 }
    );
  }

  try {
    const { name, bio } = await request.json();

    // Update user profile
    const updatedUser = await updateUserProfile(session.user.id, { name, bio });

    return NextResponse.json({
      success: true,
      user: updatedUser,
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to update profile" },
      { status: 500 }
    );
  }
}
```

## Session Management

### 13. Session Utilities
```typescript
// lib/session-utils.ts
import { getServerSession } from "@/lib/auth";

export async function getUserRole() {
  const session = await getServerSession();
  return session?.user?.role || null;
}

export async function hasPermission(permission: string) {
  const session = await getServerSession();
  if (!session?.user) return false;

  // Check if user has required permission
  // This would depend on your permission system
  return session.user.permissions?.includes(permission) || false;
}

export async function requireAdmin() {
  const session = await getServerSession();
  if (!session?.user || session.user.role !== "admin") {
    throw new Error("Admin access required");
  }
  return session;
}
```

## Error Handling

### 14. Authentication Error Boundaries
```typescript
// components/auth-error-boundary.tsx
"use client";
import { Component, ReactNode } from "react";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class AuthErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: any) {
    console.error("Auth error caught by boundary:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="bg-red-100 p-4 rounded-md">
          <h2 className="text-red-800 font-semibold">Authentication Error</h2>
          <p className="text-red-600">{this.state.error?.message}</p>
        </div>
      );
    }

    return this.props.children;
  }
}
```

## Loading States

### 15. Authentication Loading Components
```typescript
// components/auth-loading.tsx
import { useSession } from "better-auth/react";

export function AuthLoading({
  children,
  fallback = <div>Loading authentication...</div>,
  unauthorizedFallback = <div>Please log in to continue.</div>
}: {
  children: React.ReactNode;
  fallback?: React.ReactNode;
  unauthorizedFallback?: React.ReactNode;
}) {
  const { data: session, isLoading } = useSession();

  if (isLoading) {
    return <>{fallback}</>;
  }

  if (!session) {
    return <>{unauthorizedFallback}</>;
  }

  return <>{children}</>;
}
```

## Environment Configuration

### 16. Environment Setup
```typescript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverActions: true,
  },
  env: {
    // These will be available on the server
    NEXTAUTH_URL: process.env.NEXTAUTH_URL,
    NEXTAUTH_SECRET: process.env.NEXTAUTH_SECRET,
  },
  async redirects() {
    return [
      // Redirect from old auth paths to new ones
      {
        source: '/auth/signin',
        destination: '/login',
        permanent: true,
      },
    ];
  },
};

module.exports = nextConfig;
```

## Testing Patterns

### 17. Testing Authentication
```typescript
// __tests__/auth.test.tsx
import { render, screen, waitFor } from "@testing-library/react";
import { AuthProvider } from "better-auth/react";
import { auth } from "@/lib/auth";

// Mock session provider
jest.mock("better-auth/react", () => ({
  useSession: jest.fn(() => ({
    data: { user: { name: "Test User", email: "test@example.com" } },
    isLoading: false,
  })),
}));

describe("Authentication Components", () => {
  it("should render user profile when authenticated", () => {
    render(
      <AuthProvider auth={auth}>
        <UserProfile />
      </AuthProvider>
    );

    expect(screen.getByText("Test User")).toBeInTheDocument();
    expect(screen.getByText("test@example.com")).toBeInTheDocument();
  });
});
```

These integration patterns provide comprehensive coverage for implementing Better-Auth with Next.js, including both App Router and traditional patterns, middleware integration, form handling, API routes, and proper error handling.