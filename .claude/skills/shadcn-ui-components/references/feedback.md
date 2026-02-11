# Feedback Components

Toast notifications (Sonner), alerts, and badges for user feedback.

## Installation

```bash
npx shadcn@latest add sonner alert badge
```

## Sonner (Toast Notifications)

shadcn/ui uses Sonner for toast notifications.

### Setup

Add the Toaster component to your root layout:

```tsx
// app/layout.tsx
import { Toaster } from "@/components/ui/sonner"

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Toaster />
      </body>
    </html>
  )
}
```

### Basic Usage

```tsx
import { toast } from "sonner"

// Success
toast.success("Profile updated")

// Error
toast.error("Failed to save changes")

// Warning
toast.warning("Your session is about to expire")

// Info
toast.info("New features available")

// Default (neutral)
toast("Event has been created")

// Loading
toast.loading("Saving...")
```

### Toast with Description

```tsx
toast.success("Changes saved", {
  description: "Your profile has been updated successfully.",
})
```

### Toast with Action

```tsx
toast("Item deleted", {
  action: {
    label: "Undo",
    onClick: () => restoreItem(),
  },
})
```

### Toast with Cancel

```tsx
toast("Confirm deletion", {
  action: {
    label: "Delete",
    onClick: () => deleteItem(),
  },
  cancel: {
    label: "Cancel",
    onClick: () => console.log("Cancelled"),
  },
})
```

### Promise Toast

Automatic loading, success, and error states:

```tsx
const promise = saveSettings()

toast.promise(promise, {
  loading: "Saving settings...",
  success: "Settings saved!",
  error: "Failed to save settings",
})
```

### Custom Duration

```tsx
// 5 seconds
toast.success("Saved", { duration: 5000 })

// Infinite (must be dismissed manually)
toast.info("Important notice", { duration: Infinity })
```

### Dismissing Toasts

```tsx
// Dismiss specific toast
const toastId = toast.loading("Loading...")
toast.dismiss(toastId)

// Dismiss all toasts
toast.dismiss()
```

### Rich Content Toast

```tsx
toast.custom((t) => (
  <div className="flex items-center gap-2 bg-background p-4 rounded-lg border">
    <Avatar>
      <AvatarImage src={user.avatar} />
      <AvatarFallback>{user.initials}</AvatarFallback>
    </Avatar>
    <div>
      <p className="font-medium">{user.name}</p>
      <p className="text-sm text-muted-foreground">Sent you a message</p>
    </div>
  </div>
))
```

### Position Configuration

```tsx
// In layout
<Toaster position="top-right" />
<Toaster position="top-center" />
<Toaster position="top-left" />
<Toaster position="bottom-right" />
<Toaster position="bottom-center" />
<Toaster position="bottom-left" />
```

### Theme Integration

```tsx
<Toaster
  theme="system" // or "light" | "dark"
  richColors // Enable rich colors for success/error/etc
  closeButton // Show close button on all toasts
  expand={false} // Stack toasts
/>
```

## Alert Component

Inline, persistent alerts for important information.

### Basic Alerts

```tsx
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Terminal, AlertCircle, CheckCircle, Info } from "lucide-react"

// Default
<Alert>
  <Terminal className="h-4 w-4" />
  <AlertTitle>Heads up!</AlertTitle>
  <AlertDescription>
    You can add components to your app using the CLI.
  </AlertDescription>
</Alert>

// Destructive
<Alert variant="destructive">
  <AlertCircle className="h-4 w-4" />
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>
    Your session has expired. Please log in again.
  </AlertDescription>
</Alert>
```

### Alert Variants

```tsx
// Success (custom)
<Alert className="border-green-500 bg-green-50 dark:bg-green-950">
  <CheckCircle className="h-4 w-4 text-green-600" />
  <AlertTitle className="text-green-800 dark:text-green-200">Success</AlertTitle>
  <AlertDescription className="text-green-700 dark:text-green-300">
    Your changes have been saved.
  </AlertDescription>
</Alert>

// Warning (custom)
<Alert className="border-yellow-500 bg-yellow-50 dark:bg-yellow-950">
  <AlertCircle className="h-4 w-4 text-yellow-600" />
  <AlertTitle className="text-yellow-800 dark:text-yellow-200">Warning</AlertTitle>
  <AlertDescription className="text-yellow-700 dark:text-yellow-300">
    Your account is about to expire.
  </AlertDescription>
</Alert>

// Info (custom)
<Alert className="border-blue-500 bg-blue-50 dark:bg-blue-950">
  <Info className="h-4 w-4 text-blue-600" />
  <AlertTitle className="text-blue-800 dark:text-blue-200">Info</AlertTitle>
  <AlertDescription className="text-blue-700 dark:text-blue-300">
    New features are available in this version.
  </AlertDescription>
</Alert>
```

### Dismissible Alert

```tsx
"use client"

import { useState } from "react"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { X } from "lucide-react"
import { Button } from "@/components/ui/button"

export function DismissibleAlert() {
  const [isVisible, setIsVisible] = useState(true)

  if (!isVisible) return null

  return (
    <Alert className="relative">
      <AlertTitle>Notice</AlertTitle>
      <AlertDescription>
        This is an important message.
      </AlertDescription>
      <Button
        variant="ghost"
        size="icon"
        className="absolute top-2 right-2 h-6 w-6"
        onClick={() => setIsVisible(false)}
      >
        <X className="h-4 w-4" />
      </Button>
    </Alert>
  )
}
```

### Alert with Action

```tsx
<Alert>
  <AlertCircle className="h-4 w-4" />
  <AlertTitle>Subscription expiring</AlertTitle>
  <AlertDescription className="flex items-center justify-between">
    <span>Your subscription expires in 3 days.</span>
    <Button size="sm" variant="outline" className="ml-4">
      Renew now
    </Button>
  </AlertDescription>
</Alert>
```

## Badge Component

Status indicators and labels.

### Basic Badges

```tsx
import { Badge } from "@/components/ui/badge"

<Badge>Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="outline">Outline</Badge>
<Badge variant="destructive">Destructive</Badge>
```

### Status Badges

```tsx
// Custom status badges
function StatusBadge({ status }: { status: string }) {
  const variants = {
    pending: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200",
    active: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200",
    inactive: "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200",
    error: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200",
  }

  return (
    <Badge className={variants[status] || variants.inactive}>
      {status}
    </Badge>
  )
}

// Usage
<StatusBadge status="active" />
<StatusBadge status="pending" />
<StatusBadge status="error" />
```

### Badge with Icon

```tsx
import { Badge } from "@/components/ui/badge"
import { Check, Clock, X } from "lucide-react"

<Badge className="gap-1">
  <Check className="h-3 w-3" />
  Verified
</Badge>

<Badge variant="secondary" className="gap-1">
  <Clock className="h-3 w-3" />
  Pending
</Badge>

<Badge variant="destructive" className="gap-1">
  <X className="h-3 w-3" />
  Failed
</Badge>
```

### Notification Badge

```tsx
import { Badge } from "@/components/ui/badge"
import { Bell } from "lucide-react"
import { Button } from "@/components/ui/button"

function NotificationButton({ count }: { count: number }) {
  return (
    <Button variant="outline" size="icon" className="relative">
      <Bell className="h-4 w-4" />
      {count > 0 && (
        <Badge
          className="absolute -top-2 -right-2 h-5 w-5 rounded-full p-0 flex items-center justify-center"
          variant="destructive"
        >
          {count > 99 ? "99+" : count}
        </Badge>
      )}
    </Button>
  )
}
```

### Badge as Link

```tsx
import Link from "next/link"
import { Badge } from "@/components/ui/badge"

<Badge asChild>
  <Link href="/docs">Documentation</Link>
</Badge>
```

## When to Use What

| Component | Use For | Duration |
|-----------|---------|----------|
| **Toast (Sonner)** | Non-blocking feedback for actions | Temporary (auto-dismiss) |
| **Alert** | Important info user must acknowledge | Persistent |
| **Badge** | Status indicators, counts, labels | Always visible |

### Decision Guide

```
User performed an action?
  ├─ Success/failure feedback → Toast
  └─ No action, just info
      ├─ Requires attention now → Alert
      └─ Status/label → Badge

Is it temporary?
  ├─ Yes → Toast
  └─ No → Alert or Badge
```

## Integration Examples

### Form Submission Feedback

```tsx
async function onSubmit(values) {
  try {
    await saveData(values)
    toast.success("Saved successfully")
  } catch (error) {
    toast.error("Failed to save", {
      description: error.message,
    })
  }
}
```

### Real-time Updates

```tsx
function useRealtimeUpdates() {
  useEffect(() => {
    const unsubscribe = subscribeToUpdates((update) => {
      toast.info(`New update: ${update.title}`, {
        action: {
          label: "View",
          onClick: () => router.push(`/updates/${update.id}`),
        },
      })
    })
    return unsubscribe
  }, [])
}
```

### Async Operation with Progress

```tsx
async function uploadFiles(files: File[]) {
  const toastId = toast.loading(`Uploading ${files.length} files...`)

  try {
    for (let i = 0; i < files.length; i++) {
      await uploadFile(files[i])
      toast.loading(`Uploading ${i + 1}/${files.length}...`, { id: toastId })
    }
    toast.success("All files uploaded!", { id: toastId })
  } catch (error) {
    toast.error("Upload failed", { id: toastId })
  }
}
```

## Best Practices

### Toast
- Keep messages short and actionable
- Use appropriate variants (success/error/warning)
- Provide undo for destructive actions
- Don't spam toasts - batch if multiple actions

### Alert
- Use sparingly for important information
- Provide clear next steps or actions
- Use appropriate severity colors
- Consider dismissibility for non-critical alerts

### Badge
- Keep text short (1-2 words)
- Use consistent colors for same meanings
- Consider accessibility (don't rely on color alone)
