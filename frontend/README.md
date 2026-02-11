# Tickwen Frontend

A premium task management application built with Next.js, TypeScript, and Tailwind CSS.

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

### Running the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

### Environment Variables

Create a `.env.local` file in the root of the frontend directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:7860/api
```

### Building for Production

```bash
npm run build
npm start
```

### Running Tests

```bash
npm test
```

### Linting

```bash
npm run lint
```

## Features

- **Dashboard**: View, complete, and delete tasks
- **Task Creation/Editing**: Create and edit tasks with title and description
- **Authentication**: Login and registration flows
- **Filtering**: Client-side filtering of tasks
- **Responsive Design**: Works on mobile and desktop
- **Dark/Light Mode**: Theme switching with persistence
- **Error Handling**: Toast notifications for user feedback

## Tech Stack

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Forms**: React Hook Form + Zod
- **Icons**: Lucide React
- **Toasts**: Sonner
- **Testing**: Jest + React Testing Library
- **Theme**: next-themes

## Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── app/               # Next.js App Router pages
│   │   ├── (auth)/        # Login/Register routes
│   │   ├── dashboard/     # Protected routes
│   │   └── page.tsx       # Landing page
│   ├── components/
│   │   ├── ui/           # Shared UI primitives
│   │   └── feature/      # Domain components (TaskItem, etc.)
│   ├── lib/
│   │   ├── api.ts        # API Client
│   │   ├── store.ts      # Zustand Store
│   │   ├── schemas.ts    # Zod validation schemas
│   │   └── types.ts      # TypeScript interfaces
│   └── __tests__/        # Tests
├── package.json
├── tailwind.config.ts
└── next.config.js
```
