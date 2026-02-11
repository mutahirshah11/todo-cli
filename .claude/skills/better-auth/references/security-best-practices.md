# Better-Auth Security Best Practices

## Critical Security Measures

### 1. HTTP-Only Cookies (Essential)
HTTP-only cookies are the cornerstone of secure session management. They prevent XSS attacks by making session tokens inaccessible to client-side JavaScript.

```typescript
// Correct configuration
session: {
  cookie: {
    name: "__Secure-NextAuth_Session", // Use secure prefix
    httpOnly: true,                    // Critical: prevents XSS
    secure: process.env.NODE_ENV === "production", // HTTPS only in production
    sameSite: "lax" as const,          // Prevents CSRF
    maxAge: 7 * 24 * 60 * 60,        // 7 days
  },
},
```

**Security Impact:**
- ✅ Prevents XSS from stealing session tokens
- ✅ Reduces risk of session hijacking
- ❌ XSS attacks cannot access the session cookie

### 2. Secure Environment Variables
Never expose sensitive credentials in client-side code.

```env
# ✅ CORRECT: Server-side only
NEXTAUTH_URL="https://yourapp.com"
NEXTAUTH_SECRET="your-super-secret-key-here"

# ❌ INCORRECT: Never put in client bundle
NEXT_PUBLIC_DB_PASSWORD="do-not-do-this"
```

### 3. CSRF Protection
Better-Auth includes built-in CSRF protection, but ensure it's properly configured:

```typescript
// CSRF protection is enabled by default
auth: {
  csrf: {
    enabled: true,  // Default: true
    cookie: {
      name: "__Host-CSRF-Token",
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict" as const,
    },
  },
}
```

## Authentication Security

### 4. Strong Password Requirements
Implement robust password policies to prevent weak passwords:

```typescript
emailAndPassword: {
  enabled: true,
  password: {
    // Minimum requirements
    minLength: 12,                    // Longer is better
    requireNumbers: true,             // At least one number
    requireSymbols: true,             // At least one symbol
    requireUppercase: true,           // At least one uppercase
    requireLowercase: true,           // At least one lowercase

    // Advanced options
    enableBreachDetection: true,      // Check against known breaches
    maxRepeatingCharacters: 2,        // Prevent "aaaaaa"
    minWords: 3,                     // For passphrases
  },
},
```

### 5. Account Lockout and Rate Limiting
Protect against brute force attacks:

```typescript
// Rate limiting configuration
rateLimit: {
  // Login attempts
  signIn: {
    window: 15 * 60 * 1000,  // 15 minutes
    max: 5,                   // 5 attempts per window
  },
  // Password reset attempts
  passwordReset: {
    window: 60 * 60 * 1000,  // 1 hour
    max: 3,                   // 3 attempts per hour
  },
  // Account lockout
  accountLockout: {
    duration: 15 * 60 * 1000, // Lock for 15 minutes
    attempts: 10,              // After 10 failed attempts
  },
},
```

### 6. Email Verification
Require email verification for account security:

```typescript
emailAndPassword: {
  requireEmailVerification: true,  // Force email verification

  // Verification email customization
  verification: {
    expires: 24 * 60 * 60 * 1000,  // 24 hours
    resendDelay: 5 * 60 * 1000,    // 5 minutes between resends
  },
},
```

## Session Security

### 7. Session Token Rotation
Implement automatic session token rotation to limit exposure windows:

```typescript
session: {
  expiresIn: 7 * 24 * 60 * 60,     // 7 days
  updateAge: 1 * 24 * 60 * 60,     // Rotate every 24 hours
  slidingExpiration: true,          // Extend session with activity

  // Advanced rotation
  maxInactiveAge: 30 * 60,          // 30 minutes of inactivity
  updateAgeOnVisit: true,           // Refresh on every visit
},
```

### 8. Secure OAuth Configuration
Properly configure OAuth providers to prevent open redirect attacks:

```typescript
socialProviders: {
  google: {
    clientId: process.env.GOOGLE_CLIENT_ID!,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET!,

    // Security settings
    scope: ["openid", "email", "profile"],  // Minimal required scope
    authorizationParams: {
      prompt: "select_account",  // Force account selection
    },
  },

  github: {
    clientId: process.env.GITHUB_CLIENT_ID!,
    clientSecret: process.env.GITHUB_CLIENT_SECRET!,

    // Security settings
    scope: ["read:user", "user:email"],  // Minimal required scope
  },
},
```

## Advanced Security Features

### 9. Two-Factor Authentication (2FA)
Enable multi-factor authentication for enhanced security:

```typescript
// Enable 2FA
twoFactor: {
  enabled: true,
  issuer: "Your App Name",           // For authenticator apps
  backupCodes: {
    enabled: true,                  // Enable backup codes
    count: 10,                      // Number of backup codes
  },
  totp: {
    algorithm: "SHA1",              // Or SHA256, SHA512
    digits: 6,                      // 6-digit codes
    period: 30,                     // 30-second intervals
  },
},

// Require 2FA for sensitive operations
require2FA: {
  enabled: true,
  gracePeriod: 7 * 24 * 60 * 60,   // 7 days to enable 2FA
  exemptPaths: [],                  // Paths that don't require 2FA
},
```

### 10. Account Linking Security
Secure account linking to prevent unauthorized associations:

```typescript
account: {
  accountLinking: {
    enabled: true,
    requiredAccountTypes: ["email", "oauth"],  // Require both for linking
    trustedEmails: true,                      // Auto-link trusted emails
    sessionManagement: {
      enableSessionMerging: true,             // Merge sessions after linking
      allowMultipleSessions: false,           // One session per account
    },
  },
},
```

## API Security

### 11. Protected API Routes
Secure your API routes with proper authentication:

```typescript
// app/api/protected/route.ts
import { getServerSession } from "@/lib/auth";
import { NextResponse } from "next/server";

export async function GET(request: Request) {
  const session = await getServerSession();

  // ✅ Proper authentication check
  if (!session?.user) {
    return NextResponse.json(
      { error: "Unauthorized" },
      { status: 401 }
    );
  }

  // ✅ Validate user permissions
  if (session.user.role !== "admin") {
    return NextResponse.json(
      { error: "Insufficient permissions" },
      { status: 403 }
    );
  }

  // ✅ Safe to proceed with admin operations
  return NextResponse.json({
    message: "Admin data",
    user: session.user.email,
  });
}
```

### 12. Input Validation and Sanitization
Always validate and sanitize inputs, even with authentication:

```typescript
// ✅ Secure API route with validation
export async function POST(request: Request) {
  const session = await getServerSession();
  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    const body = await request.json();

    // ✅ Validate input
    const { comment, postId } = body;

    if (!comment || typeof comment !== "string" || comment.length > 1000) {
      return NextResponse.json(
        { error: "Invalid comment" },
        { status: 400 }
      );
    }

    if (!postId || typeof postId !== "string") {
      return NextResponse.json(
        { error: "Invalid post ID" },
        { status: 400 }
      );
    }

    // ✅ Sanitize input
    const sanitizedComment = comment.trim().substring(0, 1000);

    // ✅ Validate user owns the resource (if applicable)
    const post = await getPostById(postId);
    if (post.userId !== session.user.id) {
      return NextResponse.json(
        { error: "Not authorized for this post" },
        { status: 403 }
      );
    }

    // ✅ Proceed with safe operation
    await createComment(sanitizedComment, postId, session.user.id);

    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
```

## Security Headers and Middleware

### 13. Security Headers
Configure security headers to protect against common attacks:

```typescript
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const response = NextResponse.next();

  // ✅ Security headers
  response.headers.set("X-Frame-Options", "DENY");
  response.headers.set("X-Content-Type-Options", "nosniff");
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  response.headers.set("Permissions-Policy", "camera=(), microphone=()");

  // ✅ Content Security Policy
  response.headers.set(
    "Content-Security-Policy",
    "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;"
  );

  return response;
}

export const config = {
  matcher: ["/dashboard/:path*", "/admin/:path*"],
};
```

## Monitoring and Logging

### 14. Security Event Logging
Log security-relevant events for monitoring:

```typescript
// hooks for security logging
hooks: {
  signIn: async (user, account, profile) => {
    // Log successful sign-ins
    console.log("SIGN_IN_SUCCESS", {
      userId: user.id,
      email: user.email,
      provider: account?.provider,
      timestamp: new Date().toISOString(),
      ip: getIP(), // Implement IP logging
    });
  },

  signInFailure: async (error, profile) => {
    // Log failed sign-ins
    console.warn("SIGN_IN_FAILURE", {
      error: error.message,
      email: profile?.email,
      timestamp: new Date().toISOString(),
      ip: getIP(), // Implement IP logging
    });
  },

  sessionCreated: async (session) => {
    // Log new sessions
    console.log("SESSION_CREATED", {
      sessionId: session.id,
      userId: session.userId,
      timestamp: new Date().toISOString(),
      userAgent: getUserAgent(), // Implement user agent logging
    });
  },
},
```

## Security Testing

### 15. Common Security Tests
Regularly test your authentication system:

```typescript
// Example security test cases
describe("Authentication Security", () => {
  test("Should reject invalid credentials", async () => {
    const response = await signIn.email({
      email: "nonexistent@example.com",
      password: "wrong-password",
    });
    expect(response.success).toBe(false);
  });

  test("Should prevent session fixation", async () => {
    // Test that session ID changes after login
    const oldSession = getCurrentSession();
    await login();
    const newSession = getCurrentSession();
    expect(oldSession.id).not.toBe(newSession.id);
  });

  test("Should enforce rate limiting", async () => {
    // Test that multiple failed attempts are rate-limited
    for (let i = 0; i < 10; i++) {
      await attemptFailedLogin();
    }
    const response = await attemptFailedLogin();
    expect(response.status).toBe(429); // Too Many Requests
  });
});
```

## Emergency Procedures

### 16. Incident Response
Have procedures ready for security incidents:

```typescript
// Emergency session invalidation
async function invalidateAllSessionsForUser(userId: string) {
  // This would be called during a security incident
  await db.session.deleteMany({
    where: { userId },
  });
}

// Emergency password reset
async function forcePasswordReset(userId: string) {
  // Invalidate current password and require reset
  await db.user.update({
    where: { id: userId },
    data: {
      passwordNeedsReset: true,
      passwordResetRequiredAt: new Date(),
    },
  });
}
```

## Security Checklist

### ✅ Before Going Live
- [ ] HTTP-only cookies enabled
- [ ] Secure flags set for production
- [ ] CSRF protection enabled
- [ ] Rate limiting configured
- [ ] Password requirements enforced
- [ ] Email verification required (if needed)
- [ ] Session token rotation enabled
- [ ] OAuth providers properly configured
- [ ] API routes protected
- [ ] Security headers configured
- [ ] Input validation implemented
- [ ] Security logging enabled
- [ ] Incident response procedures ready

### 🔒 Ongoing Security Maintenance
- [ ] Regular dependency updates
- [ ] Security audit reviews
- [ ] Monitor authentication logs
- [ ] Review access patterns
- [ ] Update security policies
- [ ] Test authentication flows
- [ ] Review third-party integrations
- [ ] Update incident response procedures

Following these security best practices will help ensure your Better-Auth implementation remains secure and protects your users' data effectively.