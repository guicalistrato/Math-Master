# Chat GPT helped to move questions it created w/ my supervision to project.db
import sqlite3
import csv

# Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('project.db')
cursor = conn.cursor()

# Create the questions table (if it doesn't exist)
cursor.execute('''
CREATE TABLE IF NOT EXISTS questions (
    number INTEGER PRIMARY KEY,
    subject TEXT,
    question TEXT,
    a TEXT,
    b TEXT,
    c TEXT,
    d TEXT,
    answer TEXT,
    difficulty TEXT
)
''')

# Read the CSV file and insert its data into the database
with open('questions.csv', 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        cursor.execute('''
        INSERT INTO questions (number, subject, question, a, b, c, d, answer, difficulty)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row['number'], row['subject'], row['question'], row['a'], row['b'], row['c'], row['d'], row['answer'], row['difficulty']))

# Commit the changes and close the connection
conn.commit()
conn.close()
