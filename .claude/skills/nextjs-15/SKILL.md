---
name: nextjs-15
description: |
  Next.js 15 App Router patterns for frontend-only architecture with Python FastAPI backend.
  This skill should be used when building UI with Next.js that consumes a FastAPI API, implementing
  Server/Client Components, data fetching from external APIs, Server Actions as API proxies,
  loading/error states, middleware auth with Better-Auth, or optimizing Next.js performance.
---

# Next.js 15 App Router (Frontend Layer for FastAPI)

Guide for building Next.js 15 frontend that consumes a Python FastAPI backend.

## Critical Architecture Rule

```
┌─────────────────────────────────────────────────────────────────┐
│  FRONTEND (Next.js 15)              BACKEND (FastAPI)           │
│  ─────────────────────              ─────────────────           │
│  • Display data                     • Business logic            │
│  • User interactions                • Database queries          │
│  • Form validation (client)         • Authentication logic      │
│  • Call FastAPI endpoints           • Data processing           │
│  • Loading/error states             • API responses             │
└─────────────────────────────────────────────────────────────────┘
```

**Frontend = "dumb" (displays)** | **Backend = "smart" (processes)**

### What NOT to Do in Next.js

- Direct database connections
- Complex business logic in Server Components
- Server Actions that bypass FastAPI for data mutations
- Storing secrets in client-accessible code

## Before Implementation

| Source | Gather |
|--------|--------|
| **Codebase** | Existing components, API client setup, auth configuration |
| **Conversation** | User's specific endpoints, data shapes, UI requirements |
| **Skill References** | Patterns from `references/` for API consumption, components |
| **User Guidelines** | Project conventions, component library (ShadCN) |

---

## Server vs Client Components Decision Tree

```
Is interactivity needed?
├─ NO → Server Component (default)
│   └─ Fetches from FastAPI, renders HTML
└─ YES → Does it need...
    ├─ useState/useEffect? → Client Component
    ├─ onClick/onChange? → Client Component
    ├─ Browser APIs? → Client Component
    └─ Form with real-time validation? → Client Component
```

### Quick Reference

| Use Server Component | Use Client Component |
|---------------------|---------------------|
| Fetch API data | Form inputs with validation |
| Display static content | Interactive buttons/modals |
| SEO-critical content | Real-time updates (polling) |
| Initial page render | useState, useEffect, useRef |
| Access env variables | Browser APIs (localStorage) |

### The "use client" Boundary

```tsx
// app/dashboard/page.tsx (Server Component - default)
import { UserStats } from './user-stats'  // Also server
import { FilterPanel } from './filter-panel'  // Client (has 'use client')

export default async function Dashboard() {
  const data = await fetchFromFastAPI('/api/dashboard')
  return (
    <div>
      <UserStats data={data} />       {/* Static display */}
      <FilterPanel />                  {/* Interactive */}
    </div>
  )
}
```

---

## App Router Structure

```
app/
├── layout.tsx          # Root layout (Server Component)
├── page.tsx            # Home page
├── loading.tsx         # Root loading state
├── error.tsx           # Root error boundary
├── not-found.tsx       # 404 page
├── (auth)/             # Route group (no URL impact)
│   ├── login/page.tsx
│   └── register/page.tsx
├── (dashboard)/        # Another route group
│   ├── layout.tsx      # Dashboard-specific layout
│   ├── page.tsx
│   └── settings/
│       └── page.tsx
├── api/                # Route Handlers (BFF proxy if needed)
│   └── auth/
│       └── [...all]/route.ts  # Better-Auth catch-all
└── @modal/             # Parallel route slot for modals
    └── (.)product/[id]/page.tsx  # Intercepting route
```

### Special Files

| File | Purpose |
|------|---------|
| `page.tsx` | Route UI (required to make route accessible) |
| `layout.tsx` | Shared UI wrapper, preserved across navigation |
| `loading.tsx` | Suspense fallback while page loads |
| `error.tsx` | Error boundary (must be Client Component) |
| `not-found.tsx` | 404 UI |
| `route.ts` | API Route Handler |

---

## Data Fetching from FastAPI

### Pattern 1: Server Component Fetch (Recommended)

```tsx
// app/agents/page.tsx
const API_BASE = process.env.FASTAPI_URL || 'http://localhost:8000'

async function getAgents() {
  const res = await fetch(`${API_BASE}/api/agents`, {
    cache: 'no-store',  // Always fresh data
    headers: {
      'Content-Type': 'application/json',
    },
  })

  if (!res.ok) {
    throw new Error(`Failed to fetch agents: ${res.status}`)
  }

  return res.json()
}

export default async function AgentsPage() {
  const agents = await getAgents()

  return (
    <ul>
      {agents.map((agent: Agent) => (
        <li key={agent.id}>{agent.name}</li>
      ))}
    </ul>
  )
}
```

### Pattern 2: With Authentication Headers

```tsx
// lib/api.ts
import { cookies } from 'next/headers'

const API_BASE = process.env.FASTAPI_URL!

export async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const cookieStore = await cookies()
  const sessionToken = cookieStore.get('session_token')?.value

  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(sessionToken && { Authorization: `Bearer ${sessionToken}` }),
      ...options.headers,
    },
    cache: options.cache ?? 'no-store',
  })

  if (!res.ok) {
    const error = await res.json().catch(() => ({}))
    throw new Error(error.detail || `API Error: ${res.status}`)
  }

  return res.json()
}

// Usage in Server Component
const agents = await fetchAPI<Agent[]>('/api/agents')
```

### Pattern 3: Parallel Data Fetching

```tsx
// app/dashboard/page.tsx
export default async function Dashboard() {
  // Fetch in parallel - don't await sequentially!
  const [stats, recentCalls, agents] = await Promise.all([
    fetchAPI<Stats>('/api/stats'),
    fetchAPI<Call[]>('/api/calls/recent'),
    fetchAPI<Agent[]>('/api/agents'),
  ])

  return (
    <div className="grid grid-cols-3 gap-4">
      <StatsCard stats={stats} />
      <RecentCallsList calls={recentCalls} />
      <AgentsList agents={agents} />
    </div>
  )
}
```

---

## Server Actions (FastAPI Proxy Only)

Server Actions call FastAPI endpoints - they do NOT contain business logic.

### Pattern: Form Mutation

```tsx
// app/agents/actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { fetchAPI } from '@/lib/api'

export async function createAgent(formData: FormData) {
  const data = {
    name: formData.get('name') as string,
    prompt: formData.get('prompt') as string,
    voice_id: formData.get('voice_id') as string,
  }

  try {
    await fetchAPI('/api/agents', {
      method: 'POST',
      body: JSON.stringify(data),
    })

    revalidatePath('/agents')
    return { success: true }
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to create agent'
    }
  }
}

// app/agents/new/page.tsx
import { createAgent } from '../actions'

export default function NewAgentPage() {
  return (
    <form action={createAgent}>
      <input name="name" placeholder="Agent name" required />
      <textarea name="prompt" placeholder="System prompt" required />
      <select name="voice_id">
        <option value="voice1">Voice 1</option>
      </select>
      <button type="submit">Create Agent</button>
    </form>
  )
}
```

### Pattern: With Client-Side Feedback

```tsx
// components/create-agent-form.tsx
'use client'

import { useActionState } from 'react'
import { createAgent } from '@/app/agents/actions'
import { Button } from '@/components/ui/button'

export function CreateAgentForm() {
  const [state, formAction, isPending] = useActionState(createAgent, null)

  return (
    <form action={formAction}>
      <input name="name" disabled={isPending} />
      <Button type="submit" disabled={isPending}>
        {isPending ? 'Creating...' : 'Create Agent'}
      </Button>
      {state?.error && (
        <p className="text-red-500">{state.error}</p>
      )}
    </form>
  )
}
```

---

## Loading States

### Route-Level Loading (loading.tsx)

```tsx
// app/agents/loading.tsx
import { Skeleton } from '@/components/ui/skeleton'

export default function AgentsLoading() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-8 w-48" />
      <div className="grid gap-4">
        {[...Array(3)].map((_, i) => (
          <Skeleton key={i} className="h-24 w-full" />
        ))}
      </div>
    </div>
  )
}
```

### Component-Level Suspense

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react'
import { StatsCard, StatsCardSkeleton } from './stats-card'
import { CallsList, CallsListSkeleton } from './calls-list'

export default function Dashboard() {
  return (
    <div className="grid grid-cols-2 gap-4">
      <Suspense fallback={<StatsCardSkeleton />}>
        <StatsCard />
      </Suspense>
      <Suspense fallback={<CallsListSkeleton />}>
        <CallsList />
      </Suspense>
    </div>
  )
}

// Components fetch their own data
async function StatsCard() {
  const stats = await fetchAPI<Stats>('/api/stats')
  return <div>{/* render stats */}</div>
}
```

### Dynamic Route with Key

```tsx
// app/agents/[id]/page.tsx
import { Suspense } from 'react'

export default async function AgentPage({
  params
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params

  return (
    <Suspense key={id} fallback={<AgentSkeleton />}>
      <AgentDetails id={id} />
    </Suspense>
  )
}
```

---

## Error Handling

### error.tsx (Must be Client Component)

```tsx
// app/agents/error.tsx
'use client'

import { useEffect } from 'react'
import { Button } from '@/components/ui/button'

export default function AgentsError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error('Agents page error:', error)
  }, [error])

  return (
    <div className="flex flex-col items-center gap-4 p-8">
      <h2 className="text-xl font-semibold">Failed to load agents</h2>
      <p className="text-muted-foreground">
        {error.message || 'Something went wrong'}
      </p>
      <Button onClick={reset}>Try again</Button>
    </div>
  )
}
```

### Global Error Handler

```tsx
// app/global-error.tsx
'use client'

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <html>
      <body>
        <h2>Something went wrong!</h2>
        <button onClick={reset}>Try again</button>
      </body>
    </html>
  )
}
```

---

## Middleware & Authentication

### Better-Auth Integration

```tsx
// middleware.ts
import { NextRequest, NextResponse } from 'next/server'
import { getSessionCookie } from 'better-auth/cookies'

const protectedRoutes = ['/dashboard', '/agents', '/calls']
const authRoutes = ['/login', '/register']

export async function middleware(request: NextRequest) {
  const session = getSessionCookie(request)
  const { pathname } = request.nextUrl

  // Redirect authenticated users away from auth pages
  if (authRoutes.some(route => pathname.startsWith(route))) {
    if (session) {
      return NextResponse.redirect(new URL('/dashboard', request.url))
    }
    return NextResponse.next()
  }

  // Protect dashboard routes
  if (protectedRoutes.some(route => pathname.startsWith(route))) {
    if (!session) {
      const loginUrl = new URL('/login', request.url)
      loginUrl.searchParams.set('callbackUrl', pathname)
      return NextResponse.redirect(loginUrl)
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}
```

---

## Client-Side Data (TanStack Query)

For real-time updates or client-side polling:

```tsx
// providers/query-provider.tsx
'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () => new QueryClient({
      defaultOptions: {
        queries: {
          staleTime: 60 * 1000, // 1 minute
        },
      },
    })
  )

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}

// app/layout.tsx
import { QueryProvider } from '@/providers/query-provider'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  )
}
```

### Polling Example

```tsx
// components/live-call-status.tsx
'use client'

import { useQuery } from '@tanstack/react-query'

export function LiveCallStatus({ callId }: { callId: string }) {
  const { data, isLoading } = useQuery({
    queryKey: ['call', callId],
    queryFn: () =>
      fetch(`/api/proxy/calls/${callId}`).then(r => r.json()),
    refetchInterval: 2000, // Poll every 2 seconds
  })

  if (isLoading) return <span>Loading...</span>
  return <span>Status: {data?.status}</span>
}
```

---

## Performance Optimization

### Image Optimization

```tsx
import Image from 'next/image'

// Remote images require configuration
// next.config.ts
export default {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'your-cdn.com' },
    ],
  },
}

// Usage
<Image
  src="/avatar.png"
  alt="User avatar"
  width={40}
  height={40}
  priority  // For above-the-fold images
/>
```

### Font Optimization

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  )
}
```

### Dynamic Imports

```tsx
import dynamic from 'next/dynamic'

// Load heavy components only when needed
const Chart = dynamic(() => import('./chart'), {
  loading: () => <ChartSkeleton />,
  ssr: false,  // Client-only component
})
```

---

## Route Groups & Advanced Routing

### Route Groups (Organization Only)

```
app/
├── (marketing)/      # No /marketing in URL
│   ├── page.tsx      # /
│   └── about/page.tsx # /about
└── (app)/            # No /app in URL
    ├── layout.tsx    # Different layout
    └── dashboard/page.tsx  # /dashboard
```

### Parallel Routes (Simultaneous Rendering)

```
app/
├── layout.tsx
├── @sidebar/         # Slot
│   └── page.tsx
├── @main/            # Slot
│   └── page.tsx
└── page.tsx
```

```tsx
// app/layout.tsx
export default function Layout({
  sidebar,
  main,
}: {
  sidebar: React.ReactNode
  main: React.ReactNode
}) {
  return (
    <div className="flex">
      <aside>{sidebar}</aside>
      <main>{main}</main>
    </div>
  )
}
```

### Intercepting Routes (Modals)

```
app/
├── agents/
│   ├── page.tsx           # /agents (list)
│   └── [id]/page.tsx      # /agents/123 (full page)
└── @modal/
    └── (.)agents/[id]/    # Intercepts /agents/123
        └── page.tsx       # Shows as modal
```

---

## Common Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| DB queries in Server Component | Fetch from FastAPI endpoint |
| Business logic in Server Action | Call FastAPI, return result |
| `'use client'` on entire page | Add only to interactive leaf components |
| Sequential `await` calls | `Promise.all()` for parallel fetching |
| Disabling cache everywhere | Use `revalidatePath()` for mutations |
| Ignoring loading states | Always provide `loading.tsx` or Suspense |

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/api-patterns.md` | Detailed API consumption patterns |
| `references/component-patterns.md` | Server/Client component examples |
| `references/auth-patterns.md` | Better-Auth integration details |
| `references/tanstack-query.md` | Client-side data fetching |
