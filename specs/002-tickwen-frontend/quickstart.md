# Quickstart: Tickwen Frontend

**Feature**: 002-tickwen-frontend

## Prerequisites
- Node.js 18+
- Backend running locally (usually on port 8000 or similar)

## Setup

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Environment Variables**
   Create `.env.local` in the root:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

3. **Run Development Server**
   ```bash
   npm run dev
   ```
   Open [http://localhost:3000](http://localhost:3000).

## Testing

- **Run Unit Tests**:
  ```bash
  npm test
  ```
- **Run Linting**:
  ```bash
  npm run lint
  ```

## Build

```bash
npm run build
npm start
```
