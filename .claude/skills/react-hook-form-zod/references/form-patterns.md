# Form Patterns

## Validation Modes

```tsx
const { register, handleSubmit } = useForm<FormData>({
  resolver: zodResolver(schema),
  mode: "onBlur",      // Validate on blur (recommended)
  // mode: "onChange", // Validate on every change (more aggressive)
  // mode: "onSubmit", // Validate only on submit (default)
  // mode: "onTouched",// Validate on blur, then onChange after first error
  // mode: "all",      // Validate on blur AND onChange
});
```

## Default Values

```tsx
// Static defaults
const { register } = useForm<FormData>({
  resolver: zodResolver(schema),
  defaultValues: {
    email: "",
    role: "user",
    notifications: true,
  },
});

// Async defaults (fetched data)
const { register } = useForm<FormData>({
  resolver: zodResolver(schema),
  defaultValues: async () => {
    const user = await fetchUser();
    return {
      email: user.email,
      name: user.name,
    };
  },
});
```

## Reset Form

```tsx
const { reset, handleSubmit } = useForm<FormData>({
  resolver: zodResolver(schema),
  defaultValues: { email: "", name: "" },
});

// Reset to default values
const onSubmit = async (data: FormData) => {
  await api.submit(data);
  reset(); // Clears to defaultValues
};

// Reset to specific values
reset({ email: "new@example.com", name: "New Name" });

// Reset with options
reset(undefined, {
  keepErrors: false,
  keepDirty: false,
  keepValues: false,
  keepDefaultValues: true,
});
```

## Watch & Conditional Fields

```tsx
function ConditionalForm() {
  const { register, watch, control } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  // Watch single field (causes re-render)
  const accountType = watch("accountType");

  // Watch multiple fields
  const [firstName, lastName] = watch(["firstName", "lastName"]);

  return (
    <form>
      <select {...register("accountType")}>
        <option value="personal">Personal</option>
        <option value="business">Business</option>
      </select>

      {accountType === "business" && (
        <>
          <input {...register("companyName")} placeholder="Company Name" />
          <input {...register("taxId")} placeholder="Tax ID" />
        </>
      )}
    </form>
  );
}
```

## useWatch (Isolate Re-renders)

```tsx
// In child component - only this component re-renders
function PriceDisplay({ control }: { control: Control<FormData> }) {
  const quantity = useWatch({ control, name: "quantity" });
  const price = useWatch({ control, name: "price" });

  return <div>Total: ${quantity * price}</div>;
}

// In parent - watch without re-rendering parent
function ParentForm() {
  const { control, register } = useForm<FormData>();

  return (
    <form>
      <input {...register("quantity")} type="number" />
      <input {...register("price")} type="number" />
      <PriceDisplay control={control} />
    </form>
  );
}
```

## FormState Properties

```tsx
const {
  formState: {
    errors,        // Validation errors object
    isSubmitting,  // True during async submit
    isValid,       // True if no errors (requires mode != onSubmit)
    isDirty,       // True if any field changed from default
    isLoading,     // True during async defaultValues load
    dirtyFields,   // Object of dirty field names
    touchedFields, // Object of touched field names
    submitCount,   // Number of submit attempts
  },
} = useForm<FormData>({ resolver: zodResolver(schema) });

// Common usage
<button disabled={isSubmitting || !isDirty}>
  {isSubmitting ? "Saving..." : "Save"}
</button>
```

## setValue & trigger

```tsx
const { setValue, trigger, getValues } = useForm<FormData>();

// Set value programmatically
setValue("email", "user@example.com");

// Set with options
setValue("email", "user@example.com", {
  shouldValidate: true,  // Trigger validation
  shouldDirty: true,     // Mark as dirty
  shouldTouch: true,     // Mark as touched
});

// Trigger validation manually
await trigger("email");        // Single field
await trigger(["email", "name"]); // Multiple fields
await trigger();               // All fields

// Get current values
const email = getValues("email");
const allValues = getValues();
```

## Controlled Inputs (Controller)

Use for UI libraries that don't expose `ref`:

```tsx
import { Controller } from "react-hook-form";

function Form() {
  const { control, handleSubmit } = useForm<FormData>();

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Controller
        name="select"
        control={control}
        render={({ field, fieldState: { error } }) => (
          <>
            <CustomSelect
              value={field.value}
              onChange={field.onChange}
              onBlur={field.onBlur}
            />
            {error && <span>{error.message}</span>}
          </>
        )}
      />
    </form>
  );
}
```

## Form Context (Nested Components)

```tsx
import { FormProvider, useFormContext } from "react-hook-form";

// Parent wraps with FormProvider
function ParentForm() {
  const methods = useForm<FormData>({ resolver: zodResolver(schema) });

  return (
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(onSubmit)}>
        <NestedInput />
        <button>Submit</button>
      </form>
    </FormProvider>
  );
}

// Child accesses via useFormContext
function NestedInput() {
  const { register, formState: { errors } } = useFormContext<FormData>();

  return (
    <div>
      <input {...register("email")} />
      {errors.email && <span>{errors.email.message}</span>}
    </div>
  );
}
```

## Error Handling Pattern

```tsx
function FormWithErrors() {
  const {
    register,
    handleSubmit,
    setError,
    formState: { errors },
  } = useForm<FormData>({ resolver: zodResolver(schema) });

  const onSubmit = async (data: FormData) => {
    try {
      await api.submit(data);
    } catch (err) {
      // Set server error on specific field
      setError("email", {
        type: "server",
        message: "Email already exists",
      });

      // Or set root error
      setError("root", {
        type: "server",
        message: "Something went wrong",
      });
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("email")} />
      {errors.email && <span className="error">{errors.email.message}</span>}

      {errors.root && <div className="error">{errors.root.message}</div>}

      <button>Submit</button>
    </form>
  );
}
```
