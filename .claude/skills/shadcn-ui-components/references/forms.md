# Forms with shadcn/ui

Complete guide to building forms with react-hook-form, Zod validation, and shadcn/ui components.

## Installation

```bash
npx shadcn@latest add form input select checkbox radio-group textarea button label
npm install react-hook-form zod @hookform/resolvers
```

## Form Components

| Component | Import | Purpose |
|-----------|--------|---------|
| Form | `@/components/ui/form` | Form context provider |
| FormField | `@/components/ui/form` | Connects field to form state |
| FormItem | `@/components/ui/form` | Field container |
| FormLabel | `@/components/ui/form` | Accessible label |
| FormControl | `@/components/ui/form` | Input wrapper |
| FormDescription | `@/components/ui/form` | Help text |
| FormMessage | `@/components/ui/form` | Error message |

## Basic Form Pattern

```tsx
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

// 1. Define schema
const formSchema = z.object({
  username: z.string().min(2, "Username must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
})

// 2. Infer type from schema
type FormValues = z.infer<typeof formSchema>

export function ProfileForm() {
  // 3. Initialize form
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      email: "",
    },
  })

  // 4. Handle submit
  async function onSubmit(values: FormValues) {
    console.log(values)
    // API call here
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Username</FormLabel>
              <FormControl>
                <Input placeholder="johndoe" {...field} />
              </FormControl>
              <FormDescription>
                This is your public display name.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" placeholder="john@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? "Saving..." : "Save"}
        </Button>
      </form>
    </Form>
  )
}
```

## Select Component

```tsx
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

<FormField
  control={form.control}
  name="role"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Role</FormLabel>
      <Select onValueChange={field.onChange} defaultValue={field.value}>
        <FormControl>
          <SelectTrigger>
            <SelectValue placeholder="Select a role" />
          </SelectTrigger>
        </FormControl>
        <SelectContent>
          <SelectItem value="admin">Admin</SelectItem>
          <SelectItem value="user">User</SelectItem>
          <SelectItem value="guest">Guest</SelectItem>
        </SelectContent>
      </Select>
      <FormMessage />
    </FormItem>
  )}
/>
```

## Checkbox Component

```tsx
import { Checkbox } from "@/components/ui/checkbox"

<FormField
  control={form.control}
  name="terms"
  render={({ field }) => (
    <FormItem className="flex flex-row items-start space-x-3 space-y-0">
      <FormControl>
        <Checkbox
          checked={field.value}
          onCheckedChange={field.onChange}
        />
      </FormControl>
      <div className="space-y-1 leading-none">
        <FormLabel>Accept terms and conditions</FormLabel>
        <FormDescription>
          You agree to our Terms of Service and Privacy Policy.
        </FormDescription>
      </div>
    </FormItem>
  )}
/>
```

## Radio Group

```tsx
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"

<FormField
  control={form.control}
  name="type"
  render={({ field }) => (
    <FormItem className="space-y-3">
      <FormLabel>Notification type</FormLabel>
      <FormControl>
        <RadioGroup
          onValueChange={field.onChange}
          defaultValue={field.value}
          className="flex flex-col space-y-1"
        >
          <FormItem className="flex items-center space-x-3 space-y-0">
            <FormControl>
              <RadioGroupItem value="all" />
            </FormControl>
            <FormLabel className="font-normal">All notifications</FormLabel>
          </FormItem>
          <FormItem className="flex items-center space-x-3 space-y-0">
            <FormControl>
              <RadioGroupItem value="mentions" />
            </FormControl>
            <FormLabel className="font-normal">Mentions only</FormLabel>
          </FormItem>
          <FormItem className="flex items-center space-x-3 space-y-0">
            <FormControl>
              <RadioGroupItem value="none" />
            </FormControl>
            <FormLabel className="font-normal">None</FormLabel>
          </FormItem>
        </RadioGroup>
      </FormControl>
      <FormMessage />
    </FormItem>
  )}
/>
```

## Textarea

```tsx
import { Textarea } from "@/components/ui/textarea"

<FormField
  control={form.control}
  name="bio"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Bio</FormLabel>
      <FormControl>
        <Textarea
          placeholder="Tell us about yourself"
          className="resize-none"
          {...field}
        />
      </FormControl>
      <FormDescription>Max 500 characters</FormDescription>
      <FormMessage />
    </FormItem>
  )}
/>
```

## Zod Validation Patterns

### Common Validations

```tsx
const schema = z.object({
  // Required string
  name: z.string().min(1, "Required"),

  // Email
  email: z.string().email("Invalid email"),

  // URL
  website: z.string().url("Invalid URL").optional(),

  // Number in range
  age: z.coerce.number().min(18, "Must be 18+").max(120),

  // Enum
  role: z.enum(["admin", "user", "guest"]),

  // Boolean required true
  terms: z.literal(true, {
    errorMap: () => ({ message: "You must accept terms" }),
  }),

  // Date
  birthday: z.coerce.date(),

  // Array with min items
  tags: z.array(z.string()).min(1, "Select at least one"),

  // Conditional (password confirmation)
  password: z.string().min(8),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
})
```

### Async Validation

```tsx
const schema = z.object({
  username: z.string()
    .min(3)
    .refine(async (val) => {
      const exists = await checkUsernameExists(val)
      return !exists
    }, "Username already taken"),
})
```

### Conditional Fields

```tsx
const schema = z.discriminatedUnion("accountType", [
  z.object({
    accountType: z.literal("personal"),
    name: z.string(),
  }),
  z.object({
    accountType: z.literal("business"),
    name: z.string(),
    companyName: z.string(),
    taxId: z.string(),
  }),
])
```

## Form State Helpers

```tsx
const form = useForm<FormValues>({...})

// Check if form is dirty
form.formState.isDirty

// Check if submitting
form.formState.isSubmitting

// Check if submitted successfully
form.formState.isSubmitSuccessful

// Get specific field error
form.formState.errors.email?.message

// Reset form
form.reset()

// Set specific value
form.setValue("email", "new@email.com")

// Watch field changes
const email = form.watch("email")

// Trigger validation manually
form.trigger("email")
```

## Multi-Step Form

```tsx
"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

// Schema for all steps
const fullSchema = z.object({
  // Step 1
  email: z.string().email(),
  password: z.string().min(8),
  // Step 2
  firstName: z.string().min(2),
  lastName: z.string().min(2),
  // Step 3
  plan: z.enum(["free", "pro", "enterprise"]),
})

// Partial schemas for each step
const step1Schema = fullSchema.pick({ email: true, password: true })
const step2Schema = fullSchema.pick({ firstName: true, lastName: true })
const step3Schema = fullSchema.pick({ plan: true })

const schemas = [step1Schema, step2Schema, step3Schema]

export function MultiStepForm() {
  const [step, setStep] = useState(0)

  const form = useForm<z.infer<typeof fullSchema>>({
    resolver: zodResolver(schemas[step]),
    mode: "onChange",
  })

  async function nextStep() {
    const valid = await form.trigger()
    if (valid && step < schemas.length - 1) {
      setStep(step + 1)
    }
  }

  function prevStep() {
    if (step > 0) setStep(step - 1)
  }

  async function onSubmit(values: z.infer<typeof fullSchema>) {
    console.log("Final values:", values)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        {step === 0 && (
          <>
            {/* Email and password fields */}
          </>
        )}
        {step === 1 && (
          <>
            {/* Name fields */}
          </>
        )}
        {step === 2 && (
          <>
            {/* Plan selection */}
          </>
        )}

        <div className="flex gap-2 mt-4">
          {step > 0 && (
            <Button type="button" variant="outline" onClick={prevStep}>
              Back
            </Button>
          )}
          {step < schemas.length - 1 ? (
            <Button type="button" onClick={nextStep}>
              Next
            </Button>
          ) : (
            <Button type="submit">Submit</Button>
          )}
        </div>
      </form>
    </Form>
  )
}
```

## Form with Dialog

```tsx
"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const schema = z.object({
  name: z.string().min(2),
})

export function FormDialog() {
  const [open, setOpen] = useState(false)

  const form = useForm<z.infer<typeof schema>>({
    resolver: zodResolver(schema),
    defaultValues: { name: "" },
  })

  async function onSubmit(values: z.infer<typeof schema>) {
    await saveData(values)
    form.reset()
    setOpen(false) // Close dialog on success
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>Add Item</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Add New Item</DialogTitle>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Name</FormLabel>
                  <FormControl>
                    <Input {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <div className="flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" disabled={form.formState.isSubmitting}>
                Save
              </Button>
            </div>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  )
}
```

## Best Practices

### Do
- Always use FormField wrapper for proper form state connection
- Use zodResolver for type-safe validation
- Provide defaultValues to avoid uncontrolled input warnings
- Use FormDescription for helpful hints
- Disable submit button during submission
- Reset form after successful submission

### Don't
- Don't spread field directly on Select (use onValueChange)
- Don't forget FormControl wrapper around inputs
- Don't use native form validation (let Zod handle it)
- Don't nest forms (HTML doesn't allow it)
