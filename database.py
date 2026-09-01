import sqlite3

def add_application(conn, company, role, date_applied, status, link=None, notes=None):
    conn.execute(
        "INSERT INTO applications (company, role, date_applied, status, link, notes) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (company, role, date_applied, status, link, notes),
    )
    conn.commit()

def get_all(conn):
    cursor = conn.execute("SELECT * FROM applications ORDER BY date_applied DESC")
    return cursor.fetchall()


def init_db(path="applications.db"):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            date_applied TEXT NOT NULL,
            status TEXT NOT NULL,
            link TEXT,
            notes TEXT
        )
    """)
    conn.commit()
    return conn