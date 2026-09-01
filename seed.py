from database import init_db, add_application

conn = init_db()
add_application(conn, "Example Company", "Software Engineer", "2026-09-01", "Applied", None, None)
conn.close()