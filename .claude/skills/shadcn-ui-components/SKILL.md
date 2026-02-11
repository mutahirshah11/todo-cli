---
name: shadcn-ui-components
description: |
  Build UI with shadcn/ui components including forms, tables, dialogs, and feedback elements.
  This skill should be used when users ask to create forms with validation, data tables,
  modal dialogs, dropdown menus, toast notifications, or any UI using shadcn/ui components.
---

# shadcn/ui Components

Build production-ready UI with shadcn/ui - a collection of reusable components built on Radix UI primitives and styled with Tailwind CSS.

## What This Skill Does

- Install and configure shadcn/ui components
- Build forms with react-hook-form + Zod validation
- Create data tables with TanStack Table (sorting, filtering, pagination)
- Implement dialogs, sheets, and overlay components
- Add toast notifications and feedback elements
- Apply theming with CSS variables and dark mode
- Compose components following shadcn patterns

## What This Skill Does NOT Do

- Create custom Radix primitives from scratch
- Build native mobile components
- Handle backend API logic
- Manage authentication flows
- Deploy applications

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Check for existing shadcn setup (`components/ui/`), Tailwind config, existing components |
| **Conversation** | User's specific UI requirements, which components needed |
| **Skill References** | Component patterns from `references/` |
| **User Guidelines** | Project styling conventions, design system tokens |

---

## Installation

### CLI Setup (Recommended)

```bash
# Initialize shadcn/ui in project
npx shadcn@latest init

# Add individual components
npx shadcn@latest add button
npx shadcn@latest add form
npx shadcn@latest add table
npx shadcn@latest add dialog
```

### Required Dependencies

```bash
# For forms
npm install react-hook-form zod @hookform/resolvers

# For data tables
npm install @tanstack/react-table
```

### Project Structure

```
components/
├── ui/                    # shadcn components (auto-generated)
│   ├── button.tsx
│   ├── form.tsx
│   ├── input.tsx
│   └── ...
└── [your-components]/     # Your composed components
```

---

## Component Categories

### Form Components
| Component | Purpose | Reference |
|-----------|---------|-----------|
| Form | Form wrapper with validation | `references/forms.md` |
| Input | Text input field | `references/forms.md` |
| Select | Dropdown selection | `references/forms.md` |
| Checkbox | Boolean toggle | `references/forms.md` |
| Textarea | Multi-line text | `references/forms.md` |

### Data Display
| Component | Purpose | Reference |
|-----------|---------|-----------|
| Table | Data grid | `references/data-table.md` |
| Card | Content container | `references/components.md` |
| Tabs | Tabbed content | `references/components.md` |
| Accordion | Collapsible sections | `references/components.md` |

### Overlays
| Component | Purpose | Reference |
|-----------|---------|-----------|
| Dialog | Modal window | `references/overlays.md` |
| Sheet | Side panel | `references/overlays.md` |
| Popover | Floating content | `references/overlays.md` |
| Tooltip | Hover hints | `references/overlays.md` |

### Feedback
| Component | Purpose | Reference |
|-----------|---------|-----------|
| Sonner | Toast notifications | `references/feedback.md` |
| Alert | Inline messages | `references/feedback.md` |
| Badge | Status indicators | `references/feedback.md` |

### Navigation
| Component | Purpose | Reference |
|-----------|---------|-----------|
| DropdownMenu | Action menu | `references/navigation.md` |
| Command | Command palette | `references/navigation.md` |
| NavigationMenu | Site navigation | `references/navigation.md` |

---

## Quick Patterns

### Form with Validation

```tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const schema = z.object({
  email: z.string().email("Invalid email"),
  name: z.string().min(2, "Name too short"),
})

export function MyForm() {
  const form = useForm<z.infer<typeof schema>>({
    resolver: zodResolver(schema),
    defaultValues: { email: "", name: "" },
  })

  function onSubmit(values: z.infer<typeof schema>) {
    console.log(values)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="email@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}
```

### Controlled Dialog

```tsx
import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"

export function MyDialog() {
  const [open, setOpen] = useState(false)

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>Open</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Dialog Title</DialogTitle>
        </DialogHeader>
        {/* Content */}
        <Button onClick={() => setOpen(false)}>Close</Button>
      </DialogContent>
    </Dialog>
  )
}
```

### Toast Notification

```tsx
import { toast } from "sonner"

// Success
toast.success("Saved successfully")

// Error
toast.error("Something went wrong")

// With action
toast("Item deleted", {
  action: {
    label: "Undo",
    onClick: () => restoreItem(),
  },
})
```

---

## Theming

### CSS Variables (globals.css)

```css
:root {
  --background: 0 0% 100%;
  --foreground: 240 10% 3.9%;
  --primary: 240 5.9% 10%;
  --primary-foreground: 0 0% 98%;
  --secondary: 240 4.8% 95.9%;
  --muted: 240 4.8% 95.9%;
  --accent: 240 4.8% 95.9%;
  --destructive: 0 84.2% 60.2%;
  --border: 240 5.9% 90%;
  --ring: 240 5.9% 10%;
  --radius: 0.5rem;
}

.dark {
  --background: 240 10% 3.9%;
  --foreground: 0 0% 98%;
  --primary: 0 0% 98%;
  --primary-foreground: 240 5.9% 10%;
  /* ... other dark mode values */
}
```

### Dark Mode Toggle

```tsx
import { useTheme } from "next-themes"
import { Button } from "@/components/ui/button"
import { Moon, Sun } from "lucide-react"

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
    </Button>
  )
}
```

---

## Best Practices

### Must Follow
- [ ] Install components individually (don't bulk install)
- [ ] Use Form component for all forms (built-in accessibility)
- [ ] Pass `asChild` to triggers when wrapping custom elements
- [ ] Use CSS variables for theming (not hardcoded colors)
- [ ] Follow composition patterns (combine primitives)

### Must Avoid
- [ ] Don't modify `components/ui/` files directly for one-off changes
- [ ] Don't use inline styles instead of Tailwind classes
- [ ] Don't skip FormField wrapper in forms
- [ ] Don't nest NavigationMenu components (known issue)
- [ ] Don't use Dialog for confirmations (use AlertDialog)

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/forms.md` | Building forms with validation |
| `references/data-table.md` | Tables with sorting/filtering/pagination |
| `references/overlays.md` | Dialogs, sheets, popovers |
| `references/feedback.md` | Toasts, alerts, badges |
| `references/navigation.md` | Menus, command palette |
| `references/components.md` | Cards, tabs, accordion |
| `references/theming.md` | CSS variables, dark mode |

---

## Output Checklist

Before delivering UI code, verify:

- [ ] Components installed via CLI (`npx shadcn@latest add`)
- [ ] Required dependencies installed (react-hook-form, zod, tanstack)
- [ ] Form fields wrapped in FormField with proper control
- [ ] Dialogs have proper trigger and content structure
- [ ] CSS variables used for colors (not hardcoded)
- [ ] Accessibility: labels, ARIA attributes preserved
- [ ] TypeScript types properly inferred from Zod schemas
