import sqlite3

conn = sqlite3.connect("attendance.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    timestamp TEXT NOT NULL
)
""")
conn.commit()
conn.close()
print("✅ Database initialized: attendance.db")
