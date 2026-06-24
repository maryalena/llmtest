"""
Scheduler module for the Telegram Task Manager Bot.
Handles all APScheduler operations for reminders and daily summaries.
"""

import logging
from datetime import datetime, timedelta
from typing import Callable, Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger

from config import (
    LOCAL_TIMEZONE,
    DAILY_SUMMARY_HOUR,
    DAILY_SUMMARY_MINUTE,
    REMINDER_OPTIONS,
    MESSAGES,
    logger,
    format_shamsi_date,
)
from database import db

# -----------------------------------------------------------------------------
# Scheduler Manager Class
# -----------------------------------------------------------------------------
class SchedulerManager:
    """
    Manages all scheduled jobs for the task management system.
    Handles reminders and daily summary notifications.
    """

    def __init__(self):
        """
        Initialize the SchedulerManager with a BackgroundScheduler.
        """
        self.scheduler = BackgroundScheduler(timezone=LOCAL_TIMEZONE)
        self.scheduler.start()
        logger.info("Scheduler initialized and started.")

    def schedule_reminder(
        self,
        task_id: int,
        user_id: int,
        due_date: str,
        due_time: str,
        reminder_minutes: int,
        callback: Callable,
    ) -> None:
        """
        Schedule a reminder for a task.

        Args:
            task_id: ID of the task.
            user_id: Telegram user ID.
            due_date: Due date in YYYY-MM-DD format.
            due_time: Due time in HH:MM format.
            reminder_minutes: Minutes before due date to send reminder.
            callback: Function to call when reminder triggers.
        """
        try:
            # Calculate reminder time
            due_datetime = datetime.strptime(
                f"{due_date} {due_time}", "%Y-%m-%d %H:%M"
            )
            reminder_datetime = due_datetime - timedelta(minutes=reminder_minutes)

            # Don't schedule if reminder time has already passed
            if reminder_datetime < datetime.now():
                logger.warning(
                    f"Reminder time already passed for task {task_id}. Skipping."
                )
                return

            # Create unique job ID
            job_id = f"reminder_{task_id}_{user_id}"

            # Remove existing job if it exists
            self.remove_job(job_id)

            # Schedule the reminder
            self.scheduler.add_job(
                callback,
                trigger=DateTrigger(run_date=reminder_datetime),
                id=job_id,
                args=[task_id, user_id],
                replace_existing=True,
            )

        except Exception as e:
            logger.error(f"Error scheduling reminder for task {task_id}: {e}")

        logger.info(
            f"⏰ یادآوری برای وظیفه {task_id} در تاریخ {format_shamsi_date(reminder_datetime.strftime('%Y-%m-%d'))} - {reminder_datetime.strftime('%H:%M')}"
        )

    def remove_job(self, job_id: str) -> None:
        """
        Remove a scheduled job by ID.

        Args:
            job_id: ID of the job to remove.
        """
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"Job {job_id} removed.")
        except Exception:
            # Job doesn't exist, which is fine
            pass

    def remove_task_reminder(self, task_id: int, user_id: int) -> None:
        """
        Remove a task reminder.

        Args:
            task_id: ID of the task.
            user_id: Telegram user ID.
        """
        job_id = f"reminder_{task_id}_{user_id}"
        self.remove_job(job_id)

    def schedule_daily_summary(
        self,
        callback: Callable,
        hour: int = DAILY_SUMMARY_HOUR,
        minute: int = DAILY_SUMMARY_MINUTE,
    ) -> None:
        """
        Schedule task for daily summary notifications.

        Args:
            callback: Function to call for daily summary.
            hour: Hour to send summary (0-23).
            minute: Minute to send summary (0-59).
        """
        try:
            job_id = "daily_summary"

            # Remove existing daily summary job
            self.remove_job(job_id)

            # Schedule daily summary
            self.scheduler.add_job(
                callback,
                trigger=CronTrigger(hour=hour, minute=minute),
                id=job_id,
                replace_existing=True,
            )

            logger.info(f"Daily summary scheduled for {hour:02d}:{minute:02d}")

        except Exception as e:
            logger.error(f"Error scheduling daily summary: {e}")

    def shutdown(self) -> None:
        """
        Shutdown the scheduler gracefully.
        """
        self.scheduler.shutdown()
        logger.info("Scheduler shut down.")


# -----------------------------------------------------------------------------
# Singleton Instance
# -----------------------------------------------------------------------------
scheduler = SchedulerManager()