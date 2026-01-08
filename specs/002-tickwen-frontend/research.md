# Research & Technical Decisions: Tickwen Frontend

**Feature**: 002-tickwen-frontend
**Date**: 2026-01-07

## 1. Technical Stack Decisions

### Framework: Next.js (App Router)
- **Decision**: Use Next.js 14+ with App Router (`app/` directory).
- **Rationale**: User requested "latest" Next.js. App Router provides better performance, simplified routing, and server components where applicable.
- **Alternatives**: Pages router (legacy).

### Styling: Tailwind CSS
- **Decision**: Tailwind CSS with `clsx` and `tailwind-merge` for conditional class management.
- **Rationale**: User requested Tailwind. It enables "Premium" custom designs without fighting framework defaults.
- **Alternatives**: CSS Modules, Styled Components (rejected based on user constraint).

### State Management: Zustand
- **Decision**: Zustand.
- **Rationale**: The spec suggested Context or Zustand. Zustand is simpler, has less boilerplate than Context + Reducer, and avoids unnecessary re-renders. Fits Article V (Simplicity).
- **Alternatives**: React Context (more boilerplate), Redux (overkill).

### Form Management: React Hook Form + Zod
- **Decision**: `react-hook-form` for logic, `zod` for validation.
- **Rationale**: Standard industry practice. Ensures strict validation (Article III - Correctness) and improves UX with inline errors as per spec. Zod schemas can be shared or mirrored from backend rules.

### API Client: Native Fetch
- **Decision**: Native `fetch` with a custom wrapper utility.
- **Rationale**: Next.js extends `fetch` with caching/revalidation controls. Reduces bundle size compared to Axios.
- **Alternatives**: Axios (unnecessary dependency).

### Icons: Lucide React
- **Decision**: `lucide-react`.
- **Rationale**: Clean, modern SVG icons that match the "Vercel/Neon" aesthetic.
- **Alternatives**: Heroicons, FontAwesome.

### Testing: Jest + React Testing Library
- **Decision**: Jest for test runner, RTL for component testing.
- **Rationale**: Constitution Article I requires Strict TDD. This is the standard testing stack for React.

## 2. Project Structure (Next.js Standard)

The project will follow the standard `src/` directory convention to keep configuration files separate from source code.

```
src/
  app/                 # App Router pages/layouts
    (auth)/            # Route group for login/register
    dashboard/         # Dashboard page
    page.tsx           # Landing page
  components/
    ui/                # Generic UI components (buttons, inputs)
    feature/           # Feature-specific components (TaskItem, TaskList)
  lib/                 # Utilities
    api.ts             # API client wrapper
    store.ts           # Zustand store
    types.ts           # TypeScript interfaces
    utils.ts           # Helper functions (cn, etc.)
  __tests__/           # Co-located or root test folder (per convention)
```

## 3. "Premium" UI/UX Implementation Strategy

To achieve the Vercel/Neon look:
- **Typography**: Inter (default Next.js font) or similar sans-serif.
- **Spacing**: Generous padding/margin using Tailwind's spacing scale.
- **Colors**: High contrast. Dark mode (persisted via localStorage).
  - Backgrounds: `#000000` or very dark gray for dark mode.
  - Accents: Subtle borders, glow effects for active states.
- **Interactions**:
  - `framer-motion` for smooth transitions (toasts, modals, list reordering).
  - Hover states on all interactive elements.

## 4. Unknowns Resolved
- **Auth UI**: Dedicated pages `/login` and `/register`.
- **Delete Confirmation**: Custom Modal (implemented with Dialog primitive).
- **Feedback**: Toasts (using `sonner` or similar lightweight lib, or custom build). *Decision: `sonner` for better UX/simplicity.*
- **Theme**: `next-themes` for easy light/dark mode persistence implementation.

## 5. Security & Privacy (Constitution Article II)
- **Token Storage**: `localStorage` (per spec clarification).
- **XSS Protection**: React automatically escapes content.
- **CSRF**: API should handle standard CORS; frontend sends token in Header.

