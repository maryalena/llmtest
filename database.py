ب"""
Database module for the Telegram Task Manager Bot.
Handles all SQLite database operations using OOP principles.
"""

import sqlite3
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from contextlib import contextmanager

from config import DATABASE_NAME, LOCAL_TIMEZONE, logger, get_today_shamsi, shamsi_to_gregorian

# -----------------------------------------------------------------------------
# Database Manager Class
# -----------------------------------------------------------------------------
class DatabaseManager:
    """
    Manages all database operations for the task management system.
    Uses context managers for safe connection handling.
    """

    def __init__(self, db_name: str = DATABASE_NAME):
        """
        Initialize the DatabaseManager.

        Args:
            db_name: Name of the SQLite database file.
        """
        self.db_name = db_name
        self._init_database()

    @contextmanager
    def _get_connection(self):
        """
        Context manager for database connections.
        Yields a connection object and ensures proper cleanup.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            # Enable dictionary-like row access
            conn.row_factory = sqlite3.Row
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def _init_database(self) -> None:
        """
        Initialize the database with required tables.
        Creates tables if they don't exist.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Tasks table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date TEXT NOT NULL,
                    due_time TEXT NOT NULL,
                    reminder_minutes INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'pending',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            # Users table for tracking
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            conn.commit()
            logger.info("Database initialized successfully.")

    # -------------------------------------------------------------------------
    # User Operations
    # -------------------------------------------------------------------------
    def add_or_update_user(self, user_id: int, username: str = None,
                          first_name: str = None, last_name: str = None) -> None:
        """
        Add a new user or update existing user information.

        Args:
            user_id: Telegram user ID.
            username: Telegram username.
            first_name: User's first name.
            last_name: User's last name.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (user_id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    username = excluded.username,
                    first_name = excluded.first_name,
                    last_name = excluded.last_name
                """,
                (user_id, username, first_name, last_name),
            )
            conn.commit()

    # -------------------------------------------------------------------------
    # Task Operations
    # -------------------------------------------------------------------------
    def add_task(
        self,
        user_id: int,
        title: str,
        description: str,
        due_date: str,
        due_time: str,
        reminder_minutes: int = 0,
    ) -> int:
        """
        Add a new task to the database.

        Args:
            user_id: Telegram user ID.
            title: Task title.
            description: Task description.
            due_date: Due date in YYYY-MM-DD format.
            due_time: Due time in HH:MM format.
            reminder_minutes: Minutes before due date to send reminder.

        Returns:
            ID of the newly created task.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO tasks (user_id, title, description, due_date, due_time, reminder_minutes)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_id, title, description, due_date, due_time, reminder_minutes),
            )
            conn.commit()
            task_id = cursor.lastrowid
            logger.info(f"Task added: ID={task_id}, User={user_id}, Title={title}")
            return task_id

    def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a single task by ID.

        Args:
            task_id: Task ID.

        Returns:
            Dictionary containing task data or None if not found.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM tasks WHERE id = ?",
                (task_id,),
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_user_tasks(
        self,
        user_id: int,
        status: str = None,
        date: str = None,
    ) -> List[Dict[str, Any]]:
        """
        Get tasks for a specific user with optional filtering.

        Args:
            user_id: Telegram user ID.
            status: Filter by status ('pending', 'completed').
            date: Filter by specific date (YYYY-MM-DD).

        Returns:
            List of task dictionaries.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM tasks WHERE user_id = ?"
            params = [user_id]

            if status:
                query += " AND status = ?"
                params.append(status)

            if date:
                query += " AND due_date = ?"
                params.append(date)

            query += " ORDER BY due_date, due_time"

            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_all_user_tasks(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Get all tasks for a user.

        Args:
            user_id: Telegram user ID.

        Returns:
            List of all task dictionaries.
        """
        return self.get_user_tasks(user_id)

    def get_today_tasks(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Get tasks due today for a user.

        Args:
            user_id: Telegram user ID.

        Returns:
            List of task dictionaries due today.
        """
        today = get_today_shamsi()
        return self.get_user_tasks(user_id, date=today)

    def get_overdue_tasks(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Get overdue tasks for a user.

        Args:
            user_id: Telegram user ID.

        Returns:
            List of overdue task dictionaries.
        """
        today = get_today_shamsi()
        now_time = datetime.now().strftime("%H:%M")

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM tasks
                WHERE user_id = ?
                AND status = 'pending'
                AND (
                    due_date < ?
                    OR (due_date = ? AND due_time < ?)
                )
                ORDER BY due_date, due_time
                """,
                (user_id, today, today, now_time),
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def update_task(self, task_id: int, **kwargs) -> bool:
        """
        Update task fields.

        Args:
            task_id: Task ID to update.
            **kwargs: Fields to update.

        Returns:
            True if updated successfully, False otherwise.
        """
        allowed_fields = {
            "title",
            "description",
            "due_date",
            "due_time",
            "reminder_minutes",
            "status",
        }

        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not updates:
            return False

        set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
        values = list(updates.values()) + [task_id]

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE tasks SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                values,
            )
            conn.commit()
            logger.info(f"Task updated: ID={task_id}")
            return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task.

        Args:
            task_id: Task ID to delete.

        Returns:
            True if deleted successfully, False otherwise.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            logger.info(f"Task deleted: ID={task_id}")
            return cursor.rowcount > 0

    def mark_task_completed(self, task_id: int) -> bool:
        """
        Mark a task as completed.

        Args:
            task_id: Task ID to mark as completed.

        Returns:
            True if updated successfully, False otherwise.
        """
        return self.update_task(task_id, status="completed")

    def get_pending_tasks_with_reminders(self) -> List[Dict[str, Any]]:
        """
        Get all pending tasks that have reminders set.

        Returns:
            List of task dictionaries with reminders.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM tasks
                WHERE status = 'pending'
                AND reminder_minutes > 0
                """
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Get all registered users.

        Returns:
            List of user dictionaries.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]


# -----------------------------------------------------------------------------
# Singleton Instance
# -----------------------------------------------------------------------------
db = DatabaseManager()