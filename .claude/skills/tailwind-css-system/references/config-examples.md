# Tailwind Configuration Examples

Complete configuration templates and customization patterns.

## Complete Configuration Template

```js
// tailwind.config.js
const defaultTheme = require('tailwindcss/defaultTheme')

/** @type {import('tailwindcss').Config} */
module.exports = {
  // Content paths for purging
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],

  // Dark mode strategy
  darkMode: 'selector', // or 'class' for v3.3 and below

  theme: {
    // Override container
    container: {
      center: true,
      padding: {
        DEFAULT: '1rem',
        sm: '2rem',
        lg: '4rem',
        xl: '5rem',
      },
    },

    extend: {
      // Custom colors
      colors: {
        // Brand colors with shades
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#172554',
        },
        // Semantic colors
        success: {
          light: '#dcfce7',
          DEFAULT: '#22c55e',
          dark: '#15803d',
        },
        warning: {
          light: '#fef3c7',
          DEFAULT: '#f59e0b',
          dark: '#b45309',
        },
        error: {
          light: '#fee2e2',
          DEFAULT: '#ef4444',
          dark: '#b91c1c',
        },
        // Surface colors for dark mode
        surface: {
          50: '#fafafa',
          100: '#f4f4f5',
          200: '#e4e4e7',
          800: '#27272a',
          900: '#18181b',
          950: '#09090b',
        },
      },

      // Custom fonts
      fontFamily: {
        sans: ['Inter var', ...defaultTheme.fontFamily.sans],
        mono: ['JetBrains Mono', ...defaultTheme.fontFamily.mono],
      },

      // Custom font sizes
      fontSize: {
        '2xs': ['0.625rem', { lineHeight: '0.75rem' }],
      },

      // Custom spacing (extends default scale)
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },

      // Custom border radius
      borderRadius: {
        '4xl': '2rem',
      },

      // Custom shadows
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
        'inner-lg': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.1)',
      },

      // Custom animations
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },

      // Custom screens (breakpoints)
      screens: {
        'xs': '475px',
        '3xl': '1920px',
      },

      // Z-index scale
      zIndex: {
        '60': '60',
        '70': '70',
        '80': '80',
        '90': '90',
        '100': '100',
      },
    },
  },

  // Plugins
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/container-queries'),
  ],
}
```

---

## CSS Variables Integration

### Define CSS Variables

```css
/* globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 224.3 76.3% 48%;
  }
}
```

### Use in Config

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
    },
  },
}
```

---

## Forms Plugin Configuration

```js
// tailwind.config.js
module.exports = {
  plugins: [
    require('@tailwindcss/forms')({
      strategy: 'class', // Only generate classes, not base styles
    }),
  ],
}
```

### Usage

```html
<!-- With strategy: 'class' -->
<input type="text" class="form-input rounded-lg" />
<select class="form-select rounded-lg">...</select>
<textarea class="form-textarea rounded-lg">...</textarea>
<input type="checkbox" class="form-checkbox rounded" />
<input type="radio" class="form-radio" />
```

---

## Typography Plugin

```js
// tailwind.config.js
module.exports = {
  plugins: [
    require('@tailwindcss/typography'),
  ],
  theme: {
    extend: {
      typography: (theme) => ({
        DEFAULT: {
          css: {
            color: theme('colors.gray.700'),
            a: {
              color: theme('colors.primary.500'),
              '&:hover': {
                color: theme('colors.primary.600'),
              },
            },
            'code::before': { content: '""' },
            'code::after': { content: '""' },
          },
        },
        dark: {
          css: {
            color: theme('colors.gray.300'),
            a: {
              color: theme('colors.primary.400'),
            },
          },
        },
      }),
    },
  },
}
```

### Usage

```html
<article class="prose prose-lg dark:prose-dark max-w-none">
  <!-- Markdown content rendered here -->
</article>
```

---

## Container Queries Plugin

```js
// tailwind.config.js
module.exports = {
  plugins: [
    require('@tailwindcss/container-queries'),
  ],
}
```

### Usage

```html
<div class="@container">
  <div class="@sm:flex @md:grid @md:grid-cols-2 @lg:grid-cols-3">
    <!-- Responds to container width, not viewport -->
  </div>
</div>

<!-- Named container -->
<div class="@container/main">
  <div class="@lg/main:grid-cols-3">...</div>
</div>
```

---

## Custom Plugin Example

```js
// tailwind.config.js
const plugin = require('tailwindcss/plugin')

module.exports = {
  plugins: [
    plugin(function({ addUtilities, addComponents, theme }) {
      // Add custom utilities
      addUtilities({
        '.text-shadow': {
          'text-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
        },
        '.text-shadow-lg': {
          'text-shadow': '0 4px 8px rgba(0, 0, 0, 0.12)',
        },
      })

      // Add custom components
      addComponents({
        '.card': {
          backgroundColor: theme('colors.white'),
          borderRadius: theme('borderRadius.lg'),
          padding: theme('spacing.6'),
          boxShadow: theme('boxShadow.md'),
        },
        '.btn': {
          padding: `${theme('spacing.2')} ${theme('spacing.4')}`,
          borderRadius: theme('borderRadius.lg'),
          fontWeight: theme('fontWeight.medium'),
        },
      })
    }),
  ],
}
```

---

## PostCSS Configuration

```js
// postcss.config.js
module.exports = {
  plugins: {
    'tailwindcss': {},
    'autoprefixer': {},
    ...(process.env.NODE_ENV === 'production'
      ? { 'cssnano': { preset: 'default' } }
      : {}),
  },
}
```

---

## Next.js Integration

```js
// next.config.js - No special config needed for Tailwind

// tailwind.config.js
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
}
```

```tsx
// app/layout.tsx
import './globals.css'

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

---

## Safelist (Prevent Purging)

```js
// tailwind.config.js
module.exports = {
  safelist: [
    // Specific classes
    'bg-red-500',
    'text-3xl',

    // Pattern matching
    {
      pattern: /bg-(red|green|blue)-(100|500|700)/,
      variants: ['hover', 'dark'],
    },

    // Dynamic classes from CMS
    {
      pattern: /text-(sm|base|lg|xl)/,
    },
  ],
}
```

---

## Presets (Sharing Config)

```js
// tailwind-preset.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#1a73e8',
          secondary: '#5f6368',
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

// tailwind.config.js (in project)
module.exports = {
  presets: [
    require('./tailwind-preset'),
  ],
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
}
```

---

## Performance Tips

### 1. Specific Content Paths

```js
// Good - specific paths
content: [
  './src/components/**/*.tsx',
  './src/app/**/*.tsx',
]

// Bad - too broad
content: [
  './**/*.{js,ts,jsx,tsx}', // Scans node_modules!
]
```

### 2. Don't Construct Class Names

```tsx
// Bad - won't be detected
const color = 'red'
<div className={`bg-${color}-500`} />

// Good - full class names
<div className={color === 'red' ? 'bg-red-500' : 'bg-blue-500'} />
```

### 3. Use Safelist Sparingly

Only safelist classes that truly cannot be detected statically.

### 4. Production Build

```bash
# Tailwind automatically purges in production
NODE_ENV=production npm run build
```

Typical production CSS: **< 10KB** gzipped.
