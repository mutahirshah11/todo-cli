---
name: tailwind-css-system
description: |
  Tailwind CSS utility-first styling patterns, responsive design, and configuration for consistent UI.
  This skill should be used when styling components with Tailwind utilities, implementing responsive
  layouts, configuring design tokens, creating dark mode, building reusable UI patterns (buttons,
  cards, forms), or optimizing Tailwind for production.
---

# Tailwind CSS Design System

Guide for utility-first styling with Tailwind CSS v3+.

## Before Implementation

| Source | Gather |
|--------|--------|
| **Codebase** | Existing `tailwind.config.js`, color palette, component patterns |
| **Conversation** | Specific UI requirements, brand colors, breakpoint needs |
| **Skill References** | Patterns from `references/` (utilities, components, config) |
| **User Guidelines** | Design system tokens, accessibility requirements |

---

## Core Principle: Mobile-First

```
Base styles → sm: → md: → lg: → xl: → 2xl:
   ↑
Start here (no prefix = all screens)
```

**Wrong:** `lg:flex flex-col` (desktop-first thinking)
**Right:** `flex flex-col lg:flex-row` (mobile-first)

---

## Default Breakpoints

| Prefix | Min-Width | Target |
|--------|-----------|--------|
| (none) | 0px | Mobile (default) |
| `sm:` | 640px | Large phones |
| `md:` | 768px | Tablets |
| `lg:` | 1024px | Laptops |
| `xl:` | 1280px | Desktops |
| `2xl:` | 1536px | Large screens |

```html
<!-- Stacks on mobile, 2 cols on md, 3 cols on lg -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
```

---

## Spacing Scale (Default)

| Class | Value | Pixels |
|-------|-------|--------|
| `*-0` | 0 | 0px |
| `*-1` | 0.25rem | 4px |
| `*-2` | 0.5rem | 8px |
| `*-3` | 0.75rem | 12px |
| `*-4` | 1rem | 16px |
| `*-6` | 1.5rem | 24px |
| `*-8` | 2rem | 32px |
| `*-12` | 3rem | 48px |
| `*-16` | 4rem | 64px |

Use for: `p-*`, `m-*`, `gap-*`, `space-*`, `w-*`, `h-*`

---

## Color System

### Semantic Naming Pattern

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        // Brand colors
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        // Semantic colors
        success: '#22c55e',
        warning: '#f59e0b',
        error: '#ef4444',
        // Surface colors
        surface: {
          DEFAULT: '#ffffff',
          muted: '#f1f5f9',
        },
      },
    },
  },
}
```

### Usage

```html
<button class="bg-primary-500 hover:bg-primary-600 text-white">
<div class="bg-surface text-foreground">
<span class="text-error">
```

---

## Dark Mode

### Configuration (v3.4+)

```js
// tailwind.config.js
module.exports = {
  darkMode: 'selector', // or 'class' for older versions
}
```

### Pattern

```html
<!-- Always pair light and dark -->
<div class="bg-white dark:bg-gray-900">
  <h1 class="text-gray-900 dark:text-white">
  <p class="text-gray-600 dark:text-gray-300">
</div>
```

### Toggle Script

```html
<script>
  // Check on page load
  if (localStorage.theme === 'dark' ||
      (!localStorage.theme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark')
  }
</script>
```

---

## Typography Scale

| Class | Size | Line Height |
|-------|------|-------------|
| `text-xs` | 12px | 16px |
| `text-sm` | 14px | 20px |
| `text-base` | 16px | 24px |
| `text-lg` | 18px | 28px |
| `text-xl` | 20px | 28px |
| `text-2xl` | 24px | 32px |
| `text-3xl` | 30px | 36px |
| `text-4xl` | 36px | 40px |

### Font Weights

`font-normal` (400) | `font-medium` (500) | `font-semibold` (600) | `font-bold` (700)

---

## Layout Patterns

### Flexbox

```html
<!-- Center everything -->
<div class="flex items-center justify-center">

<!-- Space between with wrap -->
<div class="flex flex-wrap items-center justify-between gap-4">

<!-- Vertical stack -->
<div class="flex flex-col gap-2">

<!-- Horizontal on desktop, vertical on mobile -->
<div class="flex flex-col md:flex-row gap-4">
```

### Grid

```html
<!-- Responsive columns -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">

<!-- Fixed sidebar layout -->
<div class="grid grid-cols-[250px_1fr]">

<!-- Auto-fit (as many as fit) -->
<div class="grid grid-cols-[repeat(auto-fit,minmax(200px,1fr))] gap-4">
```

### Container

```html
<!-- Centered container with padding -->
<div class="container mx-auto px-4">

<!-- Max-width constraint -->
<div class="max-w-4xl mx-auto px-4">
```

---

## State Variants

### Interactive States

```html
<button class="
  bg-blue-500
  hover:bg-blue-600
  focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
  active:bg-blue-700
  disabled:opacity-50 disabled:cursor-not-allowed
">
```

### Group & Peer

```html
<!-- Group: parent state affects children -->
<div class="group">
  <span class="group-hover:text-blue-500">Hover parent</span>
</div>

<!-- Peer: sibling state affects siblings -->
<input class="peer" />
<span class="peer-invalid:text-red-500">Error message</span>
```

---

## Animations & Transitions

### Transitions

```html
<!-- Color transition -->
<button class="transition-colors duration-200">

<!-- All properties -->
<div class="transition-all duration-300 ease-in-out">

<!-- Transform -->
<div class="transition-transform hover:scale-105">
```

### Built-in Animations

```html
<div class="animate-spin">    <!-- Loading spinner -->
<div class="animate-pulse">   <!-- Skeleton loading -->
<div class="animate-bounce">  <!-- Attention grabber -->
```

---

## Arbitrary Values

Use sparingly—prefer config tokens.

```html
<!-- One-off values -->
<div class="w-[137px]">
<div class="bg-[#1a1a1a]">
<div class="grid-cols-[1fr_2fr_1fr]">
<div class="top-[calc(100%-4rem)]">
```

---

## Container Queries (v3.2+ Plugin)

```bash
npm install @tailwindcss/container-queries
```

```js
// tailwind.config.js
plugins: [require('@tailwindcss/container-queries')]
```

```html
<!-- Mark container -->
<div class="@container">
  <!-- Respond to container, not viewport -->
  <div class="@md:flex @lg:grid @lg:grid-cols-2">
</div>
```

---

## Component Extraction

### When to Use @apply

- Repeated utility patterns (3+ times)
- Framework components (buttons, inputs)
- Third-party library styling

### Pattern

```css
/* globals.css */
@layer components {
  .btn {
    @apply px-4 py-2 rounded-lg font-medium transition-colors;
  }
  .btn-primary {
    @apply btn bg-primary-500 text-white hover:bg-primary-600;
  }
  .input {
    @apply w-full px-3 py-2 border rounded-lg
           focus:ring-2 focus:ring-primary-500 focus:outline-none;
  }
}
```

---

## Quick Reference: Common Classes

### Spacing
`p-4` `px-4` `py-2` `m-auto` `mx-4` `my-2` `gap-4` `space-y-4`

### Sizing
`w-full` `w-1/2` `h-screen` `min-h-screen` `max-w-lg`

### Display
`hidden` `block` `flex` `grid` `inline-flex`

### Position
`relative` `absolute` `fixed` `sticky` `inset-0` `top-0`

### Borders
`border` `border-2` `border-gray-200` `rounded-lg` `rounded-full`

### Shadows
`shadow-sm` `shadow` `shadow-md` `shadow-lg` `shadow-xl`

### Z-Index
`z-0` `z-10` `z-20` `z-50` `z-auto`

---

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| `style="..."` inline | Use Tailwind utilities |
| Custom CSS for basics | Use built-in utilities |
| Arbitrary values everywhere | Define in config |
| `!important` overrides | Fix specificity properly |
| Huge class strings | Extract to component |
| Desktop-first (`lg:` then override) | Mobile-first (base then `lg:`) |

---

## Performance

### Production Build

Tailwind automatically purges unused CSS. Ensure content paths are correct:

```js
// tailwind.config.js
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
}
```

### Tips

- Keep `content` paths specific (avoid `**/*`)
- Don't dynamically construct class names: `text-${color}-500` ✗
- Use complete class names: `text-red-500` ✓

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/utility-reference.md` | Complete utility class reference |
| `references/component-patterns.md` | Button, card, form, nav patterns |
| `references/config-examples.md` | Configuration templates |
