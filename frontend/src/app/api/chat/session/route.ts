import { NextResponse } from 'next/server';

export async function POST() {
  try {
    const apiKey = process.env.OPENAI_API_KEY;

    if (!apiKey || apiKey === "MISSING_KEY") {
      console.warn("OPENAI_API_KEY is missing. Realtime session will fail.");
      return NextResponse.json(
        { error: "Please set a valid OPENAI_API_KEY in your .env file to use ChatKit UI." },
        { status: 400 }
      );
    }

    // Attempt to create a real session
    const response = await fetch("https://api.openai.com/v1/realtime/sessions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "gpt-4o-realtime-preview-2024-12-17",
        modalities: ["text"],
        instructions: "You are a task management assistant. Use provided tools.",
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("OpenAI Realtime Error:", errorText);
      return NextResponse.json({ error: "OpenAI API error: " + errorText }, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json({
      client_secret: data.client_secret.value,
    });

  } catch (error: any) {
    console.error("Internal Session Error:", error);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}
