import { NextRequest, NextResponse } from 'next/server';

// This function can be marked `async` if using `await` inside
export function proxy(request: NextRequest) {
  // Define protected routes that require authentication
  const protectedPaths = ['/dashboard', '/create', '/edit'];
  const currentPath = request.nextUrl.pathname;

  // Check if the current path is a protected route
  const isProtectedRoute = protectedPaths.some(path =>
    currentPath.startsWith(path)
  );

  // For this demo, we'll check if there's a token in localStorage
  // In a real app, this would involve checking cookies or headers
  if (isProtectedRoute) {
    // In a real implementation, we'd check for a valid token
    // For now, we'll just allow all requests but in a real app you'd check:
    // const token = request.cookies.get('auth-token') || localStorage.getItem('token');

    // For demo purposes, we'll allow all requests to protected routes
    // In a real app, redirect to login if no valid token exists
    // if (!token) {
    //   return NextResponse.redirect(new URL('/login', request.url));
    // }
  }

  return NextResponse.next();
}

// See "Matching Paths" to learn more: https://nextjs.org/docs/app/building-your-application/routing/middleware#matching-paths
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};