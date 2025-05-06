import sqlite3

conn = sqlite3.connect('predictions.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM predictions")
data = cursor.fetchall()

conn.close()

print("Database Records:")
for row in data:
    print(row)
