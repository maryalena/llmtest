"""
Configuration module for the Telegram Task Manager Bot.
Contains all constants, settings, and configuration variables.
"""

import os
import logging
from datetime import datetime, timedelta
import pytz
import jdatetime

# -----------------------------------------------------------------------------
# Logging Configuration
# -----------------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Bot Configuration
# -----------------------------------------------------------------------------
# ⭐ محل وارد کردن توکن ربات ⭐
# روش اول (توصیه شده): استفاده از متغیر محیطی
#   در ترمینال اجرا کنید:
#   export TASK_BOT_TOKEN="توکن_شما"
#
# روش دوم: توکن را مستقیم در اینجا قرار دهید (خط زیر را تغییر دهید):
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8896833712:AAHdltzdXynCftKPa83t4k9KdJMAdj1G5xU")

# -----------------------------------------------------------------------------
# Database Configuration
# -----------------------------------------------------------------------------
DATABASE_NAME = "tasks.db"

# -----------------------------------------------------------------------------
# Timezone Configuration
# -----------------------------------------------------------------------------
# Using local timezone (can be adjusted as needed)
LOCAL_TIMEZONE = "Asia/Tehran"  # Persian timezone default

# -----------------------------------------------------------------------------
# Reminder Options (in minutes before due date)
# -----------------------------------------------------------------------------
REMINDER_OPTIONS = {
    "5_minutes": 5,
    "15_minutes": 15,
    "1_hour": 60,
    "1_day": 1440,  # 24 hours
}

# -----------------------------------------------------------------------------
# Daily Summary Time
# -----------------------------------------------------------------------------
DAILY_SUMMARY_HOUR = 8
DAILY_SUMMARY_MINUTE = 0

# -----------------------------------------------------------------------------
# Conversation States
# -----------------------------------------------------------------------------
(
    TASK_TITLE,
    TASK_DESCRIPTION,
    TASK_DUE_DATE,
    TASK_DUE_TIME,
    TASK_REMINDER,
) = range(5)

# Edit conversation states
(
    EDIT_SELECT_TASK,
    EDIT_SELECT_FIELD,
    EDIT_TITLE,
    EDIT_DESCRIPTION,
    EDIT_DUE_DATE,
    EDIT_DUE_TIME,
    EDIT_REMINDER,
) = range(5, 12)

# -----------------------------------------------------------------------------
# Persian Messages (RTL Friendly)
# -----------------------------------------------------------------------------
MESSAGES = {
    "welcome": (
        "👋 خوش آمدید!\n\n"
        "🤖 من ربات مدیریت وظایف روزانه شما هستم.\n"
        "✅ با من می‌توانید وظایف خود را مدیریت کنید.\n\n"
        "📋 دستورات موجود:\n"
        "➕ /addtask - افزودن وظیفه جدید\n"
        "📋 /tasks - مشاهده لیست وظایف\n"
        "🗑 /deletetask - حذف وظیفه\n"
        "📅 /today - وظایف امروز\n"
        "⚠️ /overdue - وظایف عقب‌افتاده\n"
        "✏️ /edittask - ویرایش وظیفه\n"
        "✅ /complete - تکمیل وظیفه\n"
        "📊 /summary - خلاصه روزانه\n"
        "📤 /export - خروجی اکسل\n"
        "📥 /import - ورودی اکسل\n"
        "❓ /help - راهنما"
    ),
    "help": (
        "📋 راهنمای ربات مدیریت وظایف:\n\n"
        "➕ /addtask - افزودن وظیفه جدید\n"
        "📋 /tasks - مشاهده تمام وظایف\n"
        "🗑 /deletetask - حذف یک وظیفه\n"
        "📅 /today - وظایف امروز\n"
        "⚠️ /overdue - وظایف عقب‌افتاده\n"
        "✏️ /edittask - ویرایش وظیفه\n"
        "✅ /complete - تکمیل وظیفه\n"
        "📊 /summary - خلاصه روزانه\n"
        "📤 /export - خروجی اکسل\n"
        "📥 /import - ورودی اکسل\n"
        "❓ /help - نمایش این راهنما\n\n"
        "💡 نکته: برای هر وظیفه می‌توانید یادآوری تنظیم کنید."
    ),
    "enter_title": "📝 لطفاً عنوان وظیفه را وارد کنید:",
    "enter_description": "📄 لطفاً توضیحات وظیفه را وارد کنید:",
    "enter_due_date": (
        "📅 لطفاً تاریخ انجام را وارد کنید (فرمت: YYYY-MM-DD):\n"
        "مثال: 2024-12-25"
    ),
    "enter_due_time": (
        "⏰ لطفاً زمان انجام را وارد کنید (فرمت: HH:MM):\n"
        "مثال: 14:30"
    ),
    "select_reminder": (
        "🔔 لطفاً زمان یادآوری را انتخاب کنید:\n\n"
        "⏱ 5 دقیقه قبل\n"
        "⏱ 15 دقیقه قبل\n"
        "⏱ 1 ساعت قبل\n"
        "⏱ 1 روز قبل"
    ),
    "task_added": "✅ وظیفه با موفقیت اضافه شد!",
    "invalid_date": "❌ تاریخ نامعتبر است. لطفاً دوباره تلاش کنید (YYYY-MM-DD):",
    "invalid_time": "❌ زمان نامعتبر است. لطفاً دوباره تلاش کنید (HH:MM):",
    "no_tasks": "📭 شما هیچ وظیفه‌ای ندارید.",
    "task_deleted": "🗑 وظیفه حذف شد.",
    "task_completed": "✅ وظیفه تکمیل شد!",
    "select_task_to_delete": "🗑 لطفاً وظیفه‌ای را برای حذف انتخاب کنید:",
    "select_task_to_edit": "✏️ لطفاً وظیفه‌ای را برای ویرایش انتخاب کنید:",
    "select_task_to_complete": "✅ لطفاً وظیفه‌ای را برای تکمیل انتخاب کنید:",
    "select_field_to_edit": (
        "📝 کدام فیلد را می‌خواهید ویرایش کنید؟\n"
        "1. عنوان\n"
        "2. توضیحات\n"
        "3. تاریخ\n"
        "4. زمان\n"
        "5. یادآوری"
    ),
    "enter_new_value": "✏️ لطفاً مقدار جدید را وارد کنید:",
    "task_updated": "✅ وظیفه به‌روزرسانی شد!",
    "no_overdue_tasks": "🎉 شما هیچ وظیفه عقب‌افتاده‌ای ندارید!",
    "daily_summary_title": "📊 خلاصه روزانه",
    "reminder_message": (
        "🔔 یادآوری وظیفه!\n\n"
        "📌 عنوان: {title}\n"
        "📝 توضیحات: {description}\n"
        "📅 تاریخ: {due_date}\n"
        "⏰ زمان: {due_time}"
    ),
    "export_success": "📤 فایل اکسل با موفقیت صادر شد.",
    "import_success": "📥 وظایف از فایل اکسل وارد شدند.",
    "import_error": "❌ خطا در وارد کردن فایل. لطفاً فایل معتبر اکسل آپلود کنید.",
    "cancelled": "❌ عملیات لغو شد.",
    "main_menu": (
        "🏠 <b>منوی اصلی</b>\n\n"
        "از دکمه‌های زیر برای مدیریت وظایف خود استفاده کنید:\n"
    ),
}

# -----------------------------------------------------------------------------
# Emoji Status Mapping
# -----------------------------------------------------------------------------
STATUS_EMOJIS = {
    "pending": "⏳",
    "completed": "✅",
    "overdue": "⚠️",
}

# -----------------------------------------------------------------------------
# Time Helper Functions
# -----------------------------------------------------------------------------
def get_iran_time() -> datetime:
    """Get current time in Iran timezone (Asia/Tehran)."""
    return datetime.now(pytz.timezone("Asia/Tehran"))


def format_iran_time(dt: datetime = None) -> str:
    """Format datetime to Persian string in Iran timezone using Persian (Jalali) calendar."""
    if dt is None:
        dt = get_iran_time()
    elif dt.tzinfo is None:
        dt = pytz.timezone("Asia/Tehran").localize(dt)
    else:
        dt = dt.astimezone(pytz.timezone("Asia/Tehran"))
    
    # Convert to Persian (Jalali) calendar
    jdt = jdatetime.datetime.fromgregorian(datetime=dt)
    
    # Persian day names
    days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]
    day_name = days[jdt.weekday()]
    
    # Persian month names
    months = [
        "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
        "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
    ]
    month_name = months[jdt.month - 1]
    
    return f"{day_name} {jdt.day} {month_name} {jdt.year} - {jdt.strftime('%H:%M')}"


def get_iran_time_short() -> str:
    """Get short formatted Iran time."""
    dt = get_iran_time()
    return dt.strftime("%Y-%m-%d %H:%M")


# -----------------------------------------------------------------------------
# Persian (Jalali) Date Conversion Helpers
# -----------------------------------------------------------------------------
def gregorian_to_shamsi(gregorian_date: str) -> str:
    """
    Convert Gregorian date (YYYY-MM-DD) to Shamsi date (YYYY-MM-DD).
    
    Args:
        gregorian_date: Date in Gregorian format (YYYY-MM-DD).
        
    Returns:
        Date in Shamsi format (YYYY-MM-DD).
    """
    try:
        year, month, day = map(int, gregorian_date.split("-"))
        g_date = datetime(year, month, day)
        j_date = jdatetime.date.fromgregorian(date=g_date)
        return f"{j_date.year:04d}-{j_date.month:02d}-{j_date.day:02d}"
    except (ValueError, AttributeError):
        return gregorian_date


def shamsi_to_gregorian(shamsi_date: str) -> str:
    """
    Convert Shamsi date (YYYY-MM-DD) to Gregorian date (YYYY-MM-DD).
    
    Args:
        shamsi_date: Date in Shamsi format (YYYY-MM-DD).
        
    Returns:
        Date in Gregorian format (YYYY-MM-DD).
    """
    try:
        year, month, day = map(int, shamsi_date.split("-"))
        j_date = jdatetime.date(year, month, day)
        g_date = j_date.togregorian()
        return f"{g_date.year:04d}-{g_date.month:02d}-{g_date.day:02d}"
    except (ValueError, AttributeError):
        return shamsi_date


def get_today_shamsi() -> str:
    """Get today's date in Shamsi format (YYYY-MM-DD)."""
    jdt = jdatetime.date.today()
    return f"{jdt.year:04d}-{jdt.month:02d}-{jdt.day:02d}"


def format_shamsi_date(shamsi_date: str) -> str:
    """
    Format Shamsi date to Persian string.
    
    Args:
        shamsi_date: Date in Shamsi format (YYYY-MM-DD).
        
    Returns:
        Formatted Persian date string.
    """
    try:
        year, month, day = map(int, shamsi_date.split("-"))
        jdt = jdatetime.date(year, month, day)
        
        days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]
        months = [
            "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
            "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
        ]
        
        day_name = days[jdt.weekday()]
        month_name = months[jdt.month - 1]
        
        return f"{day_name} {jdt.day} {month_name} {jdt.year}"
    except (ValueError, AttributeError):
        return shamsi_date


# -----------------------------------------------------------------------------
# Keyboard Options
# -----------------------------------------------------------------------------
REMINDER_KEYBOARD = [
    ["5 دقیقه قبل", "15 دقیقه قبل"],
    ["1 ساعت قبل", "1 روز قبل"],
]

EDIT_FIELD_KEYBOARD = [
    ["عنوان", "توضیحات"],
    ["تاریخ", "زمان", "یادآوری"],
]
