import sqlite3

# Create a connection object and a new database file named 'example.db'
conn = sqlite3.connect('example.db')

# Create a cursor object
c = conn.cursor()

# Create a table (This will only create the table if it does not exist)
c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)')

# Insert some rows of data
c.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")
c.execute("INSERT INTO users (name, age) VALUES ('Bob', 40)")
c.execute("INSERT INTO users (name, age) VALUES ('Charlie', 50)")

# Commit the changes
conn.commit()

# Query data from the table
c.execute('SELECT * FROM users')

# Fetch all rows from the cursor
rows = c.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close the cursor and the connection
c.close()
conn.close()

