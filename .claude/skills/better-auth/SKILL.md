---
name: better-auth
description: This skill provides comprehensive guidance on Better-Auth setup and configuration for authentication in Next.js and FastAPI applications. It should be used when users need guidance on installation, auth configuration, email/password authentication, OAuth providers, session management, JWT tokens, magic link authentication, password reset flows, email verification, multi-factor authentication, and security best practices.
---

# Better-Auth Guide

This skill provides comprehensive guidance on Better-Auth setup and configuration for authentication in Next.js and FastAPI applications. It covers installation, auth configuration, email/password authentication, OAuth providers, session management, JWT tokens, magic link authentication, password reset flows, email verification, multi-factor authentication, and security best practices.

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing authentication patterns, database setup, and security requirements |
| **Conversation** | User's specific authentication needs, OAuth provider requirements, and security constraints |
| **Skill References** | Auth patterns from `references/` (configuration, security, integration) |
| **User Guidelines** | Project-specific security standards, team conventions |

Ensure all required context is gathered before implementing.

## Installation Guide

### Basic Installation
```bash
npm install better-auth @better-auth/next-js
# Or with yarn
yarn add better-auth @better-auth/next-js
```

### Prerequisites
- Node.js 18+
- TypeScript (recommended)
- A supported database (PostgreSQL, MySQL, SQLite)

### Environment Variables
```env
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"

# OAuth Providers (as needed)
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"
GITHUB_CLIENT_ID="your-github-client-id"
GITHUB_CLIENT_SECRET="your-github-client-secret"

# JWT Secret (for JWT tokens)
JWT_SECRET="your-super-secret-jwt-key"
```

## Configuration Options

### Basic Configuration
```typescript
import { betterAuth } from "better-auth";
import { nextjs } from "@better-auth/next-js";

export const auth = betterAuth({
  database: {
    provider: "postgresql", // or "mysql", "sqlite"
    url: process.env.DATABASE_URL!,
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      scope: ["email", "profile"],
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
  },
  // Email/Password authentication
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Set to true for email verification
    password: {
      minLength: 8,
      requireNumbers: true,
      requireSymbols: false,
    },
  },
  // Session configuration
  session: {
    expiresIn: 7 * 24 * 60 * 60, // 7 days in seconds
    updateAge: 24 * 60 * 60, // Update session every 24 hours
    cookie: {
      name: "__session",
      httpOnly: true, // Critical security feature
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax" as const,
      maxAge: 7 * 24 * 60 * 60, // 7 days
    },
  },
  // Account management
  account: {
    accountLinking: {
      enabled: true,
      requiredAccountTypes: ["email", "oauth"],
    },
  },
});

// For Next.js integration
export const { getServerSession, signIn, signOut } = nextjs(auth);
```

### Advanced Configuration
```typescript
export const auth = betterAuth({
  // ... basic config

  // Custom callbacks
  hooks: {
    createUser: async (user) => {
      // Called after user creation
      console.log(`New user created: ${user.email}`);
    },
    sessionCreated: async (session) => {
      // Called after session creation
      console.log(`Session created for user: ${session.userId}`);
    },
  },

  // Rate limiting
  rateLimit: {
    window: 15 * 60 * 1000, // 15 minutes
    max: 5, // 5 requests per window
  },

  // Email configuration
  email: {
    from: "noreply@yourapp.com",
    // Custom email templates can be configured here
  },
});
```

## Authentication Flows

### Email/Password Authentication

#### Sign Up Flow
```typescript
// Client-side sign up
"use client";
import { signUp } from "better-auth/client";

export function SignUpForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const result = await signUp.email({
        email,
        password,
        callbackURL: "/dashboard", // Redirect after successful sign up
      });

      if (!result.success) {
        setError(result.error.message);
      }
    } catch (err) {
      setError("Sign up failed");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button type="submit">Sign Up</button>
      {error && <p>{error}</p>}
    </form>
  );
}
```

#### Login Flow
```typescript
// Client-side login
"use client";
import { signIn } from "better-auth/client";

export function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const result = await signIn.email({
        email,
        password,
        callbackURL: "/dashboard",
      });

      if (!result.success) {
        setError(result.error.message);
      }
    } catch (err) {
      setError("Login failed");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button type="submit">Login</button>
      {error && <p>{error}</p>}
    </form>
  );
}
```

### OAuth Integration

#### Google OAuth Login
```typescript
// Google OAuth login
"use client";
import { signIn } from "better-auth/client";

export function GoogleLoginButton() {
  const handleGoogleLogin = async () => {
    try {
      await signIn.social({
        provider: "google",
        callbackURL: "/dashboard",
      });
    } catch (err) {
      console.error("Google login failed:", err);
    }
  };

  return (
    <button onClick={handleGoogleLogin}>
      Sign in with Google
    </button>
  );
}
```

#### GitHub OAuth Login
```typescript
// GitHub OAuth login
"use client";
import { signIn } from "better-auth/client";

export function GitHubLoginButton() {
  const handleGitHubLogin = async () => {
    try {
      await signIn.social({
        provider: "github",
        callbackURL: "/dashboard",
      });
    } catch (err) {
      console.error("GitHub login failed:", err);
    }
  };

  return (
    <button onClick={handleGitHubLogin}>
      Sign in with GitHub
    </button>
  );
}
```

### Logout
```typescript
// Logout functionality
"use client";
import { signOut } from "better-auth/client";

export function LogoutButton() {
  const handleLogout = async () => {
    try {
      await signOut();
      // User is now logged out
      window.location.href = "/"; // Redirect after logout
    } catch (err) {
      console.error("Logout failed:", err);
    }
  };

  return (
    <button onClick={handleLogout}>
      Logout
    </button>
  );
}
```

## Session Management

### Server-Side Session Access
```typescript
// Server component with session access
import { getServerSession } from "@/lib/auth";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await getServerSession();

  if (!session?.user) {
    redirect("/login");
  }

  return (
    <div>
      <h1>Welcome, {session.user.name || session.user.email}</h1>
      <p>Your session ID: {session.sessionId}</p>
    </div>
  );
}
```

### Client-Side Session Access
```typescript
// Client component with session access
"use client";
import { useSession } from "better-auth/react";

export function UserProfile() {
  const { data: session, isLoading, mutate } = useSession();

  if (isLoading) return <div>Loading...</div>;
  if (!session) return <div>Please log in</div>;

  return (
    <div>
      <h2>Hello, {session.user.name || session.user.email}</h2>
      <p>Email: {session.user.email}</p>
      <p>User ID: {session.user.id}</p>
    </div>
  );
}
```

### Protected Routes (Middleware)
```typescript
// middleware.ts
import { auth } from "@/lib/auth";

export default auth.middleware;

export const config = {
  matcher: [
    // Protect these routes
    "/dashboard/:path*",
    "/admin/:path*",
    "/api/protected/:path*",
    // Exclude public routes
    "/((?!api|_next/static|_next/image|favicon.ico).*)",
  ],
};
```

### API Route Protection
```typescript
// app/api/protected/route.ts
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

  return NextResponse.json({
    message: "This is a protected route",
    user: session.user,
  });
}
```

## OAuth Integration

### OAuth Configuration
```typescript
// Supported OAuth providers
socialProviders: {
  google: {
    clientId: process.env.GOOGLE_CLIENT_ID!,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    scope: ["email", "profile"], // Customize as needed
  },
  github: {
    clientId: process.env.GITHUB_CLIENT_ID!,
    clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    scope: ["read:user", "user:email"], // Customize as needed
  },
  discord: {
    clientId: process.env.DISCORD_CLIENT_ID!,
    clientSecret: process.env.DISCORD_CLIENT_SECRET!,
  },
  microsoft: {
    clientId: process.env.MICROSOFT_CLIENT_ID!,
    clientSecret: process.env.MICROSOFT_CLIENT_SECRET!,
  },
  apple: {
    clientId: process.env.APPLE_CLIENT_ID!,
    teamId: process.env.APPLE_TEAM_ID!,
    privateKey: process.env.APPLE_PRIVATE_KEY!,
    keyId: process.env.APPLE_KEY_ID!,
  },
}
```

### OAuth Callback Configuration
```typescript
// OAuth callback URL configuration
// For Next.js, the callback URL is typically:
// http://localhost:3000/api/auth/callback/[provider]
// or in production: https://yourdomain.com/api/auth/callback/[provider]

// Make sure to configure these in your OAuth provider's dashboard
```

## Security Best Practices

### HTTP-Only Cookies
- Always use HTTP-only cookies for session tokens to prevent XSS attacks
- Configure secure flags for production environments
- Use appropriate SameSite settings to prevent CSRF

### CSRF Protection
- Better-Auth includes built-in CSRF protection
- Uses double-submit cookie pattern
- Validates state parameters for OAuth flows

### Rate Limiting
```typescript
// Rate limiting configuration
rateLimit: {
  window: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 requests per window for sensitive endpoints
},
```

### Password Security
```typescript
// Password requirements configuration
emailAndPassword: {
  password: {
    minLength: 8,
    requireNumbers: true,
    requireSymbols: true,
    requireUppercase: true,
    // Optional: breach detection
    enableBreachDetection: true,
  },
},
```

### Session Token Rotation
```typescript
// Session configuration with token rotation
session: {
  expiresIn: 7 * 24 * 60 * 60, // 7 days
  updateAge: 24 * 60 * 60, // Update session every 24 hours
  // This enables automatic token rotation
},
```

### Email Verification
```typescript
// Enable email verification
emailAndPassword: {
  requireEmailVerification: true, // Requires email verification
},

// Custom email templates can be configured for verification emails
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Session Not Persisting
- Check that your domain configuration matches your actual domain
- Ensure cookies are configured correctly (secure flag in production)
- Verify database connection is working

#### 2. OAuth Callback Issues
- Verify callback URLs are correctly configured in OAuth provider dashboards
- Check that your app is accessible from the internet for OAuth redirects
- Ensure environment variables are properly set

#### 3. Database Connection Problems
- Verify database URL is correct
- Check that your database is running and accessible
- Ensure required tables are created (Better-Auth handles this automatically)

#### 4. CORS Issues
```typescript
// Configure CORS if needed
// In your Next.js config or API routes
export const config = {
  api: {
    bodyParser: false,
  },
};
```

#### 5. Environment Variable Issues
- Ensure all required environment variables are set
- Check that variables are properly prefixed if using Next.js
- Verify variables are available in the correct environment

### Debugging Tips
- Enable debug logging in development
- Check browser developer tools for network errors
- Verify database contains expected user/session data
- Test authentication flows in incognito/private browsing mode