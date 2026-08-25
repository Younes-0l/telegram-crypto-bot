# 💰 Crypto Price Bot

A Telegram bot for tracking cryptocurrency prices, managing a personal watchlist, setting price alerts, and monitoring a simple portfolio with live profit/loss calculation — built with a clean, layered backend architecture.

> Live prices are fetched from the [Tabdeal](https://tabdeal.org) exchange API and cached with Redis to keep the bot fast and avoid hitting API rate limits.

---

## ✨ Features

- **💰 Live Price Lookup** — Get the current price of any supported coin in Toman (IRT), pulled from real market trades.
- **⭐ Personal Watchlist** — Save your favorite coins and see all their prices at a glance, with one tap to add or remove.
- **🔔 Price Alerts** — Set a target price for any coin and get notified automatically the moment it's crossed (checked every 60 seconds in the background).
- **📊 Portfolio Tracking** — Record how much of each coin you hold and your average buy price; the bot calculates your current value and live profit/loss (amount + percentage).
- **⚡ Redis Caching** — Price requests are cached for 20 seconds, cutting exchange API calls dramatically and keeping response times near-instant on cache hits.
- **🛡️ Resilient by Design** — The bot keeps working (just slower) if Redis or the exchange API is temporarily unavailable, instead of freezing or crashing.

---

## 🏗️ Architecture

The project follows a layered architecture to keep concerns separated and the codebase testable:

```
Telegram Update
      │
      ▼
   Handlers        →  parse the update, talk to Telegram, call services
      │
      ▼
   Services        →  business logic (pricing, caching, profit/loss math)
      │
      ▼
 Repositories       →  database queries only, no business logic
      │
      ▼
  PostgreSQL / Redis
```

This means, for example, that `PriceService` doesn't know anything about Telegram, and handlers don't know anything about SQL — each layer only talks to the one below it.

### Project structure

```
cryptocurrency/
├── main.py                    # Entry point: builds the app, registers handlers & jobs
├── config.py                  # Environment-based configuration
├── handlers/                  # Telegram update handlers (one file per feature)
│   ├── start.py
│   ├── price.py
│   ├── watchlist.py
│   ├── alert.py
│   ├── alert_conversation.py
│   ├── portfolio.py
│   ├── holding_conversation.py
│   ├── navigation.py
│   ├── error_handler.py
│   └── common.py
├── services/                  # Business logic
│   ├── price_service.py
│   ├── watchlist_service.py
│   ├── alert_checker.py
│   └── portfolio_service.py
├── repositories/               # Database access layer
│   ├── watchlist_repository.py
│   ├── alert_repository.py
│   └── holding_repository.py
├── keyboards/                  # Inline keyboard builders
├── database/                   # Models, session, Redis client
└── requirements.txt
```

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Bot framework | [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) |
| Database | PostgreSQL + SQLAlchemy |
| Caching | Redis |
| Exchange API | [Tabdeal](https://docs.tabdeal.org) |
| Scheduling | `python-telegram-bot` JobQueue |
| Language | Python 3.11+ |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- PostgreSQL
- Redis (or [Memurai](https://www.memurai.com) on Windows)
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- A Tabdeal API key & secret

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/crypto-price-bot.git
   cd crypto-price-bot
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv env
   source env/bin/activate   # On Windows: env\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Copy `.env.example` to `.env` and fill in your own values:
   ```bash
   cp .env.example .env
   ```

   ```env
   BOT_TOKEN=your_telegram_bot_token
   TABDEAL_API_KEY=your_tabdeal_api_key
   TABDEAL_SECURITY_KEY=your_tabdeal_secret_key
   DATABASE_URL=postgresql://user:password@localhost:5432/crypto_bot
   REDIS_HOST=127.0.0.1
   REDIS_PORT=6379
   REDIS_DB=0
   ```

4. **Make sure PostgreSQL and Redis are running**, then start the bot:
   ```bash
   python main.py
   ```

   Database tables are created automatically on first run.

---

## 📖 How It Works

### Price caching

Every price request first checks Redis. On a cache miss, the bot fetches the latest trade price from Tabdeal, stores it in Redis with a 20-second TTL, and returns it. On a cache hit, the response is near-instant (sub-millisecond) instead of taking 1–3 seconds for a live API call.

### Price alerts

When a user sets an alert, it's stored in PostgreSQL. A background job (`JobQueue.run_repeating`) checks all active alerts every 60 seconds against the (cached) current price, and sends a Telegram message the moment a target is crossed — then deactivates the alert.

### Portfolio

Instead of tracking a full transaction ledger, the bot stores one holding record per coin per user (amount + average buy price). This keeps the profit/loss math simple:

```
profit = (current_price - avg_buy_price) × amount
```

---

## 📸 Screenshots

<!-- Add screenshots here, e.g.: -->
<!-- ![Main menu](screenshots/main_menu.png) -->
<!-- ![Watchlist](screenshots/watchlist.png) -->
<!-- ![Price alert](screenshots/alert.png) -->
<!-- ![Portfolio](screenshots/portfolio.png) -->

| Main Menu | Watchlist | Price Alert | Portfolio |
|---|---|---|---|
| _screenshot_ | _screenshot_ | _screenshot_ | _screenshot_ |

---

## 🗺️ Possible Improvements

- Price charts (candlestick/line, via matplotlib)
- Multi-language support (Persian/English toggle)
- Docker & docker-compose for one-command setup
- USDT / multi-currency pricing
- Unit tests for the service layer

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Built by **[Your Name]** as part of a portfolio of Telegram bots.
Other projects: Group Management Bot · Instagram/YouTube Downloader Bot