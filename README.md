# ICT SMC Sniper — Telegram connector starter

This starter only tests Telegram messaging. It does not read Deriv prices or generate trading signals.

## Render environment variables
- `BOT_TOKEN`: your Telegram bot token (keep private)
- `WEBHOOK_SECRET`: random letters/numbers, at least 20 characters
- `SETUP_KEY`: a different random secret for one-time webhook setup

After deployment, visit:
`https://YOUR-RENDER-SERVICE.onrender.com/setup-webhook?key=YOUR_SETUP_KEY`

Replace the example service URL and key with your own values. Then send `/start` to your Telegram bot.
Free hosting can sleep or have limits. Live market data and ICT/SMC analysis are not included.
