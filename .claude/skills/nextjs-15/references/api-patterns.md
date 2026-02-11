# API Consumption Patterns

Detailed patterns for consuming FastAPI from Next.js 15.

## API Client Setup

### Type-Safe API Client

```tsx
// lib/api/client.ts
import { cookies } from 'next/headers'

const API_BASE = process.env.FASTAPI_URL || 'http://localhost:8000'

export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public detail?: string
  ) {
    super(message)
    this.name = 'APIError'
  }
}

interface FetchOptions extends Omit<RequestInit, 'body'> {
  body?: Record<string, unknown>
}

export async function api<T>(
  endpoint: string,
  options: FetchOptions = {}
): Promise<T> {
  const cookieStore = await cookies()
  const token = cookieStore.get('session_token')?.value

  const { body, ...fetchOptions } = options

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...fetchOptions,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
    body: body ? JSON.stringify(body) : undefined,
    cache: options.cache ?? 'no-store',
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new APIError(
      errorData.message || `API Error: ${response.status}`,
      response.status,
      errorData.detail
    )
  }

  // Handle empty responses
  const text = await response.text()
  return text ? JSON.parse(text) : null
}

// Convenience methods
export const api = {
  get: <T>(endpoint: string, options?: FetchOptions) =>
    apiFetch<T>(endpoint, { ...options, method: 'GET' }),

  post: <T>(endpoint: string, body: Record<string, unknown>, options?: FetchOptions) =>
    apiFetch<T>(endpoint, { ...options, method: 'POST', body }),

  put: <T>(endpoint: string, body: Record<string, unknown>, options?: FetchOptions) =>
    apiFetch<T>(endpoint, { ...options, method: 'PUT', body }),

  patch: <T>(endpoint: string, body: Record<string, unknown>, options?: FetchOptions) =>
    apiFetch<T>(endpoint, { ...options, method: 'PATCH', body }),

  delete: <T>(endpoint: string, options?: FetchOptions) =>
    apiFetch<T>(endpoint, { ...options, method: 'DELETE' }),
}
```

### Usage Examples

```tsx
// app/agents/page.tsx
import { api } from '@/lib/api/client'
import { Agent } from '@/types/agent'

export default async function AgentsPage() {
  const agents = await api.get<Agent[]>('/api/agents')

  return (
    <ul>
      {agents.map(agent => (
        <li key={agent.id}>{agent.name}</li>
      ))}
    </ul>
  )
}
```

---

## Caching Strategies

### No Cache (Real-time Data)

```tsx
// Always get fresh data
const calls = await api.get<Call[]>('/api/calls', {
  cache: 'no-store'
})
```

### Time-Based Revalidation

```tsx
// Revalidate every 60 seconds
const stats = await fetch(`${API_BASE}/api/stats`, {
  next: { revalidate: 60 }
})
```

### Tag-Based Revalidation

```tsx
// Fetch with tag
const agents = await fetch(`${API_BASE}/api/agents`, {
  next: { tags: ['agents'] }
})

// In Server Action, revalidate tag
import { revalidateTag } from 'next/cache'

export async function createAgent(data: AgentInput) {
  await api.post('/api/agents', data)
  revalidateTag('agents')
}
```

### Path Revalidation

```tsx
import { revalidatePath } from 'next/cache'

export async function updateAgent(id: string, data: Partial<Agent>) {
  await api.patch(`/api/agents/${id}`, data)
  revalidatePath('/agents')        // Revalidate list
  revalidatePath(`/agents/${id}`)  // Revalidate detail
}
```

---

## Error Handling Patterns

### In Server Components

```tsx
// app/agents/page.tsx
import { notFound } from 'next/navigation'
import { APIError } from '@/lib/api/client'

export default async function AgentPage({
  params
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params

  try {
    const agent = await api.get<Agent>(`/api/agents/${id}`)
    return <AgentDetails agent={agent} />
  } catch (error) {
    if (error instanceof APIError && error.status === 404) {
      notFound()
    }
    throw error  // Re-throw to trigger error.tsx
  }
}
```

### In Server Actions

```tsx
// app/agents/actions.ts
'use server'

import { APIError } from '@/lib/api/client'

type ActionResult<T = void> =
  | { success: true; data?: T }
  | { success: false; error: string; field?: string }

export async function createAgent(
  formData: FormData
): Promise<ActionResult<Agent>> {
  const data = {
    name: formData.get('name') as string,
    prompt: formData.get('prompt') as string,
  }

  // Client-side validation
  if (!data.name || data.name.length < 3) {
    return {
      success: false,
      error: 'Name must be at least 3 characters',
      field: 'name'
    }
  }

  try {
    const agent = await api.post<Agent>('/api/agents', data)
    revalidatePath('/agents')
    return { success: true, data: agent }
  } catch (error) {
    if (error instanceof APIError) {
      return {
        success: false,
        error: error.detail || error.message,
        field: error.status === 409 ? 'name' : undefined
      }
    }
    return { success: false, error: 'Failed to create agent' }
  }
}
```

---

## Pagination Pattern

### Server Component with Search Params

```tsx
// app/calls/page.tsx
import { api } from '@/lib/api/client'
import { Pagination } from '@/components/pagination'

interface SearchParams {
  page?: string
  limit?: string
  status?: string
}

export default async function CallsPage({
  searchParams
}: {
  searchParams: Promise<SearchParams>
}) {
  const params = await searchParams
  const page = Number(params.page) || 1
  const limit = Number(params.limit) || 20

  const queryString = new URLSearchParams({
    page: String(page),
    limit: String(limit),
    ...(params.status && { status: params.status })
  }).toString()

  const { items, total, pages } = await api.get<PaginatedResponse<Call>>(
    `/api/calls?${queryString}`
  )

  return (
    <div>
      <CallsList calls={items} />
      <Pagination
        currentPage={page}
        totalPages={pages}
        baseUrl="/calls"
      />
    </div>
  )
}
```

### Pagination Component

```tsx
// components/pagination.tsx
'use client'

import { usePathname, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'

interface PaginationProps {
  currentPage: number
  totalPages: number
}

export function Pagination({ currentPage, totalPages }: PaginationProps) {
  const pathname = usePathname()
  const searchParams = useSearchParams()

  function createPageURL(page: number) {
    const params = new URLSearchParams(searchParams)
    params.set('page', String(page))
    return `${pathname}?${params.toString()}`
  }

  return (
    <div className="flex gap-2">
      <Button asChild disabled={currentPage <= 1}>
        <Link href={createPageURL(currentPage - 1)}>Previous</Link>
      </Button>
      <span className="flex items-center px-4">
        Page {currentPage} of {totalPages}
      </span>
      <Button asChild disabled={currentPage >= totalPages}>
        <Link href={createPageURL(currentPage + 1)}>Next</Link>
      </Button>
    </div>
  )
}
```

---

## File Upload Pattern

```tsx
// app/agents/[id]/actions.ts
'use server'

export async function uploadAgentAvatar(
  agentId: string,
  formData: FormData
): Promise<ActionResult<{ url: string }>> {
  const file = formData.get('avatar') as File

  if (!file || file.size === 0) {
    return { success: false, error: 'No file provided' }
  }

  if (file.size > 5 * 1024 * 1024) {
    return { success: false, error: 'File too large (max 5MB)' }
  }

  // Forward to FastAPI with multipart/form-data
  const apiFormData = new FormData()
  apiFormData.append('file', file)

  const response = await fetch(
    `${process.env.FASTAPI_URL}/api/agents/${agentId}/avatar`,
    {
      method: 'POST',
      body: apiFormData,
      headers: {
        // Don't set Content-Type - let browser set with boundary
        Authorization: `Bearer ${await getSessionToken()}`,
      },
    }
  )

  if (!response.ok) {
    return { success: false, error: 'Upload failed' }
  }

  const result = await response.json()
  revalidatePath(`/agents/${agentId}`)
  return { success: true, data: result }
}
```

---

## Streaming Responses

### Server-Sent Events from FastAPI

```tsx
// components/call-transcript-stream.tsx
'use client'

import { useEffect, useState } from 'react'

export function CallTranscriptStream({ callId }: { callId: string }) {
  const [transcript, setTranscript] = useState<string[]>([])

  useEffect(() => {
    const eventSource = new EventSource(
      `${process.env.NEXT_PUBLIC_API_URL}/api/calls/${callId}/stream`
    )

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setTranscript(prev => [...prev, data.text])
    }

    eventSource.onerror = () => {
      eventSource.close()
    }

    return () => eventSource.close()
  }, [callId])

  return (
    <div className="space-y-2">
      {transcript.map((line, i) => (
        <p key={i}>{line}</p>
      ))}
    </div>
  )
}
```

---

## Route Handler as BFF Proxy

When you need client-side access to FastAPI:

```tsx
// app/api/proxy/[...path]/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { cookies } from 'next/headers'

const API_BASE = process.env.FASTAPI_URL!

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path } = await params
  const endpoint = path.join('/')

  const cookieStore = await cookies()
  const token = cookieStore.get('session_token')?.value

  const response = await fetch(`${API_BASE}/api/${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    },
  })

  const data = await response.json()
  return NextResponse.json(data, { status: response.status })
}

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path } = await params
  const endpoint = path.join('/')
  const body = await request.json()

  const cookieStore = await cookies()
  const token = cookieStore.get('session_token')?.value

  const response = await fetch(`${API_BASE}/api/${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    },
    body: JSON.stringify(body),
  })

  const data = await response.json()
  return NextResponse.json(data, { status: response.status })
}
```

Usage from client:

```tsx
// Client component can now call /api/proxy/agents
const response = await fetch('/api/proxy/agents')
```
