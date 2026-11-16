"""Local MCP server exposing a deliberate phone notification tool."""

from typing import Literal

from mcp.server import MCPServer

from telegram_notify import send_message


mcp = MCPServer(
    "agent-notifier",
    version="0.1.0",
    instructions=(
        "Use notify_phone only when substantial requested work is finished or the "
        "user must act to unblock it. Do not notify for routine replies, progress "
        "updates, or each prompt. Send at most one concise alert per event. Never "
        "include credentials, private file contents, or sensitive logs."
    ),
)


@mcp.tool()
def notify_phone(
    event: Literal["task_finished", "needs_attention"], summary: str
) -> str:
    """Alert the owner's phone for meaningful task completion or required action.

    Call only for a substantial finished task or when work cannot continue without
    the user's input or approval. Do not call for ordinary conversational replies.
    """
    summary = summary.strip()
    if not summary or len(summary) > 500:
        raise ValueError("Summary must contain 1 to 500 characters")

    title = "Codex task finished" if event == "task_finished" else "Codex needs attention"
    send_message(f"{title}\n{summary}")
    return "Phone notification sent."


if __name__ == "__main__":
    mcp.run(transport="stdio")
