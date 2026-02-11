# Authentication Patterns

Better-Auth integration with Next.js 15 App Router.

## Better-Auth Setup

### Installation

```bash
npm install better-auth
```

### Auth Configuration

```tsx
// lib/auth.ts
import { betterAuth } from 'better-auth'
import { prismaAdapter } from 'better-auth/adapters/prisma'
import { prisma } from './prisma'

export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: 'postgresql',
  }),
  emailAndPassword: {
    enabled: true,
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day
  },
})

export type Session = typeof auth.$Infer.Session
```

### Auth Client

```tsx
// lib/auth-client.ts
import { createAuthClient } from 'better-auth/react'

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL!,
})

export const {
  signIn,
  signUp,
  signOut,
  useSession,
} = authClient
```

### Route Handler

```tsx
// app/api/auth/[...all]/route.ts
import { auth } from '@/lib/auth'
import { toNextJsHandler } from 'better-auth/next-js'

export const { GET, POST } = toNextJsHandler(auth)
```

---

## Middleware Configuration

### Cookie-Based Check (Recommended)

```tsx
// middleware.ts
import { NextRequest, NextResponse } from 'next/server'
import { getSessionCookie } from 'better-auth/cookies'

// Routes that require authentication
const protectedRoutes = [
  '/dashboard',
  '/agents',
  '/calls',
  '/settings',
]

// Routes only for unauthenticated users
const authRoutes = ['/login', '/register', '/forgot-password']

// Public routes (accessible to all)
const publicRoutes = ['/', '/about', '/pricing']

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const session = getSessionCookie(request)

  // Check if current path matches protected routes
  const isProtectedRoute = protectedRoutes.some(route =>
    pathname.startsWith(route)
  )

  // Check if current path matches auth routes
  const isAuthRoute = authRoutes.some(route =>
    pathname.startsWith(route)
  )

  // Redirect unauthenticated users from protected routes
  if (isProtectedRoute && !session) {
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('callbackUrl', pathname)
    return NextResponse.redirect(loginUrl)
  }

  // Redirect authenticated users from auth routes
  if (isAuthRoute && session) {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - api routes (handled separately)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public files (images, etc.)
     */
    '/((?!api|_next/static|_next/image|favicon.ico|.*\\..*|_next).*)',
  ],
}
```

### Full Session Validation (When Needed)

```tsx
// middleware.ts
import { betterFetch } from '@better-fetch/fetch'
import type { Session } from '@/lib/auth'
import { NextRequest, NextResponse } from 'next/server'

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Only do full validation for sensitive routes
  if (pathname.startsWith('/admin')) {
    const { data: session } = await betterFetch<Session>(
      '/api/auth/get-session',
      {
        baseURL: request.nextUrl.origin,
        headers: {
          cookie: request.headers.get('cookie') || '',
        },
      }
    )

    if (!session) {
      return NextResponse.redirect(new URL('/login', request.url))
    }

    // Check for admin role
    if (session.user.role !== 'admin') {
      return NextResponse.redirect(new URL('/unauthorized', request.url))
    }
  }

  return NextResponse.next()
}
```

---

## Server-Side Session Access

### In Server Components

```tsx
// app/dashboard/page.tsx
import { headers } from 'next/headers'
import { auth } from '@/lib/auth'

export default async function DashboardPage() {
  const session = await auth.api.getSession({
    headers: await headers(),
  })

  if (!session) {
    // This shouldn't happen if middleware is set up correctly
    redirect('/login')
  }

  return (
    <div>
      <h1>Welcome, {session.user.name}!</h1>
    </div>
  )
}
```

### In Server Actions

```tsx
// app/agents/actions.ts
'use server'

import { headers } from 'next/headers'
import { auth } from '@/lib/auth'

export async function createAgent(formData: FormData) {
  const session = await auth.api.getSession({
    headers: await headers(),
  })

  if (!session) {
    return { success: false, error: 'Unauthorized' }
  }

  // Now you have access to session.user.id for org_id, etc.
  const data = {
    name: formData.get('name'),
    org_id: session.user.organizationId,
    created_by: session.user.id,
  }

  // Call FastAPI with the data
  await api.post('/api/agents', data)

  revalidatePath('/agents')
  return { success: true }
}
```

### Utility Function

```tsx
// lib/auth-utils.ts
import { headers } from 'next/headers'
import { auth } from '@/lib/auth'
import { redirect } from 'next/navigation'

export async function requireAuth() {
  const session = await auth.api.getSession({
    headers: await headers(),
  })

  if (!session) {
    redirect('/login')
  }

  return session
}

// Usage in Server Component
export default async function ProtectedPage() {
  const session = await requireAuth()
  // ...
}
```

---

## Client-Side Session

### Using the Hook

```tsx
// components/user-menu.tsx
'use client'

import { useSession, signOut } from '@/lib/auth-client'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'

export function UserMenu() {
  const { data: session, isPending } = useSession()

  if (isPending) {
    return <div className="w-8 h-8 rounded-full bg-muted animate-pulse" />
  }

  if (!session) {
    return null
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="relative h-8 w-8 rounded-full">
          <Avatar className="h-8 w-8">
            <AvatarImage src={session.user.image || ''} />
            <AvatarFallback>
              {session.user.name?.charAt(0).toUpperCase()}
            </AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem asChild>
          <Link href="/settings">Settings</Link>
        </DropdownMenuItem>
        <DropdownMenuItem
          onClick={() => signOut({ fetchOptions: { onSuccess: () => router.push('/') } })}
        >
          Sign out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
```

---

## Auth Forms

### Login Form

```tsx
// components/auth/login-form.tsx
'use client'

import { useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { signIn } from '@/lib/auth-client'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { toast } from 'sonner'

export function LoginForm() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const callbackUrl = searchParams.get('callbackUrl') || '/dashboard'
  const [isPending, setIsPending] = useState(false)

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setIsPending(true)

    const formData = new FormData(e.currentTarget)
    const email = formData.get('email') as string
    const password = formData.get('password') as string

    const { error } = await signIn.email({
      email,
      password,
      callbackURL: callbackUrl,
    })

    setIsPending(false)

    if (error) {
      toast.error(error.message || 'Invalid credentials')
      return
    }

    router.push(callbackUrl)
    router.refresh()
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          name="email"
          type="email"
          placeholder="you@example.com"
          required
          disabled={isPending}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="password">Password</Label>
        <Input
          id="password"
          name="password"
          type="password"
          required
          disabled={isPending}
        />
      </div>

      <Button type="submit" className="w-full" disabled={isPending}>
        {isPending ? 'Signing in...' : 'Sign in'}
      </Button>
    </form>
  )
}
```

### Social Login

```tsx
// components/auth/social-buttons.tsx
'use client'

import { signIn } from '@/lib/auth-client'
import { Button } from '@/components/ui/button'

export function SocialButtons() {
  return (
    <div className="grid gap-2">
      <Button
        variant="outline"
        onClick={() =>
          signIn.social({
            provider: 'google',
            callbackURL: '/dashboard',
          })
        }
      >
        <GoogleIcon className="mr-2 h-4 w-4" />
        Continue with Google
      </Button>

      <Button
        variant="outline"
        onClick={() =>
          signIn.social({
            provider: 'github',
            callbackURL: '/dashboard',
          })
        }
      >
        <GitHubIcon className="mr-2 h-4 w-4" />
        Continue with GitHub
      </Button>
    </div>
  )
}
```

---

## Passing Auth to FastAPI

### Forward Token in API Calls

```tsx
// lib/api.ts
import { cookies } from 'next/headers'

export async function apiWithAuth<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const cookieStore = await cookies()

  // Get the session token from Better-Auth cookie
  const sessionToken = cookieStore.get('better-auth.session_token')?.value

  const response = await fetch(`${process.env.FASTAPI_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      // Forward the session token to FastAPI
      ...(sessionToken && {
        Authorization: `Bearer ${sessionToken}`,
      }),
      ...options.headers,
    },
  })

  if (response.status === 401) {
    // Session expired or invalid
    redirect('/login?error=session_expired')
  }

  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`)
  }

  return response.json()
}
```

### FastAPI Validation

FastAPI should validate the session token against the same database/session store:

```python
# Python FastAPI example
from fastapi import Depends, HTTPException, Header
from typing import Optional

async def get_current_user(
    authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.split(' ')[1]

    # Validate against your session store
    session = await validate_session(token)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")

    return session.user
```

---

## Protected Layout Pattern

```tsx
// app/(protected)/layout.tsx
import { headers } from 'next/headers'
import { redirect } from 'next/navigation'
import { auth } from '@/lib/auth'
import { Sidebar } from '@/components/sidebar'
import { Header } from '@/components/header'

export default async function ProtectedLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const session = await auth.api.getSession({
    headers: await headers(),
  })

  if (!session) {
    redirect('/login')
  }

  return (
    <div className="flex h-screen">
      <Sidebar user={session.user} />
      <div className="flex-1 flex flex-col">
        <Header user={session.user} />
        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
```

---

## Role-Based Access

```tsx
// lib/auth-utils.ts
export async function requireRole(allowedRoles: string[]) {
  const session = await requireAuth()

  if (!allowedRoles.includes(session.user.role)) {
    redirect('/unauthorized')
  }

  return session
}

// app/admin/page.tsx
export default async function AdminPage() {
  const session = await requireRole(['admin', 'super_admin'])

  return <AdminDashboard />
}
```
