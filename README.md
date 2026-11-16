# Agent Notifier

A local MCP server that gives any compatible agent a `notify_phone` tool. It
sends a Telegram message when the agent deliberately calls the tool for
meaningful completed work or a request that needs your attention.

## Set up

1. Create a Telegram bot with @BotFather and send `/start` to your new bot.
2. Copy `.env.example` to `.env` and fill in `TELEGRAM_BOT_TOKEN`. Keep `.env`
   private; Git ignores it.
3. Create the environment and install the project:

   ```sh
   python3 -m venv .venv
   .venv/bin/python -m pip install -e .
   ```

4. Run `.venv/bin/python src/telegram_notify.py chat-id`, then put the returned
   number in `TELEGRAM_CHAT_ID` in `.env`.
5. Run `.venv/bin/python src/telegram_notify.py send "Agent Notifier test"`.

The Python code loads `.env` itself, so you do not need to source it in your
shell. An already-exported environment variable takes precedence over `.env`.

## Connect to an agent

Configure your agent's MCP client to start this server over STDIO using the
absolute command below. This works with MCP-capable clients, including Codex
and Claude, that support local STDIO servers.

```sh
/absolute/path/to/agent-notifier/.venv/bin/python /absolute/path/to/agent-notifier/src/mcp_server.py
```

### Codex example

In the ChatGPT desktop app, open **Settings > MCP servers > Add server**. Name
the server `agent-notifier`, choose **STDIO**, and enter that command.

Save and restart the app. In a Codex chat, use `/mcp` to confirm that
`agent-notifier` exposes `notify_phone`.

The tool sends to the single chat ID in `.env`; callers cannot choose a
recipient. It does not monitor agent activity automatically. Approval-request
hooks can be added in clients that support them if automatic approval alerts
are needed.
