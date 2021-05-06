import sqlite3 as sq

con = sq.connect('test.db')

with con:
	con.execute("""
		CREATE TABLE IF NOT EXISTS user (
			id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			name TEXT,
			age INTEGER
		);
	""")
	
sql = 'INSERT INTO USER (id, name, age) values(?, ?, ?)'
data = [
	(1, 'Alice', 21),
	(2, 'Bob', 22),
	(3, 'Chris', 23)
]

with con:
	con.executemany(sql, data)
	
with con:
	data = con.execute("SELECT * FROM USER WHERE age <= 22")
	for row in data:
		print(row)

print(sq.version)