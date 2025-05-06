import sqlite3

conn = sqlite3.connect('predictions.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM predictions")
rows = cursor.fetchall()

print("Stored Predictions:")
for row in rows:
    print(row)

conn.close()
