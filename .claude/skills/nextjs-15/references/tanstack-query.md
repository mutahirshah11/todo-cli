# TanStack Query Patterns

Client-side data fetching with TanStack Query (React Query) in Next.js 15.

## When to Use TanStack Query

| Use TanStack Query | Use Server Components |
|--------------------|----------------------|
| Real-time polling | Initial page data |
| Optimistic updates | SEO-critical content |
| Client-side mutations | Static data |
| Complex caching needs | Simple display |
| Infinite scroll | Server-rendered lists |

**Rule**: Server Components for initial render, TanStack Query for client lifecycle.

---

## Setup

### Provider Configuration

```tsx
// providers/query-provider.tsx
'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { useState } from 'react'

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            // Don't refetch immediately after SSR
            staleTime: 60 * 1000,
            // Retry failed requests 3 times
            retry: 3,
            // Refetch on window focus in production
            refetchOnWindowFocus: process.env.NODE_ENV === 'production',
          },
          mutations: {
            // Retry mutations once
            retry: 1,
          },
        },
      })
  )

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      {process.env.NODE_ENV === 'development' && (
        <ReactQueryDevtools initialIsOpen={false} />
      )}
    </QueryClientProvider>
  )
}
```

### Root Layout Integration

```tsx
// app/layout.tsx
import { QueryProvider } from '@/providers/query-provider'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  )
}
```

---

## API Client for Client Components

```tsx
// lib/api/client-api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || '/api/proxy'

export class ClientAPIError extends Error {
  constructor(
    message: string,
    public status: number
  ) {
    super(message)
  }
}

export async function clientFetch<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new ClientAPIError(
      error.message || `Error: ${response.status}`,
      response.status
    )
  }

  return response.json()
}
```

---

## Query Patterns

### Basic Query

```tsx
// hooks/use-agents.ts
import { useQuery } from '@tanstack/react-query'
import { clientFetch } from '@/lib/api/client-api'
import { Agent } from '@/types/agent'

export function useAgents() {
  return useQuery({
    queryKey: ['agents'],
    queryFn: () => clientFetch<Agent[]>('/agents'),
  })
}

// Usage
function AgentSelector() {
  const { data: agents, isLoading, error } = useAgents()

  if (isLoading) return <Spinner />
  if (error) return <Error message={error.message} />

  return (
    <select>
      {agents?.map(agent => (
        <option key={agent.id} value={agent.id}>
          {agent.name}
        </option>
      ))}
    </select>
  )
}
```

### Query with Parameters

```tsx
// hooks/use-agent.ts
export function useAgent(id: string) {
  return useQuery({
    queryKey: ['agents', id],
    queryFn: () => clientFetch<Agent>(`/agents/${id}`),
    enabled: !!id, // Don't fetch if no ID
  })
}

// hooks/use-calls.ts
interface UseCallsParams {
  agentId?: string
  status?: string
  page?: number
}

export function useCalls(params: UseCallsParams) {
  return useQuery({
    queryKey: ['calls', params],
    queryFn: () => {
      const searchParams = new URLSearchParams()
      if (params.agentId) searchParams.set('agent_id', params.agentId)
      if (params.status) searchParams.set('status', params.status)
      if (params.page) searchParams.set('page', String(params.page))

      return clientFetch<PaginatedResponse<Call>>(
        `/calls?${searchParams.toString()}`
      )
    },
  })
}
```

---

## Polling for Real-Time Data

```tsx
// components/live-call-status.tsx
'use client'

import { useQuery } from '@tanstack/react-query'
import { clientFetch } from '@/lib/api/client-api'

interface LiveCallStatusProps {
  callId: string
}

export function LiveCallStatus({ callId }: LiveCallStatusProps) {
  const { data: call, isLoading } = useQuery({
    queryKey: ['calls', callId, 'live'],
    queryFn: () => clientFetch<Call>(`/calls/${callId}`),
    refetchInterval: (query) => {
      // Poll every 2s while call is active, stop when completed
      const status = query.state.data?.status
      if (status === 'completed' || status === 'failed') {
        return false // Stop polling
      }
      return 2000 // Poll every 2 seconds
    },
  })

  if (isLoading) {
    return <span className="text-muted-foreground">Loading...</span>
  }

  return (
    <div className="flex items-center gap-2">
      <StatusBadge status={call?.status} />
      {call?.status === 'in_progress' && (
        <span className="text-sm text-muted-foreground">
          Duration: {call.duration}s
        </span>
      )}
    </div>
  )
}
```

---

## Mutations

### Basic Mutation

```tsx
// hooks/use-create-agent.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { clientFetch } from '@/lib/api/client-api'
import { toast } from 'sonner'

interface CreateAgentInput {
  name: string
  prompt: string
  voice_id: string
}

export function useCreateAgent() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: CreateAgentInput) =>
      clientFetch<Agent>('/agents', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    onSuccess: (newAgent) => {
      // Add to cache
      queryClient.setQueryData<Agent[]>(['agents'], (old) =>
        old ? [...old, newAgent] : [newAgent]
      )
      toast.success('Agent created successfully')
    },
    onError: (error) => {
      toast.error(error.message)
    },
  })
}

// Usage
function CreateAgentButton() {
  const createAgent = useCreateAgent()

  return (
    <Button
      onClick={() => createAgent.mutate({
        name: 'New Agent',
        prompt: 'You are a helpful assistant',
        voice_id: 'alloy',
      })}
      disabled={createAgent.isPending}
    >
      {createAgent.isPending ? 'Creating...' : 'Create Agent'}
    </Button>
  )
}
```

### Mutation with Form

```tsx
// components/agents/quick-create-form.tsx
'use client'

import { useCreateAgent } from '@/hooks/use-create-agent'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export function QuickCreateForm() {
  const router = useRouter()
  const createAgent = useCreateAgent()

  useEffect(() => {
    if (createAgent.isSuccess) {
      router.push(`/agents/${createAgent.data.id}`)
    }
  }, [createAgent.isSuccess, createAgent.data, router])

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)

    createAgent.mutate({
      name: formData.get('name') as string,
      prompt: formData.get('prompt') as string,
      voice_id: formData.get('voice_id') as string,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input name="name" placeholder="Agent name" required />
      <Textarea name="prompt" placeholder="System prompt" required />
      <select name="voice_id">
        <option value="alloy">Alloy</option>
        <option value="echo">Echo</option>
      </select>

      {createAgent.error && (
        <p className="text-sm text-destructive">{createAgent.error.message}</p>
      )}

      <Button type="submit" disabled={createAgent.isPending}>
        {createAgent.isPending ? 'Creating...' : 'Create'}
      </Button>
    </form>
  )
}
```

---

## Optimistic Updates

```tsx
// hooks/use-update-agent.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'

export function useUpdateAgent(agentId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: Partial<Agent>) =>
      clientFetch<Agent>(`/agents/${agentId}`, {
        method: 'PATCH',
        body: JSON.stringify(data),
      }),

    // Optimistic update
    onMutate: async (newData) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['agents', agentId] })

      // Snapshot previous value
      const previousAgent = queryClient.getQueryData<Agent>(['agents', agentId])

      // Optimistically update
      queryClient.setQueryData<Agent>(['agents', agentId], (old) =>
        old ? { ...old, ...newData } : old
      )

      // Return context for rollback
      return { previousAgent }
    },

    // Rollback on error
    onError: (err, newData, context) => {
      if (context?.previousAgent) {
        queryClient.setQueryData(['agents', agentId], context.previousAgent)
      }
      toast.error('Failed to update agent')
    },

    // Refetch after success or error
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['agents', agentId] })
    },
  })
}
```

---

## Infinite Scroll

```tsx
// hooks/use-infinite-calls.ts
import { useInfiniteQuery } from '@tanstack/react-query'

export function useInfiniteCalls(agentId?: string) {
  return useInfiniteQuery({
    queryKey: ['calls', 'infinite', agentId],
    queryFn: async ({ pageParam = 1 }) => {
      const params = new URLSearchParams({
        page: String(pageParam),
        limit: '20',
      })
      if (agentId) params.set('agent_id', agentId)

      return clientFetch<PaginatedResponse<Call>>(`/calls?${params}`)
    },
    getNextPageParam: (lastPage, pages) =>
      lastPage.hasMore ? pages.length + 1 : undefined,
    initialPageParam: 1,
  })
}

// components/calls/infinite-calls-list.tsx
'use client'

import { useInfiniteCalls } from '@/hooks/use-infinite-calls'
import { useInView } from 'react-intersection-observer'
import { useEffect } from 'react'

export function InfiniteCallsList({ agentId }: { agentId?: string }) {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
  } = useInfiniteCalls(agentId)

  const { ref, inView } = useInView()

  useEffect(() => {
    if (inView && hasNextPage) {
      fetchNextPage()
    }
  }, [inView, hasNextPage, fetchNextPage])

  if (isLoading) return <CallsListSkeleton />

  return (
    <div className="space-y-4">
      {data?.pages.map((page, i) => (
        <div key={i} className="space-y-2">
          {page.items.map(call => (
            <CallCard key={call.id} call={call} />
          ))}
        </div>
      ))}

      <div ref={ref} className="h-10 flex items-center justify-center">
        {isFetchingNextPage && <Spinner />}
      </div>
    </div>
  )
}
```

---

## Prefetching

### On Hover

```tsx
// components/agents/agent-card.tsx
'use client'

import { useQueryClient } from '@tanstack/react-query'
import Link from 'next/link'
import { clientFetch } from '@/lib/api/client-api'

export function AgentCard({ agent }: { agent: Agent }) {
  const queryClient = useQueryClient()

  function prefetchAgent() {
    queryClient.prefetchQuery({
      queryKey: ['agents', agent.id],
      queryFn: () => clientFetch<Agent>(`/agents/${agent.id}`),
      staleTime: 60 * 1000,
    })
  }

  return (
    <Link
      href={`/agents/${agent.id}`}
      onMouseEnter={prefetchAgent}
      onFocus={prefetchAgent}
      className="block p-4 border rounded-lg hover:border-primary"
    >
      <h3 className="font-medium">{agent.name}</h3>
      <p className="text-sm text-muted-foreground">{agent.description}</p>
    </Link>
  )
}
```

---

## Hydration from Server Components

### Pattern: Server Fetch + Client Hydration

```tsx
// app/agents/page.tsx (Server Component)
import { api } from '@/lib/api/client'
import { HydrateClient } from '@/providers/hydrate-client'
import { AgentsClientView } from './agents-client-view'

export default async function AgentsPage() {
  // Fetch on server
  const agents = await api.get<Agent[]>('/api/agents')

  return (
    <HydrateClient
      queries={[
        {
          queryKey: ['agents'],
          state: { data: agents },
        },
      ]}
    >
      <AgentsClientView />
    </HydrateClient>
  )
}

// providers/hydrate-client.tsx
'use client'

import { HydrationBoundary, dehydrate, QueryClient } from '@tanstack/react-query'
import { useMemo } from 'react'

interface HydrateClientProps {
  queries: Array<{
    queryKey: unknown[]
    state: { data: unknown }
  }>
  children: React.ReactNode
}

export function HydrateClient({ queries, children }: HydrateClientProps) {
  const dehydratedState = useMemo(() => {
    const queryClient = new QueryClient()

    for (const query of queries) {
      queryClient.setQueryData(query.queryKey, query.state.data)
    }

    return dehydrate(queryClient)
  }, [queries])

  return (
    <HydrationBoundary state={dehydratedState}>
      {children}
    </HydrationBoundary>
  )
}
```

---

## Query Keys Best Practices

```tsx
// lib/query-keys.ts
export const queryKeys = {
  // Agents
  agents: {
    all: ['agents'] as const,
    lists: () => [...queryKeys.agents.all, 'list'] as const,
    list: (filters: AgentFilters) =>
      [...queryKeys.agents.lists(), filters] as const,
    details: () => [...queryKeys.agents.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.agents.details(), id] as const,
  },

  // Calls
  calls: {
    all: ['calls'] as const,
    lists: () => [...queryKeys.calls.all, 'list'] as const,
    list: (filters: CallFilters) =>
      [...queryKeys.calls.lists(), filters] as const,
    infinite: (filters: CallFilters) =>
      [...queryKeys.calls.all, 'infinite', filters] as const,
    details: () => [...queryKeys.calls.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.calls.details(), id] as const,
  },
}

// Usage
useQuery({
  queryKey: queryKeys.agents.detail(agentId),
  queryFn: () => clientFetch(`/agents/${agentId}`),
})

// Invalidate all agent queries
queryClient.invalidateQueries({ queryKey: queryKeys.agents.all })

// Invalidate specific agent
queryClient.invalidateQueries({ queryKey: queryKeys.agents.detail(agentId) })
```
