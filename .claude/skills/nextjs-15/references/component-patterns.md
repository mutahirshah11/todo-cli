# Component Patterns

Server and Client Component patterns for Next.js 15 with FastAPI backend.

## Server Component Patterns

### Data Display Component

```tsx
// components/agents/agent-list.tsx
import { api } from '@/lib/api/client'
import { Agent } from '@/types/agent'
import { AgentCard } from './agent-card'

export async function AgentList() {
  const agents = await api.get<Agent[]>('/api/agents')

  if (agents.length === 0) {
    return (
      <div className="text-center py-12 text-muted-foreground">
        No agents found. Create your first agent to get started.
      </div>
    )
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {agents.map(agent => (
        <AgentCard key={agent.id} agent={agent} />
      ))}
    </div>
  )
}
```

### Detail Component with Error Handling

```tsx
// components/agents/agent-details.tsx
import { notFound } from 'next/navigation'
import { api, APIError } from '@/lib/api/client'
import { Agent } from '@/types/agent'

interface AgentDetailsProps {
  id: string
}

export async function AgentDetails({ id }: AgentDetailsProps) {
  let agent: Agent

  try {
    agent = await api.get<Agent>(`/api/agents/${id}`)
  } catch (error) {
    if (error instanceof APIError && error.status === 404) {
      notFound()
    }
    throw error
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">{agent.name}</h1>
        <p className="text-muted-foreground">{agent.description}</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <h2 className="font-semibold mb-2">Configuration</h2>
          <dl className="space-y-1">
            <div className="flex justify-between">
              <dt>Voice</dt>
              <dd>{agent.voice_id}</dd>
            </div>
            <div className="flex justify-between">
              <dt>Language</dt>
              <dd>{agent.language}</dd>
            </div>
          </dl>
        </div>

        <div>
          <h2 className="font-semibold mb-2">System Prompt</h2>
          <pre className="bg-muted p-4 rounded text-sm whitespace-pre-wrap">
            {agent.prompt}
          </pre>
        </div>
      </div>
    </div>
  )
}
```

### Async Component with Props from Parent

```tsx
// components/calls/call-summary.tsx
interface CallSummaryProps {
  agentId: string
  dateRange?: { from: Date; to: Date }
}

export async function CallSummary({ agentId, dateRange }: CallSummaryProps) {
  const params = new URLSearchParams({ agent_id: agentId })
  if (dateRange) {
    params.set('from', dateRange.from.toISOString())
    params.set('to', dateRange.to.toISOString())
  }

  const summary = await api.get<CallSummaryData>(
    `/api/calls/summary?${params}`
  )

  return (
    <div className="grid grid-cols-3 gap-4">
      <StatCard label="Total Calls" value={summary.total} />
      <StatCard label="Avg Duration" value={`${summary.avgDuration}s`} />
      <StatCard label="Success Rate" value={`${summary.successRate}%`} />
    </div>
  )
}
```

---

## Client Component Patterns

### Interactive Form

```tsx
// components/agents/create-agent-form.tsx
'use client'

import { useActionState } from 'react'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
import { createAgent } from '@/app/agents/actions'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { toast } from 'sonner'

export function CreateAgentForm() {
  const router = useRouter()
  const [state, formAction, isPending] = useActionState(createAgent, null)

  useEffect(() => {
    if (state?.success) {
      toast.success('Agent created successfully')
      router.push('/agents')
    } else if (state?.error) {
      toast.error(state.error)
    }
  }, [state, router])

  return (
    <form action={formAction} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="name">Name</Label>
        <Input
          id="name"
          name="name"
          placeholder="My Agent"
          disabled={isPending}
          aria-describedby={state?.field === 'name' ? 'name-error' : undefined}
        />
        {state?.field === 'name' && (
          <p id="name-error" className="text-sm text-destructive">
            {state.error}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="prompt">System Prompt</Label>
        <Textarea
          id="prompt"
          name="prompt"
          placeholder="You are a helpful assistant..."
          rows={6}
          disabled={isPending}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="voice_id">Voice</Label>
        <select
          id="voice_id"
          name="voice_id"
          className="w-full rounded-md border p-2"
          disabled={isPending}
        >
          <option value="alloy">Alloy</option>
          <option value="echo">Echo</option>
          <option value="nova">Nova</option>
        </select>
      </div>

      <Button type="submit" disabled={isPending}>
        {isPending ? 'Creating...' : 'Create Agent'}
      </Button>
    </form>
  )
}
```

### Filter/Search Component

```tsx
// components/calls/call-filters.tsx
'use client'

import { useRouter, useSearchParams, usePathname } from 'next/navigation'
import { useCallback, useTransition } from 'react'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { useDebouncedCallback } from 'use-debounce'

export function CallFilters() {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()
  const [isPending, startTransition] = useTransition()

  const updateParams = useCallback(
    (key: string, value: string) => {
      const params = new URLSearchParams(searchParams)
      if (value) {
        params.set(key, value)
      } else {
        params.delete(key)
      }
      params.set('page', '1') // Reset to first page on filter change

      startTransition(() => {
        router.push(`${pathname}?${params.toString()}`)
      })
    },
    [searchParams, pathname, router]
  )

  const handleSearch = useDebouncedCallback((term: string) => {
    updateParams('search', term)
  }, 300)

  return (
    <div className="flex gap-4 items-center">
      <Input
        placeholder="Search calls..."
        defaultValue={searchParams.get('search') || ''}
        onChange={(e) => handleSearch(e.target.value)}
        className="max-w-sm"
      />

      <Select
        value={searchParams.get('status') || 'all'}
        onValueChange={(value) => updateParams('status', value === 'all' ? '' : value)}
      >
        <SelectTrigger className="w-40">
          <SelectValue placeholder="Status" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All Status</SelectItem>
          <SelectItem value="completed">Completed</SelectItem>
          <SelectItem value="failed">Failed</SelectItem>
          <SelectItem value="in_progress">In Progress</SelectItem>
        </SelectContent>
      </Select>

      {isPending && (
        <span className="text-sm text-muted-foreground">Loading...</span>
      )}
    </div>
  )
}
```

### Modal Component

```tsx
// components/agents/delete-agent-dialog.tsx
'use client'

import { useState, useTransition } from 'react'
import { useRouter } from 'next/navigation'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog'
import { Button } from '@/components/ui/button'
import { deleteAgent } from '@/app/agents/actions'
import { toast } from 'sonner'

interface DeleteAgentDialogProps {
  agentId: string
  agentName: string
}

export function DeleteAgentDialog({ agentId, agentName }: DeleteAgentDialogProps) {
  const [open, setOpen] = useState(false)
  const [isPending, startTransition] = useTransition()
  const router = useRouter()

  async function handleDelete() {
    startTransition(async () => {
      const result = await deleteAgent(agentId)

      if (result.success) {
        toast.success('Agent deleted')
        setOpen(false)
        router.push('/agents')
      } else {
        toast.error(result.error)
      }
    })
  }

  return (
    <AlertDialog open={open} onOpenChange={setOpen}>
      <AlertDialogTrigger asChild>
        <Button variant="destructive">Delete</Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Delete {agentName}?</AlertDialogTitle>
          <AlertDialogDescription>
            This action cannot be undone. This will permanently delete the
            agent and all associated call history.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel disabled={isPending}>Cancel</AlertDialogCancel>
          <AlertDialogAction
            onClick={handleDelete}
            disabled={isPending}
            className="bg-destructive hover:bg-destructive/90"
          >
            {isPending ? 'Deleting...' : 'Delete'}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}
```

---

## Hybrid Patterns

### Server Component with Client Interactivity

```tsx
// app/agents/[id]/page.tsx (Server Component)
import { Suspense } from 'react'
import { AgentDetails } from '@/components/agents/agent-details'
import { AgentActions } from '@/components/agents/agent-actions'
import { AgentDetailsSkeleton } from '@/components/agents/agent-details-skeleton'

export default async function AgentPage({
  params
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params

  return (
    <div className="space-y-6">
      <Suspense fallback={<AgentDetailsSkeleton />}>
        <AgentDetails id={id} />
      </Suspense>

      {/* Client component for actions */}
      <AgentActions agentId={id} />
    </div>
  )
}

// components/agents/agent-actions.tsx (Client Component)
'use client'

import { Button } from '@/components/ui/button'
import { DeleteAgentDialog } from './delete-agent-dialog'
import Link from 'next/link'

export function AgentActions({ agentId }: { agentId: string }) {
  return (
    <div className="flex gap-2">
      <Button asChild>
        <Link href={`/agents/${agentId}/edit`}>Edit</Link>
      </Button>
      <Button variant="outline" asChild>
        <Link href={`/agents/${agentId}/test`}>Test Call</Link>
      </Button>
      <DeleteAgentDialog agentId={agentId} agentName="Agent" />
    </div>
  )
}
```

### Data Table with Server Data + Client Sorting

```tsx
// app/calls/page.tsx (Server Component)
import { api } from '@/lib/api/client'
import { CallsDataTable } from '@/components/calls/calls-data-table'

export default async function CallsPage() {
  const calls = await api.get<Call[]>('/api/calls')

  // Pass server-fetched data to client component for interactivity
  return <CallsDataTable initialData={calls} />
}

// components/calls/calls-data-table.tsx (Client Component)
'use client'

import { useState, useMemo } from 'react'
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  SortingState,
} from '@tanstack/react-table'
import { columns } from './columns'
import { DataTable } from '@/components/ui/data-table'

interface CallsDataTableProps {
  initialData: Call[]
}

export function CallsDataTable({ initialData }: CallsDataTableProps) {
  const [sorting, setSorting] = useState<SortingState>([])

  const table = useReactTable({
    data: initialData,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    onSortingChange: setSorting,
    state: { sorting },
  })

  return <DataTable table={table} />
}
```

---

## Context Provider Pattern

```tsx
// providers/agent-context.tsx
'use client'

import { createContext, useContext, ReactNode } from 'react'
import { Agent } from '@/types/agent'

interface AgentContextType {
  agent: Agent
}

const AgentContext = createContext<AgentContextType | null>(null)

export function AgentProvider({
  agent,
  children
}: {
  agent: Agent
  children: ReactNode
}) {
  return (
    <AgentContext.Provider value={{ agent }}>
      {children}
    </AgentContext.Provider>
  )
}

export function useAgent() {
  const context = useContext(AgentContext)
  if (!context) {
    throw new Error('useAgent must be used within AgentProvider')
  }
  return context
}

// app/agents/[id]/layout.tsx (Server Component)
import { api } from '@/lib/api/client'
import { AgentProvider } from '@/providers/agent-context'

export default async function AgentLayout({
  children,
  params,
}: {
  children: React.ReactNode
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const agent = await api.get<Agent>(`/api/agents/${id}`)

  return (
    <AgentProvider agent={agent}>
      {children}
    </AgentProvider>
  )
}
```

---

## Skeleton Components

```tsx
// components/agents/agent-card-skeleton.tsx
import { Skeleton } from '@/components/ui/skeleton'
import { Card, CardContent, CardHeader } from '@/components/ui/card'

export function AgentCardSkeleton() {
  return (
    <Card>
      <CardHeader>
        <Skeleton className="h-6 w-32" />
        <Skeleton className="h-4 w-48" />
      </CardHeader>
      <CardContent className="space-y-2">
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-3/4" />
      </CardContent>
    </Card>
  )
}

export function AgentListSkeleton() {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {[...Array(6)].map((_, i) => (
        <AgentCardSkeleton key={i} />
      ))}
    </div>
  )
}
```
