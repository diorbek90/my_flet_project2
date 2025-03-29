CREATE_TABLE_TASKS = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        create_time TEXT NOT NULL,
        completed INTEGER DEFAULT 0
    )
"""

SELECT_TASKS = "SELECT id, task, create_time FROM tasks"
INSERT_TASK = "INSERT INTO tasks (task, create_time) VALUES (?, ?)"
UPDATE_TASK = "UPDATE tasks SET task = ?, create_time = ? WHERE id = ?"
DELETE_TASK = "DELETE FROM tasks WHERE id = ?"


SELECT_completed = 'SELECT id, task, completed FROM tasks WHERE completed = 1'
SELECT_incomplete = 'SELECT id, task, completed FROM tasks WHERE completed = 0'