<div align="center">

# 📅 Event Management Telegram Bot

A powerful and asynchronous Telegram bot designed for event registration and order management. Built using modern Python technologies, featuring an administration panel, multi-order tracking, and full database integration.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-aiosqlite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Railway](https://img.shields.io/badge/Deployed%20on-Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)

</div>

---

## 🚀 Features

* **Multi-Ordering System:** Allows users to place multiple distinct orders without overwriting previous data, implemented via a strict One-to-Many relational database structure.
* **Advanced Admin Panel:** Enables administrators to monitor system states and view all real-time orders aggregated via optimized SQL `JOIN` operations.
* **FSM (Finite State Machine):** Safe and logical sequential workflows for user registration and tariff selection.
* **Asynchronous Execution:** High-performance, non-blocking operations powered by `aiogram` and `aiosqlite`.

---

## 🛠 Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.10+ |
| Framework | [aiogram](https://docs.aiogram.dev/) (v3.x) |
| Database | SQLite via `aiosqlite` (async transactions) |
| Deployment & Hosting | Railway Cloud Platform |
| Version Control | Git & GitHub |

---

## ⚙️ Installation & Setup

To run this project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Tleukhanov/for_erasyl.git
   cd for_erasyl
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux / macOS
   venv\Scripts\activate       # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables.** Create a `.env` file in the root directory:
   ```env
   BOT_TOKEN=your_bot_token_from_BotFather
   ```

5. **Run the bot:**
   ```bash
   python bot.py
   ```

---

## ☁️ Deployment

The project is configured to run on **Railway**. Simply connect the repository, set the required environment variables, and Railway will automatically build and redeploy the bot on every push to the main branch.

---

## 📁 Project Structure

```
├── bot.py              # Entry point
├── handlers/           # Message and command handlers
├── database/           # SQLite logic (aiosqlite, models, queries)
├── requirements.txt    # Project dependencies
└── .env                # Environment variables (not committed)
```

---

## 👤 Author

* **Developer:** Tleukhanov Yeraly
* **Role:** Backend Developer
* **Focus:** Crafting robust server-side logic, asynchronous Python systems, database normalization, and automated workflows.
* **GitHub:** [@Tleukhanov](https://github.com/Tleukhanov)

---
<div align="center">Made with ❤️ and Python</div>