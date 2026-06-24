-- =============================================================================
-- Telegram Task Manager Bot - Database Schema
-- =============================================================================
-- This file contains the SQL schema for the task management bot.
-- The database is automatically created by database.py when the bot starts,
-- but this file can be used for manual setup or reference.
-- =============================================================================

-- ---------------------------------------------------------------------------
-- Tasks Table
-- ---------------------------------------------------------------------------
-- Stores all task information for users.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tasks (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    title           TEXT NOT NULL,
    description     TEXT,
    due_date        TEXT NOT NULL,          -- Format: YYYY-MM-DD
    due_time        TEXT NOT NULL,          -- Format: HH:MM
    reminder_minutes INTEGER DEFAULT 0,     -- Minutes before due time for reminder
    status          TEXT DEFAULT 'pending',  -- 'pending' or 'completed'
    created_at      TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at      TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------------
-- Users Table
-- ---------------------------------------------------------------------------
-- Stores registered Telegram users.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id     INTEGER PRIMARY KEY,
    username    TEXT,
    first_name  TEXT,
    last_name   TEXT,
    created_at  TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------------
-- Indexes for better performance
-- ---------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);
CREATE INDEX IF NOT EXISTS idx_tasks_user_status ON tasks(user_id, status);