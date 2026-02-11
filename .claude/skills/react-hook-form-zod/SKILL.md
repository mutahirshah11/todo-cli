---
name: react-hook-form-zod
description: |
  Form handling with react-hook-form and Zod validation for type-safe, performant forms.
  This skill should be used when building forms with validation, handling form state,
  implementing field arrays, file uploads, async validation, or multi-step wizards.
---

# React Hook Form + Zod

Type-safe, performant forms with schema validation.

## Before Implementation

| Source | Gather |
|--------|--------|
| **Codebase** | Existing form patterns, UI components, API endpoints |
| **Conversation** | Form fields, validation rules, submission handler |
| **Skill References** | Patterns from `references/` |
| **shadcn/ui** | Use Form components when available (integrates with this skill) |

## Quick Setup

```bash
npm install react-hook-form zod @hookform/resolvers
```

## Core Pattern

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

// 1. Define schema FIRST
const schema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(8, "Min 8 characters"),
});

// 2. Infer TypeScript type
type FormData = z.infer<typeof schema>;

// 3. Use in component
function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormData) => {
    await api.login(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("email")} />
      {errors.email && <span>{errors.email.message}</span>}

      <input type="password" {...register("password")} />
      {errors.password && <span>{errors.password.message}</span>}

      <button disabled={isSubmitting}>
        {isSubmitting ? "Loading..." : "Submit"}
      </button>
    </form>
  );
}
```

## Zod Schema Patterns

See `references/zod-schemas.md` for complete patterns:
- String validations (email, url, min/max, regex)
- Number validations (min, max, int, positive)
- Optional/nullable fields
- Custom validation with `.refine()`
- Cross-field validation with `.superRefine()`
- Transform and preprocess

## Form Patterns

See `references/form-patterns.md` for:
- Validation modes (onBlur, onChange, onSubmit)
- Default values and reset
- Watch and conditional fields
- Controlled vs uncontrolled inputs

## Advanced Patterns

See `references/advanced-patterns.md` for:
- Field arrays (dynamic add/remove)
- Multi-step wizard forms
- Async validation (e.g., username check)
- File upload validation

## shadcn/ui Integration

See `references/shadcn-integration.md` for:
- FormField, FormItem, FormControl usage
- Error display with FormMessage
- Complete form example

## Best Practices

1. **Schema first** - Define Zod schema, infer types
2. **Uncontrolled inputs** - Use `register()` for performance
3. **Inline errors** - Show below each field
4. **Disable on submit** - Prevent double submission
5. **Reset after success** - `reset()` after successful submit
6. **Mode selection** - Use `mode: "onBlur"` for UX balance

## What This Skill Does NOT Do

- Server-side validation (backend concern)
- Form analytics/tracking
- A/B testing forms
- Form builder UI
