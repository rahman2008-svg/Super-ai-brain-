import sqlite3

DB_PATH = "super_ai.db"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# knowledge table তৈরি
c.execute('''
CREATE TABLE IF NOT EXISTS knowledge (
    question TEXT PRIMARY KEY,
    answer TEXT
)
''')

conn.commit()
conn.close()
print("Database created and table ready!")
