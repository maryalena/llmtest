# 🤖 Telegram Task Manager Bot

A powerful Telegram bot for managing daily tasks.

## 📋 Features

- ➕ Add new task via conversation dialog (ConversationHandler)
- 📋 View all tasks list
- 🗑 Delete a task
- ✏️ Edit existing tasks
- ✅ Mark tasks as completed
- 📅 View today's tasks
- ⚠️ View overdue tasks
- 🔔 Automatic reminders (5 min, 15 min, 1 hour, 1 day before)
- 📊 Daily summary (at 08:00 every day)
- 📤 Export to Excel file (.xlsx)
- 📥 Import from Excel file
- 👥 Multi-user support (independent per user)
- 🎨 Persian UI with emoji support
- 🗄 SQLite storage

## 🛠 Prerequisites

- Python 3.13+
- pip (Python package manager)
- A Telegram bot (get one from [@BotFather](https://t.me/BotFather))

## 📦 Installation

### 1. Get a Bot Token

1. Go to [@BotFather](https://t.me/BotFather) on Telegram.
2. Send the `/newbot` command.
3. Choose a name and username for your bot.
4. Save the received token.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variable

#### Linux / macOS:
```bash
export TASK_BOT_TOKEN="your_bot_token_here"
```

#### Windows (Command Prompt):
```cmd
set TASK_BOT_TOKEN=your_bot_token_here
```

#### Windows (PowerShell):
```powershell
$env:TASK_BOT_TOKEN="your_bot_token_here"
```

> **Note:** If the environment variable is not set, the bot will fail to start. You can also set your token in `config.py` (for development only).

### 4. Run the Bot

```bash
python bot.py
```

## 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Start using the bot and register |
| `/addtask` | Add a new task |
| `/tasks` | View all tasks |
| `/deletetask` | Delete a task |
| `/edittask` | Edit a task |
| `/complete` | Mark a task as completed |
| `/today` | View today's tasks |
| `/overdue` | View overdue tasks |
| `/summary` | View task statistics summary |
| `/export` | Export tasks to Excel |
| `/import` | Import tasks from Excel file |
| `/help` | Command help |
| `/cancel` | Cancel current operation |

## 📁 Project Structure

```
├── bot.py              # Main bot code and conversation handling
├── config.py           # Configuration and constants
├── database.py         # Database and SQLite operations
├── scheduler.py        # Reminder scheduling with APScheduler
├── schema.sql          # Database schema
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## 🗄 Database Schema

### `tasks` Table
| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Unique task ID |
| user_id | INTEGER | Telegram user ID |
| title | TEXT | Task title |
| description | TEXT | Task description |
| due_date | TEXT | Due date (YYYY-MM-DD) |
| due_time | TEXT | Due time (HH:MM) |
| reminder_minutes | INTEGER | Minutes before reminder |
| status | TEXT | Status (pending/completed) |
| created_at | TEXT | Creation timestamp |
| updated_at | TEXT | Last update timestamp |

### `users` Table
| Field | Type | Description |
|-------|------|-------------|
| user_id | INTEGER | Telegram user ID |
| username | TEXT | Telegram username |
| first_name | TEXT | First name |
| last_name | TEXT | Last name |
| created_at | TEXT | Registration timestamp |

## 🔧 Configuration

Edit `config.py` to change settings:

- **LOCAL_TIMEZONE**: Timezone (default: Asia/Tehran)
- **DAILY_SUMMARY_HOUR / DAILY_SUMMARY_MINUTE**: Daily summary time
- **REMINDER_OPTIONS**: Reminder time options
- **DATABASE_NAME**: Database file name

## 🐛 Troubleshooting

### Issue: Bot won't start
- Make sure you have set the bot token correctly.
- Install required libraries: `pip install -r requirements.txt`

### Issue: Reminders not working
- Make sure your system time is set correctly.
- The bot must be running to send reminders.

### Issue: Excel export/import errors
- Install the openpyxl library: `pip install openpyxl`

## 📝 Important Notes

- The bot must be running continuously for reminders to be sent.
- You can use free hosting services like Railway.app or Render.com to host the bot.
- All messages are displayed in Persian with RTL support.

## 📄 License

This project is licensed under the MIT License.