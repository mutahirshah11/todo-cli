# Zod Schema Patterns

## String Validations

```ts
const schema = z.object({
  // Basic
  name: z.string().min(2).max(50),

  // Email
  email: z.string().email("Invalid email address"),

  // URL
  website: z.string().url("Invalid URL"),

  // Regex
  username: z.string().regex(/^[a-z0-9_]+$/, "Lowercase, numbers, underscores only"),

  // Trim whitespace
  bio: z.string().trim().max(500),

  // Non-empty (after trim)
  title: z.string().trim().min(1, "Required"),
});
```

## Number Validations

```ts
const schema = z.object({
  age: z.number().min(18).max(120),
  quantity: z.number().int().positive(),
  price: z.number().nonnegative(),
  rating: z.number().min(1).max(5),
});

// Coerce from string (form inputs)
const formSchema = z.object({
  age: z.coerce.number().min(18),
  price: z.coerce.number().positive(),
});
```

## Optional & Nullable

```ts
const schema = z.object({
  // Optional (can be undefined)
  nickname: z.string().optional(),

  // Nullable (can be null)
  deletedAt: z.date().nullable(),

  // Optional OR nullable
  middleName: z.string().nullish(),

  // Optional with default
  role: z.string().default("user"),

  // Optional string but if provided, must be valid email
  secondaryEmail: z.string().email().optional().or(z.literal("")),
});
```

## Enums & Unions

```ts
// Enum
const roleSchema = z.enum(["admin", "user", "guest"]);

// Native enum
enum Status { Active = "active", Inactive = "inactive" }
const statusSchema = z.nativeEnum(Status);

// Union
const idSchema = z.union([z.string(), z.number()]);

// Discriminated union
const eventSchema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("click"), x: z.number(), y: z.number() }),
  z.object({ type: z.literal("scroll"), offset: z.number() }),
]);
```

## Arrays & Objects

```ts
const schema = z.object({
  // Array of strings
  tags: z.array(z.string()).min(1).max(5),

  // Array of objects
  items: z.array(z.object({
    name: z.string(),
    quantity: z.number().int().positive(),
  })),

  // Nested object
  address: z.object({
    street: z.string(),
    city: z.string(),
    zip: z.string().regex(/^\d{5}$/),
  }),
});
```

## Custom Validation with refine()

```ts
const schema = z.object({
  password: z.string().min(8),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"], // Error shows on this field
});

// Multiple refinements
const userSchema = z.object({
  username: z.string()
    .min(3)
    .refine((val) => !val.includes(" "), "No spaces allowed")
    .refine((val) => !bannedWords.includes(val), "Username not allowed"),
});
```

## Cross-Field Validation with superRefine()

```ts
const dateRangeSchema = z.object({
  startDate: z.coerce.date(),
  endDate: z.coerce.date(),
}).superRefine((data, ctx) => {
  if (data.endDate <= data.startDate) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "End date must be after start date",
      path: ["endDate"],
    });
  }
});
```

## Transform & Preprocess

```ts
const schema = z.object({
  // Transform output
  email: z.string().email().transform((val) => val.toLowerCase()),

  // Preprocess input (before validation)
  phone: z.preprocess(
    (val) => String(val).replace(/\D/g, ""),
    z.string().length(10)
  ),

  // Coerce types
  age: z.coerce.number(),
  isActive: z.coerce.boolean(),
  createdAt: z.coerce.date(),
});
```

## Custom Error Messages

```ts
const schema = z.object({
  email: z.string({
    required_error: "Email is required",
    invalid_type_error: "Email must be a string",
  }).email({ message: "Please enter a valid email" }),

  age: z.number({
    required_error: "Age is required",
  }).min(18, { message: "Must be 18 or older" }),
});
```

## File Validation

```ts
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ACCEPTED_TYPES = ["image/jpeg", "image/png", "image/webp"];

const fileSchema = z
  .instanceof(File)
  .refine((file) => file.size <= MAX_FILE_SIZE, "Max file size is 5MB")
  .refine(
    (file) => ACCEPTED_TYPES.includes(file.type),
    "Only .jpg, .png, .webp formats are supported"
  );

// For file input (can be null/undefined initially)
const uploadSchema = z.object({
  avatar: z
    .instanceof(File)
    .refine((f) => f.size <= MAX_FILE_SIZE, "Max 5MB")
    .optional(),
});
```

## Infer TypeScript Types

```ts
const userSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  profile: z.object({
    name: z.string(),
    age: z.number().optional(),
  }),
});

// Infer the type
type User = z.infer<typeof userSchema>;
// Result: { id: string; email: string; profile: { name: string; age?: number } }

// For input vs output types (when using transform)
type UserInput = z.input<typeof userSchema>;
type UserOutput = z.output<typeof userSchema>;
```
