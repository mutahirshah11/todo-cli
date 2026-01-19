import { render, screen, waitFor } from "@testing-library/react";
import { ChatContainer } from "@/components/chat/chat-container";
import { useChatKit } from "@openai/chatkit-react";

// Mock @openai/chatkit-react
jest.mock("@openai/chatkit-react", () => ({
  ChatKit: () => <div data-testid="chatkit-mock">ChatKit UI</div>,
  useChatKit: jest.fn(),
}));

// Mock @/lib/utils
jest.mock("@/lib/utils", () => ({
  cn: (...args: any[]) => args.filter(Boolean).join(" "),
}));

// Mock sonner
jest.mock("sonner", () => ({
  toast: {
    error: jest.fn(),
  },
}));

// Mock global fetch
global.fetch = jest.fn();

// Mock lucide-react
jest.mock("lucide-react", () => ({
  Loader2: () => <div data-testid="loader-mock" />,
}));

describe("ChatContainer", () => {
  beforeEach(() => {
    (useChatKit as jest.Mock).mockReturnValue({
      control: {},
    });
    (global.fetch as jest.Mock).mockClear();
  });

  it("renders the ChatKit component", () => {
    render(<ChatContainer />);
    expect(screen.getByTestId("chatkit-mock")).toBeInTheDocument();
  });

  it("calls getClientSecret with correct endpoint", async () => {
    // We need to trigger the getClientSecret function passed to useChatKit.
    // Since useChatKit is called inside the component, we can spy on the hook call.
    render(<ChatContainer />);
    
    // Get the config passed to useChatKit
    const config = (useChatKit as jest.Mock).mock.calls[0][0];
    const getClientSecret = config.api.getClientSecret;

    // Mock fetch response
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ client_secret: "secret_123" }),
    });

    const secret = await getClientSecret();
    
    expect(global.fetch).toHaveBeenCalledWith("/api/chat/session", expect.objectContaining({
      method: "POST"
    }));
    expect(secret).toBe("secret_123");
  });

  it("handles getClientSecret error", async () => {
    render(<ChatContainer />);
    const config = (useChatKit as jest.Mock).mock.calls[0][0];
    const getClientSecret = config.api.getClientSecret;

    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      statusText: "Internal Server Error"
    });

    await expect(getClientSecret()).rejects.toThrow("Session creation failed: Internal Server Error");
  });
});