# GZSB24 Football Bot

Telegram bot in Khmer with only two football features:
- Football news
- League standings

It does not use a football data API and does not provide live data. Content is read from `content.json` and must be updated manually.

## Run locally

1. Install Python 3.10 or newer.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a Telegram bot with [@BotFather](https://t.me/BotFather) and copy its token.
4. Set the token as an environment variable:
   - macOS/Linux: `export TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"`
   - Windows PowerShell: `$env:TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"`
5. Start the bot:
   ```bash
   python bot.py
   ```

## Commands

- `/start` — welcome menu
- `/news` — football news
- `/standings` — league standings
- `/help` — help

## Update content

Edit `content.json`:
- Add news items under `news`, each with `title` and `summary`.
- Add league tables under `standings`. Each league name maps to a list of rows with `pos`, `team`, and `points`.

Example:
```json
{
  "news": [
    {"title": "ព័ត៌មានថ្មី", "summary": "សេចក្តីសង្ខេបព័ត៌មានបាល់ទាត់។"}
  ],
  "standings": {
    "Premier League": [
      {"pos": 1, "team": "Team A", "points": 30},
      {"pos": 2, "team": "Team B", "points": 27}
    ]
  }
}
```

Keep the bot token private. The token alone connects the bot to Telegram, but the bot still needs to run on a computer or hosting service to stay online.
