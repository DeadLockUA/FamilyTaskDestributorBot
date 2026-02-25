import sqlite3

def get_connection():
    conn = sqlite3.connect("family_tasks.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()


#User should contain:
#Unique id
#Telegram id
#Name
#Role
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        name TEXT,
        role TEXT
    )
    """)


#Task should contain:
#unique id
#Title - text
#OwnerID - int
#CreatorID - int
#Deadline - text
#Status - int
#Priority -int

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        owner_id INTEGER,
        creator_id INTEGER,
        deadline TEXT,
        status INTEGER,
        priority INTEGER
    )
    """)

    conn.commit()
    conn.close()



def add_user(telegram_id, name, role):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (telegram_id, name, role)
    VALUES (?, ?, ?)
    """, (telegram_id, name, role))

    conn.commit()
    conn.close()

def get_user_by_telegram_id(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users WHERE telegram_id = ?
    """, (telegram_id,))

    user = cursor.fetchone()
    conn.close()

    return user

def get_all_users():        #For debuging and admin purposes
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()
    return users




def add_task(title, owner_id, creator_id, deadline, priority):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tasks (title, owner_id, creator_id, deadline, status, priority)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (title, owner_id, creator_id, deadline, 0 , priority))

    conn.commit()
    conn.close()

def update_task_status(task_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE tasks
    SET status = ?
    WHERE id = ?
    """, (new_status, task_id))

    conn.commit()
    conn.close()


def get_tasks_by_user_id(owner_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM tasks WHERE owner_id = ?
    """, (owner_id,))

    tasks = cursor.fetchall()
    conn.close()

    return tasks