# Advanced Patterns

## Field Arrays (Dynamic Fields)

```tsx
import { useForm, useFieldArray } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const schema = z.object({
  items: z.array(z.object({
    name: z.string().min(1, "Required"),
    quantity: z.coerce.number().min(1),
  })).min(1, "Add at least one item"),
});

type FormData = z.infer<typeof schema>;

function DynamicForm() {
  const { control, register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      items: [{ name: "", quantity: 1 }],
    },
  });

  const { fields, append, remove, move } = useFieldArray({
    control,
    name: "items",
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {fields.map((field, index) => (
        <div key={field.id}>
          <input
            {...register(`items.${index}.name`)}
            placeholder="Item name"
          />
          {errors.items?.[index]?.name && (
            <span>{errors.items[index].name.message}</span>
          )}

          <input
            {...register(`items.${index}.quantity`)}
            type="number"
          />

          <button type="button" onClick={() => remove(index)}>
            Remove
          </button>
        </div>
      ))}

      {errors.items?.root && <span>{errors.items.root.message}</span>}

      <button type="button" onClick={() => append({ name: "", quantity: 1 })}>
        Add Item
      </button>
      <button type="submit">Submit</button>
    </form>
  );
}
```

### Field Array Operations

```tsx
const { fields, append, prepend, insert, remove, swap, move, update, replace } = useFieldArray({
  control,
  name: "items",
});

// Add to end
append({ name: "", quantity: 1 });

// Add to beginning
prepend({ name: "", quantity: 1 });

// Insert at index
insert(2, { name: "", quantity: 1 });

// Remove by index
remove(0);

// Swap positions
swap(0, 1);

// Move item
move(0, 2);

// Update item at index
update(0, { name: "Updated", quantity: 5 });

// Replace entire array
replace([{ name: "New", quantity: 1 }]);
```

## Multi-Step Wizard Form

```tsx
import { useForm, FormProvider } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useState } from "react";

// Step schemas
const step1Schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

const step2Schema = z.object({
  firstName: z.string().min(2),
  lastName: z.string().min(2),
});

const step3Schema = z.object({
  plan: z.enum(["free", "pro", "enterprise"]),
  acceptTerms: z.literal(true, {
    errorMap: () => ({ message: "You must accept the terms" }),
  }),
});

// Combined schema
const fullSchema = step1Schema.merge(step2Schema).merge(step3Schema);
type FormData = z.infer<typeof fullSchema>;

const stepSchemas = [step1Schema, step2Schema, step3Schema];

function MultiStepForm() {
  const [step, setStep] = useState(0);

  const methods = useForm<FormData>({
    resolver: zodResolver(fullSchema),
    mode: "onTouched",
    defaultValues: {
      email: "",
      password: "",
      firstName: "",
      lastName: "",
      plan: "free",
      acceptTerms: false,
    },
  });

  const { trigger, handleSubmit } = methods;

  const nextStep = async () => {
    const currentSchema = stepSchemas[step];
    const fields = Object.keys(currentSchema.shape) as (keyof FormData)[];

    const isValid = await trigger(fields);
    if (isValid) setStep((s) => s + 1);
  };

  const prevStep = () => setStep((s) => s - 1);

  const onSubmit = async (data: FormData) => {
    console.log("Final data:", data);
    await api.register(data);
  };

  return (
    <FormProvider {...methods}>
      <form onSubmit={handleSubmit(onSubmit)}>
        {step === 0 && <Step1 />}
        {step === 1 && <Step2 />}
        {step === 2 && <Step3 />}

        <div>
          {step > 0 && (
            <button type="button" onClick={prevStep}>Back</button>
          )}
          {step < 2 ? (
            <button type="button" onClick={nextStep}>Next</button>
          ) : (
            <button type="submit">Submit</button>
          )}
        </div>
      </form>
    </FormProvider>
  );
}

// Step components use useFormContext
function Step1() {
  const { register, formState: { errors } } = useFormContext<FormData>();
  return (
    <>
      <input {...register("email")} placeholder="Email" />
      {errors.email && <span>{errors.email.message}</span>}

      <input {...register("password")} type="password" placeholder="Password" />
      {errors.password && <span>{errors.password.message}</span>}
    </>
  );
}
```

## Async Validation

```tsx
const schema = z.object({
  username: z.string()
    .min(3)
    .refine(async (val) => {
      // Check availability
      const response = await fetch(`/api/check-username?u=${val}`);
      const { available } = await response.json();
      return available;
    }, "Username is already taken"),

  email: z.string().email(),
});

// With debounce (recommended)
import { useDebouncedCallback } from "use-debounce";

function UsernameField() {
  const { register, setError, clearErrors } = useFormContext<FormData>();
  const [checking, setChecking] = useState(false);

  const checkUsername = useDebouncedCallback(async (username: string) => {
    if (username.length < 3) return;

    setChecking(true);
    try {
      const res = await fetch(`/api/check-username?u=${username}`);
      const { available } = await res.json();

      if (!available) {
        setError("username", { message: "Username is taken" });
      } else {
        clearErrors("username");
      }
    } finally {
      setChecking(false);
    }
  }, 500);

  return (
    <div>
      <input
        {...register("username", {
          onChange: (e) => checkUsername(e.target.value),
        })}
      />
      {checking && <span>Checking...</span>}
    </div>
  );
}
```

## File Upload

```tsx
const MAX_SIZE = 5 * 1024 * 1024; // 5MB
const ACCEPTED = ["image/jpeg", "image/png", "image/webp"];

const schema = z.object({
  avatar: z
    .instanceof(FileList)
    .refine((files) => files.length === 1, "Please select a file")
    .refine((files) => files[0]?.size <= MAX_SIZE, "Max file size is 5MB")
    .refine(
      (files) => ACCEPTED.includes(files[0]?.type),
      "Only .jpg, .png, .webp allowed"
    )
    .transform((files) => files[0]), // Extract single file
});

type FormData = z.infer<typeof schema>;

function UploadForm() {
  const { register, handleSubmit, watch, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const avatarFile = watch("avatar");
  const preview = avatarFile ? URL.createObjectURL(avatarFile) : null;

  const onSubmit = async (data: FormData) => {
    const formData = new FormData();
    formData.append("avatar", data.avatar);
    await fetch("/api/upload", { method: "POST", body: formData });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input type="file" accept={ACCEPTED.join(",")} {...register("avatar")} />
      {errors.avatar && <span>{errors.avatar.message}</span>}

      {preview && <img src={preview} alt="Preview" width={100} />}

      <button type="submit">Upload</button>
    </form>
  );
}
```

## Multiple File Upload

```tsx
const schema = z.object({
  files: z
    .instanceof(FileList)
    .refine((files) => files.length > 0, "Select at least one file")
    .refine((files) => files.length <= 5, "Max 5 files")
    .refine(
      (files) => Array.from(files).every((f) => f.size <= MAX_SIZE),
      "Each file must be under 5MB"
    ),
});

function MultiUpload() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: z.infer<typeof schema>) => {
    const formData = new FormData();
    Array.from(data.files).forEach((file, i) => {
      formData.append(`file_${i}`, file);
    });
    await fetch("/api/upload-multiple", { method: "POST", body: formData });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input type="file" multiple {...register("files")} />
      {errors.files && <span>{errors.files.message}</span>}
      <button type="submit">Upload All</button>
    </form>
  );
}
```

## Conditional Schema Validation

```tsx
const schema = z.discriminatedUnion("accountType", [
  z.object({
    accountType: z.literal("personal"),
    name: z.string().min(2),
    email: z.string().email(),
  }),
  z.object({
    accountType: z.literal("business"),
    companyName: z.string().min(2),
    taxId: z.string().regex(/^\d{9}$/),
    email: z.string().email(),
  }),
]);

function ConditionalForm() {
  const { register, watch, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema),
    defaultValues: { accountType: "personal" },
  });

  const accountType = watch("accountType");

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <select {...register("accountType")}>
        <option value="personal">Personal</option>
        <option value="business">Business</option>
      </select>

      {accountType === "personal" && (
        <input {...register("name")} placeholder="Your name" />
      )}

      {accountType === "business" && (
        <>
          <input {...register("companyName")} placeholder="Company name" />
          <input {...register("taxId")} placeholder="Tax ID" />
        </>
      )}

      <input {...register("email")} placeholder="Email" />
      <button type="submit">Submit</button>
    </form>
  );
}
```
