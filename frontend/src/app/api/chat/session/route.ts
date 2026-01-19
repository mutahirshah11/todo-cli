import { NextResponse } from 'next/server';

export async function POST() {
  // Mock response for Phase 3.2 local development
  // In Phase 3.3/3.4 this will connect to the real backend
  
  // Simulating a delay
  await new Promise((resolve) => setTimeout(resolve, 500));

  return NextResponse.json({
    client_secret: "mock_client_secret_" + Math.random().toString(36).slice(2),
    thread_id: "mock_thread_" + Math.random().toString(36).slice(2)
  });
}
