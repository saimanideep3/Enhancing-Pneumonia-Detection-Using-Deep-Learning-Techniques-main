import sqlite3

# Connect to SQLite database (or create if it doesn't exist)
conn = sqlite3.connect('predictions.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table to store predictions
cursor.execute('''
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    sex TEXT,
    place TEXT,
    filename TEXT,
    prediction TEXT,
    probability REAL
)
''')

# Commit and close connection
conn.commit()
conn.close()

print("Database and table created successfully!")
