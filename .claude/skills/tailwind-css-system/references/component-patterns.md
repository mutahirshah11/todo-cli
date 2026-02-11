# Component Patterns

Reusable UI patterns with Tailwind CSS.

## Button Variants

### Base Button Classes

```html
<!-- Primary -->
<button class="
  px-4 py-2 rounded-lg font-medium
  bg-primary-500 text-white
  hover:bg-primary-600
  focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2
  disabled:opacity-50 disabled:cursor-not-allowed
  transition-colors
">
  Primary Button
</button>

<!-- Secondary -->
<button class="
  px-4 py-2 rounded-lg font-medium
  bg-gray-100 text-gray-900
  hover:bg-gray-200
  dark:bg-gray-800 dark:text-white dark:hover:bg-gray-700
  focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2
  transition-colors
">
  Secondary Button
</button>

<!-- Outline -->
<button class="
  px-4 py-2 rounded-lg font-medium
  border-2 border-primary-500 text-primary-500
  hover:bg-primary-50
  dark:hover:bg-primary-950
  focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2
  transition-colors
">
  Outline Button
</button>

<!-- Ghost -->
<button class="
  px-4 py-2 rounded-lg font-medium
  text-gray-600 hover:text-gray-900
  hover:bg-gray-100
  dark:text-gray-300 dark:hover:text-white dark:hover:bg-gray-800
  transition-colors
">
  Ghost Button
</button>

<!-- Destructive -->
<button class="
  px-4 py-2 rounded-lg font-medium
  bg-red-500 text-white
  hover:bg-red-600
  focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2
  transition-colors
">
  Delete
</button>
```

### Button Sizes

```html
<!-- Small -->
<button class="px-3 py-1.5 text-sm rounded-md">Small</button>

<!-- Default -->
<button class="px-4 py-2 text-base rounded-lg">Default</button>

<!-- Large -->
<button class="px-6 py-3 text-lg rounded-lg">Large</button>
```

### Icon Button

```html
<button class="
  p-2 rounded-lg
  text-gray-500 hover:text-gray-700
  hover:bg-gray-100
  dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-800
">
  <svg class="w-5 h-5">...</svg>
</button>
```

### Button with Loading

```html
<button class="px-4 py-2 flex items-center gap-2" disabled>
  <svg class="w-4 h-4 animate-spin">...</svg>
  Loading...
</button>
```

---

## Card Patterns

### Basic Card

```html
<div class="
  bg-white dark:bg-gray-800
  rounded-xl shadow-sm
  border border-gray-200 dark:border-gray-700
  p-6
">
  <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
    Card Title
  </h3>
  <p class="mt-2 text-gray-600 dark:text-gray-300">
    Card content goes here.
  </p>
</div>
```

### Card with Image

```html
<div class="
  bg-white dark:bg-gray-800
  rounded-xl shadow-sm overflow-hidden
  border border-gray-200 dark:border-gray-700
">
  <img src="..." alt="..." class="w-full h-48 object-cover" />
  <div class="p-6">
    <h3 class="text-lg font-semibold">Title</h3>
    <p class="mt-2 text-gray-600 dark:text-gray-300">Description</p>
  </div>
</div>
```

### Interactive Card

```html
<a href="#" class="
  block
  bg-white dark:bg-gray-800
  rounded-xl shadow-sm
  border border-gray-200 dark:border-gray-700
  p-6
  hover:shadow-md hover:border-primary-300
  transition-all duration-200
  group
">
  <h3 class="font-semibold group-hover:text-primary-500 transition-colors">
    Clickable Card
  </h3>
</a>
```

### Card Grid

```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
  <!-- Cards -->
</div>
```

---

## Form Inputs

### Text Input

```html
<div>
  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
    Email
  </label>
  <input
    type="email"
    class="
      w-full px-3 py-2
      bg-white dark:bg-gray-900
      border border-gray-300 dark:border-gray-600
      rounded-lg
      text-gray-900 dark:text-white
      placeholder-gray-400 dark:placeholder-gray-500
      focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
      disabled:bg-gray-100 disabled:cursor-not-allowed
    "
    placeholder="you@example.com"
  />
</div>
```

### Input with Error

```html
<div>
  <label class="block text-sm font-medium text-gray-700 mb-1">
    Email
  </label>
  <input
    type="email"
    class="
      w-full px-3 py-2
      border border-red-500
      rounded-lg
      focus:outline-none focus:ring-2 focus:ring-red-500
    "
  />
  <p class="mt-1 text-sm text-red-500">Please enter a valid email</p>
</div>
```

### Input with Icon

```html
<div class="relative">
  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
    <svg class="w-5 h-5 text-gray-400">...</svg>
  </div>
  <input
    type="text"
    class="w-full pl-10 pr-3 py-2 border rounded-lg"
    placeholder="Search..."
  />
</div>
```

### Select

```html
<select class="
  w-full px-3 py-2
  bg-white dark:bg-gray-900
  border border-gray-300 dark:border-gray-600
  rounded-lg
  text-gray-900 dark:text-white
  focus:outline-none focus:ring-2 focus:ring-primary-500
  cursor-pointer
">
  <option value="">Select option</option>
  <option value="1">Option 1</option>
  <option value="2">Option 2</option>
</select>
```

### Checkbox

```html
<label class="flex items-center gap-2 cursor-pointer">
  <input
    type="checkbox"
    class="
      w-4 h-4 rounded
      border-gray-300 dark:border-gray-600
      text-primary-500
      focus:ring-primary-500 focus:ring-offset-0
    "
  />
  <span class="text-sm text-gray-700 dark:text-gray-300">
    Remember me
  </span>
</label>
```

### Textarea

```html
<textarea
  rows="4"
  class="
    w-full px-3 py-2
    bg-white dark:bg-gray-900
    border border-gray-300 dark:border-gray-600
    rounded-lg
    text-gray-900 dark:text-white
    placeholder-gray-400
    focus:outline-none focus:ring-2 focus:ring-primary-500
    resize-none
  "
  placeholder="Enter message..."
></textarea>
```

---

## Navigation

### Navbar (Responsive)

```html
<nav class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800">
  <div class="max-w-7xl mx-auto px-4">
    <div class="flex items-center justify-between h-16">
      <!-- Logo -->
      <a href="/" class="font-bold text-xl">Logo</a>

      <!-- Desktop nav -->
      <div class="hidden md:flex items-center gap-6">
        <a href="#" class="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
          Features
        </a>
        <a href="#" class="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
          Pricing
        </a>
        <button class="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600">
          Get Started
        </button>
      </div>

      <!-- Mobile menu button -->
      <button class="md:hidden p-2">
        <svg class="w-6 h-6">...</svg>
      </button>
    </div>
  </div>

  <!-- Mobile nav (toggle visibility) -->
  <div class="md:hidden border-t border-gray-200 dark:border-gray-800">
    <div class="px-4 py-4 space-y-3">
      <a href="#" class="block text-gray-600">Features</a>
      <a href="#" class="block text-gray-600">Pricing</a>
      <button class="w-full px-4 py-2 bg-primary-500 text-white rounded-lg">
        Get Started
      </button>
    </div>
  </div>
</nav>
```

### Sidebar

```html
<aside class="
  w-64 h-screen
  bg-white dark:bg-gray-900
  border-r border-gray-200 dark:border-gray-800
  flex flex-col
">
  <!-- Logo -->
  <div class="h-16 flex items-center px-6 border-b border-gray-200 dark:border-gray-800">
    <span class="font-bold text-xl">App</span>
  </div>

  <!-- Nav items -->
  <nav class="flex-1 px-4 py-4 space-y-1">
    <a href="#" class="
      flex items-center gap-3 px-3 py-2 rounded-lg
      bg-primary-50 text-primary-600
      dark:bg-primary-900/50 dark:text-primary-400
    ">
      <svg class="w-5 h-5">...</svg>
      Dashboard
    </a>
    <a href="#" class="
      flex items-center gap-3 px-3 py-2 rounded-lg
      text-gray-600 hover:bg-gray-100
      dark:text-gray-300 dark:hover:bg-gray-800
    ">
      <svg class="w-5 h-5">...</svg>
      Settings
    </a>
  </nav>
</aside>
```

### Tabs

```html
<div class="border-b border-gray-200 dark:border-gray-700">
  <nav class="flex gap-4">
    <button class="
      px-4 py-2 -mb-px
      border-b-2 border-primary-500
      text-primary-600 dark:text-primary-400
      font-medium
    ">
      Tab 1
    </button>
    <button class="
      px-4 py-2 -mb-px
      border-b-2 border-transparent
      text-gray-500 hover:text-gray-700
      dark:text-gray-400 dark:hover:text-gray-200
    ">
      Tab 2
    </button>
  </nav>
</div>
```

---

## Grid Layouts

### Responsive Columns

```html
<!-- 1 → 2 → 3 → 4 columns -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
  <div>Item 4</div>
</div>
```

### Two Column Layout (Sidebar + Content)

```html
<div class="flex min-h-screen">
  <!-- Sidebar -->
  <aside class="w-64 flex-shrink-0 hidden lg:block">...</aside>

  <!-- Main content -->
  <main class="flex-1 p-6">...</main>
</div>
```

### Holy Grail Layout

```html
<div class="min-h-screen flex flex-col">
  <!-- Header -->
  <header class="h-16 border-b">...</header>

  <!-- Body -->
  <div class="flex-1 flex">
    <aside class="w-64 border-r hidden md:block">Sidebar</aside>
    <main class="flex-1 p-6">Content</main>
  </div>

  <!-- Footer -->
  <footer class="h-16 border-t">...</footer>
</div>
```

---

## Badges & Tags

```html
<!-- Badge -->
<span class="
  inline-flex items-center px-2.5 py-0.5
  rounded-full text-xs font-medium
  bg-green-100 text-green-800
  dark:bg-green-900/50 dark:text-green-400
">
  Active
</span>

<!-- Tag with remove -->
<span class="
  inline-flex items-center gap-1 px-3 py-1
  rounded-full text-sm
  bg-gray-100 text-gray-700
  dark:bg-gray-800 dark:text-gray-300
">
  Tag
  <button class="hover:text-gray-900">
    <svg class="w-4 h-4">×</svg>
  </button>
</span>
```

---

## Modal

```html
<!-- Backdrop -->
<div class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
  <!-- Modal -->
  <div class="
    bg-white dark:bg-gray-800
    rounded-xl shadow-xl
    w-full max-w-md
    max-h-[90vh] overflow-auto
  ">
    <!-- Header -->
    <div class="flex items-center justify-between p-4 border-b dark:border-gray-700">
      <h2 class="text-lg font-semibold">Modal Title</h2>
      <button class="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded">
        <svg class="w-5 h-5">×</svg>
      </button>
    </div>

    <!-- Body -->
    <div class="p-4">
      Modal content here.
    </div>

    <!-- Footer -->
    <div class="flex justify-end gap-2 p-4 border-t dark:border-gray-700">
      <button class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg">
        Cancel
      </button>
      <button class="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600">
        Confirm
      </button>
    </div>
  </div>
</div>
```

---

## Alert / Toast

```html
<!-- Success Alert -->
<div class="
  flex items-center gap-3 p-4
  bg-green-50 border border-green-200 rounded-lg
  dark:bg-green-900/20 dark:border-green-800
">
  <svg class="w-5 h-5 text-green-500">✓</svg>
  <p class="text-green-700 dark:text-green-400">Operation successful!</p>
</div>

<!-- Error Alert -->
<div class="
  flex items-center gap-3 p-4
  bg-red-50 border border-red-200 rounded-lg
  dark:bg-red-900/20 dark:border-red-800
">
  <svg class="w-5 h-5 text-red-500">!</svg>
  <p class="text-red-700 dark:text-red-400">Something went wrong.</p>
</div>
```

---

## Skeleton Loading

```html
<div class="animate-pulse">
  <!-- Avatar -->
  <div class="w-12 h-12 bg-gray-200 dark:bg-gray-700 rounded-full"></div>

  <!-- Text lines -->
  <div class="space-y-2 mt-4">
    <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
    <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
  </div>

  <!-- Card skeleton -->
  <div class="h-32 bg-gray-200 dark:bg-gray-700 rounded-lg mt-4"></div>
</div>
```

---

## Avatar

```html
<!-- Image avatar -->
<img src="..." class="w-10 h-10 rounded-full object-cover" alt="User" />

<!-- Initials avatar -->
<div class="
  w-10 h-10 rounded-full
  bg-primary-500 text-white
  flex items-center justify-center
  font-medium text-sm
">
  JD
</div>

<!-- Avatar group -->
<div class="flex -space-x-2">
  <img class="w-8 h-8 rounded-full ring-2 ring-white" src="..." />
  <img class="w-8 h-8 rounded-full ring-2 ring-white" src="..." />
  <div class="w-8 h-8 rounded-full ring-2 ring-white bg-gray-200 flex items-center justify-center text-xs">
    +3
  </div>
</div>
```
