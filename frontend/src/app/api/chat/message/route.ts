import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  try {
    const { message, history, user_id } = await req.json();

    // Extract Authorization header from the incoming request
    const authHeader = req.headers.get("authorization");

    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };

    if (authHeader) {
      headers["Authorization"] = authHeader;
    }

    // Call the actual FastAPI backend
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:7860';
    // Remove trailing slash if present
    const cleanBaseUrl = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;
    // Construct URL: Check if base url already has /api/v1
    const endpoint = cleanBaseUrl.includes('/api/v1') 
      ? `${cleanBaseUrl}/agent/chat` 
      : `${cleanBaseUrl}/api/v1/agent/chat`;

    const backendRes = await fetch(endpoint, {
      method: "POST",
      headers,
      body: JSON.stringify({ message, history, user_id }),
    });

    if (!backendRes.ok) {
      const errorData = await backendRes.json();
      throw new Error(errorData.detail || "Backend failed");
    }

    const data = await backendRes.json();
    return NextResponse.json({ response: data.response });

  } catch (error: any) {
    console.error("Agent error:", error);
    return NextResponse.json(
      { response: "I'm having trouble thinking right now. Please make sure the backend server is running." },
      { status: 500 }
    );
  }
}
