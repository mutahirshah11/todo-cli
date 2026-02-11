# Utility Class Reference

Quick reference for commonly used Tailwind CSS utilities.

## Spacing

### Padding

| Class | CSS |
|-------|-----|
| `p-0` | `padding: 0` |
| `p-1` | `padding: 0.25rem` (4px) |
| `p-2` | `padding: 0.5rem` (8px) |
| `p-4` | `padding: 1rem` (16px) |
| `p-6` | `padding: 1.5rem` (24px) |
| `p-8` | `padding: 2rem` (32px) |
| `px-*` | Horizontal padding |
| `py-*` | Vertical padding |
| `pt-*` `pr-*` `pb-*` `pl-*` | Individual sides |

### Margin

Same scale as padding: `m-*`, `mx-*`, `my-*`, `mt-*`, `mr-*`, `mb-*`, `ml-*`

Special values:
| Class | CSS |
|-------|-----|
| `m-auto` | `margin: auto` |
| `-m-2` | `margin: -0.5rem` (negative) |

### Space Between

```html
<div class="space-y-4">  <!-- Vertical spacing between children -->
<div class="space-x-4">  <!-- Horizontal spacing between children -->
```

### Gap (Flexbox/Grid)

```html
<div class="gap-4">      <!-- Both directions -->
<div class="gap-x-4">    <!-- Column gap -->
<div class="gap-y-4">    <!-- Row gap -->
```

---

## Sizing

### Width

| Class | CSS |
|-------|-----|
| `w-0` | `width: 0` |
| `w-1` | `width: 0.25rem` |
| `w-full` | `width: 100%` |
| `w-screen` | `width: 100vw` |
| `w-auto` | `width: auto` |
| `w-1/2` | `width: 50%` |
| `w-1/3` | `width: 33.333%` |
| `w-2/3` | `width: 66.667%` |
| `w-1/4` | `width: 25%` |
| `w-fit` | `width: fit-content` |
| `w-min` | `width: min-content` |
| `w-max` | `width: max-content` |

### Height

Same patterns: `h-*`, `h-full`, `h-screen`, `h-auto`, `h-fit`, `h-min`, `h-max`

### Min/Max

| Class | CSS |
|-------|-----|
| `min-w-0` | `min-width: 0` |
| `min-w-full` | `min-width: 100%` |
| `max-w-sm` | `max-width: 24rem` |
| `max-w-md` | `max-width: 28rem` |
| `max-w-lg` | `max-width: 32rem` |
| `max-w-xl` | `max-width: 36rem` |
| `max-w-2xl` | `max-width: 42rem` |
| `max-w-4xl` | `max-width: 56rem` |
| `max-w-7xl` | `max-width: 80rem` |
| `max-w-full` | `max-width: 100%` |
| `max-w-none` | `max-width: none` |
| `min-h-screen` | `min-height: 100vh` |
| `max-h-screen` | `max-height: 100vh` |

---

## Display

| Class | CSS |
|-------|-----|
| `hidden` | `display: none` |
| `block` | `display: block` |
| `inline` | `display: inline` |
| `inline-block` | `display: inline-block` |
| `flex` | `display: flex` |
| `inline-flex` | `display: inline-flex` |
| `grid` | `display: grid` |
| `inline-grid` | `display: inline-grid` |
| `contents` | `display: contents` |

---

## Flexbox

### Container

| Class | CSS |
|-------|-----|
| `flex` | `display: flex` |
| `flex-row` | `flex-direction: row` |
| `flex-col` | `flex-direction: column` |
| `flex-row-reverse` | `flex-direction: row-reverse` |
| `flex-wrap` | `flex-wrap: wrap` |
| `flex-nowrap` | `flex-wrap: nowrap` |

### Alignment

| Class | CSS |
|-------|-----|
| `justify-start` | `justify-content: flex-start` |
| `justify-center` | `justify-content: center` |
| `justify-end` | `justify-content: flex-end` |
| `justify-between` | `justify-content: space-between` |
| `justify-around` | `justify-content: space-around` |
| `justify-evenly` | `justify-content: space-evenly` |
| `items-start` | `align-items: flex-start` |
| `items-center` | `align-items: center` |
| `items-end` | `align-items: flex-end` |
| `items-stretch` | `align-items: stretch` |
| `items-baseline` | `align-items: baseline` |

### Item

| Class | CSS |
|-------|-----|
| `flex-1` | `flex: 1 1 0%` |
| `flex-auto` | `flex: 1 1 auto` |
| `flex-none` | `flex: none` |
| `flex-grow` | `flex-grow: 1` |
| `flex-grow-0` | `flex-grow: 0` |
| `flex-shrink` | `flex-shrink: 1` |
| `flex-shrink-0` | `flex-shrink: 0` |
| `self-auto` | `align-self: auto` |
| `self-start` | `align-self: flex-start` |
| `self-center` | `align-self: center` |
| `self-end` | `align-self: flex-end` |

---

## Grid

### Container

| Class | CSS |
|-------|-----|
| `grid` | `display: grid` |
| `grid-cols-1` | `grid-template-columns: repeat(1, minmax(0, 1fr))` |
| `grid-cols-2` | `grid-template-columns: repeat(2, minmax(0, 1fr))` |
| `grid-cols-3` | `grid-template-columns: repeat(3, minmax(0, 1fr))` |
| `grid-cols-4` | `grid-template-columns: repeat(4, minmax(0, 1fr))` |
| `grid-cols-12` | `grid-template-columns: repeat(12, minmax(0, 1fr))` |
| `grid-rows-*` | Row equivalents |

### Item

| Class | CSS |
|-------|-----|
| `col-span-1` | `grid-column: span 1` |
| `col-span-2` | `grid-column: span 2` |
| `col-span-full` | `grid-column: 1 / -1` |
| `col-start-1` | `grid-column-start: 1` |
| `row-span-*` | Row equivalents |

---

## Position

| Class | CSS |
|-------|-----|
| `static` | `position: static` |
| `relative` | `position: relative` |
| `absolute` | `position: absolute` |
| `fixed` | `position: fixed` |
| `sticky` | `position: sticky` |

### Placement

| Class | CSS |
|-------|-----|
| `inset-0` | `top: 0; right: 0; bottom: 0; left: 0` |
| `inset-x-0` | `left: 0; right: 0` |
| `inset-y-0` | `top: 0; bottom: 0` |
| `top-0` | `top: 0` |
| `right-0` | `right: 0` |
| `bottom-0` | `bottom: 0` |
| `left-0` | `left: 0` |
| `-top-4` | `top: -1rem` (negative) |

---

## Typography

### Font Size

| Class | Size |
|-------|------|
| `text-xs` | 12px |
| `text-sm` | 14px |
| `text-base` | 16px |
| `text-lg` | 18px |
| `text-xl` | 20px |
| `text-2xl` | 24px |
| `text-3xl` | 30px |
| `text-4xl` | 36px |
| `text-5xl` | 48px |
| `text-6xl` | 60px |

### Font Weight

| Class | Weight |
|-------|--------|
| `font-thin` | 100 |
| `font-light` | 300 |
| `font-normal` | 400 |
| `font-medium` | 500 |
| `font-semibold` | 600 |
| `font-bold` | 700 |
| `font-extrabold` | 800 |

### Text Alignment

`text-left` | `text-center` | `text-right` | `text-justify`

### Text Transform

`uppercase` | `lowercase` | `capitalize` | `normal-case`

### Text Decoration

`underline` | `line-through` | `no-underline`

### Line Height

| Class | Value |
|-------|-------|
| `leading-none` | 1 |
| `leading-tight` | 1.25 |
| `leading-normal` | 1.5 |
| `leading-relaxed` | 1.625 |
| `leading-loose` | 2 |

### Whitespace & Overflow

| Class | CSS |
|-------|-----|
| `whitespace-nowrap` | `white-space: nowrap` |
| `whitespace-pre` | `white-space: pre` |
| `truncate` | `overflow: hidden; text-overflow: ellipsis; white-space: nowrap` |
| `line-clamp-2` | Limit to 2 lines with ellipsis |

---

## Colors

### Text Color

```html
<p class="text-gray-900">     <!-- Dark text -->
<p class="text-gray-600">     <!-- Medium text -->
<p class="text-gray-400">     <!-- Light text -->
<p class="text-primary-500">  <!-- Brand color -->
<p class="text-red-500">      <!-- Error -->
<p class="text-green-500">    <!-- Success -->
```

### Background Color

```html
<div class="bg-white">        <!-- White -->
<div class="bg-gray-100">     <!-- Light gray -->
<div class="bg-gray-900">     <!-- Dark -->
<div class="bg-primary-500">  <!-- Brand -->
<div class="bg-transparent">  <!-- Transparent -->
```

### Opacity

```html
<div class="bg-black/50">     <!-- 50% opacity -->
<div class="text-white/80">   <!-- 80% opacity -->
```

---

## Borders

### Border Width

| Class | CSS |
|-------|-----|
| `border` | `border-width: 1px` |
| `border-0` | `border-width: 0` |
| `border-2` | `border-width: 2px` |
| `border-4` | `border-width: 4px` |
| `border-t` | `border-top-width: 1px` |
| `border-r` | `border-right-width: 1px` |
| `border-b` | `border-bottom-width: 1px` |
| `border-l` | `border-left-width: 1px` |

### Border Radius

| Class | CSS |
|-------|-----|
| `rounded-none` | `border-radius: 0` |
| `rounded-sm` | `border-radius: 0.125rem` |
| `rounded` | `border-radius: 0.25rem` |
| `rounded-md` | `border-radius: 0.375rem` |
| `rounded-lg` | `border-radius: 0.5rem` |
| `rounded-xl` | `border-radius: 0.75rem` |
| `rounded-2xl` | `border-radius: 1rem` |
| `rounded-full` | `border-radius: 9999px` |
| `rounded-t-lg` | Top corners only |
| `rounded-b-lg` | Bottom corners only |

### Border Color

```html
<div class="border border-gray-200">
<div class="border border-primary-500">
```

---

## Shadows

| Class | Description |
|-------|-------------|
| `shadow-sm` | Small shadow |
| `shadow` | Default shadow |
| `shadow-md` | Medium shadow |
| `shadow-lg` | Large shadow |
| `shadow-xl` | Extra large shadow |
| `shadow-2xl` | Huge shadow |
| `shadow-inner` | Inner shadow |
| `shadow-none` | No shadow |

---

## Transitions & Animations

### Transition

```html
<div class="transition">                    <!-- All properties -->
<div class="transition-colors">             <!-- Colors only -->
<div class="transition-opacity">            <!-- Opacity only -->
<div class="transition-transform">          <!-- Transform only -->
<div class="transition-all duration-300">   <!-- All + duration -->
<div class="ease-in-out">                   <!-- Timing function -->
```

### Duration

`duration-75` | `duration-100` | `duration-150` | `duration-200` | `duration-300` | `duration-500`

### Animations

```html
<div class="animate-spin">    <!-- Spinner -->
<div class="animate-ping">    <!-- Ping effect -->
<div class="animate-pulse">   <!-- Pulse (skeleton) -->
<div class="animate-bounce">  <!-- Bounce -->
```

---

## Transforms

```html
<div class="scale-95">           <!-- Scale down -->
<div class="scale-105">          <!-- Scale up -->
<div class="rotate-45">          <!-- Rotate -->
<div class="translate-x-4">      <!-- Move right -->
<div class="translate-y-4">      <!-- Move down -->
<div class="-translate-x-1/2">   <!-- Center horizontally -->
```

---

## Overflow

| Class | CSS |
|-------|-----|
| `overflow-auto` | `overflow: auto` |
| `overflow-hidden` | `overflow: hidden` |
| `overflow-visible` | `overflow: visible` |
| `overflow-scroll` | `overflow: scroll` |
| `overflow-x-auto` | `overflow-x: auto` |
| `overflow-y-auto` | `overflow-y: auto` |

---

## Z-Index

| Class | CSS |
|-------|-----|
| `z-0` | `z-index: 0` |
| `z-10` | `z-index: 10` |
| `z-20` | `z-index: 20` |
| `z-30` | `z-index: 30` |
| `z-40` | `z-index: 40` |
| `z-50` | `z-index: 50` |
| `z-auto` | `z-index: auto` |

---

## Cursor

`cursor-pointer` | `cursor-default` | `cursor-wait` | `cursor-text` | `cursor-move` | `cursor-not-allowed` | `cursor-grab`

---

## Pointer Events

`pointer-events-none` | `pointer-events-auto`

---

## Select

`select-none` | `select-text` | `select-all` | `select-auto`

---

## Object Fit (Images)

| Class | CSS |
|-------|-----|
| `object-contain` | `object-fit: contain` |
| `object-cover` | `object-fit: cover` |
| `object-fill` | `object-fit: fill` |
| `object-none` | `object-fit: none` |
| `object-center` | `object-position: center` |
| `object-top` | `object-position: top` |

---

## Aspect Ratio

| Class | Ratio |
|-------|-------|
| `aspect-auto` | Auto |
| `aspect-square` | 1:1 |
| `aspect-video` | 16:9 |

---

## Ring (Focus Outline)

```html
<button class="focus:ring-2 focus:ring-primary-500 focus:ring-offset-2">
<input class="focus:ring-2 focus:ring-blue-500">
```

| Class | Description |
|-------|-------------|
| `ring-0` | No ring |
| `ring-1` | 1px ring |
| `ring-2` | 2px ring |
| `ring-4` | 4px ring |
| `ring-offset-2` | 2px offset |
| `ring-blue-500` | Ring color |
