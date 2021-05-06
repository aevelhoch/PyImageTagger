import sqlite3 as sq

con = sq.connect('model.db')

menu = """Choose option:
Display: P - Print all dbs
         V - Print all files with certain tag
Entries: A - Add file or tag entry to db
         D - Delete file or tag entry
Tags:    T - Tag file with tag
         R - Remove tag from file
I - Reinitialize dbs
Q - Quit"""

""" Reference for Tables:
files_____________|_tags_____|_view______________
id, address, tags | id, name | id, address, tags """

def printAll():
	with con:
		print("======------ - - -")
		print("files:")
		data = con.execute("SELECT * FROM files")
		for row in data:
			print(row)
		print("tags:")
		data = con.execute("SELECT * FROM tags")
		for row in data:
			print(row)
		print("view:")
		data = con.execute("SELECT * FROM view")
		for row in data:
			print(row)
		print("- - - ------======")

def reinitTables():
	with con:
		con.execute("DROP TABLE IF EXISTS files")
		con.execute("DROP TABLE IF EXISTS tags")
		con.execute("DROP TABLE IF EXISTS view")
		con.execute("""
		CREATE TABLE IF NOT EXISTS files (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		address TEXT,
		tags TEXT
		);
		""")
		con.execute("""
		CREATE TABLE IF NOT EXISTS tags (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		name TEXT
		);
		""")
		con.execute("""
		CREATE TABLE IF NOT EXISTS view (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		address TEXT,
		tags TEXT
		);
		""")
	print("---")

def addEntry():
	choice = input("Add to which table? (F)iles or (T)ags?\n")
	if choice.upper() == "F":
		inAddress = input("Enter address for file: ")
		sql = 'INSERT INTO files (address, tags) VALUES(?, ?)'
		data = (inAddress, "_")
	elif choice.upper() == "T":
		inName = input("Enter name of tag: ")
		sql = 'INSERT INTO tags (name) VALUES(?)'
		data = [(inName)]
	else:
		print("Invalid option.\n---")
		return
	with con:
		con.execute(sql, data)
	print("---")

def tagFile():
	# don't need to check tagID for valid as GUI will get tagID from comboBox w/no invalid choices
	fileID = input("Enter file ID to tag: ")
	tagID = input("Enter tag ID to apply: ")
	with con:
		sql = "SELECT tags FROM files WHERE id = (?) LIMIT 1"
		sqlIn = [(fileID)]
		data = con.execute(sql, sqlIn)
		for row in data:
			#print("current tags for that id = ", row[0])
			currTags = row[0]
		if ("_" + tagID + "_") not in currTags:
			currTags += tagID + "_"
			#print("will set it to ", currTags)
			sql = "UPDATE files SET tags = (?) WHERE id = (?)"
			sqlIn = (currTags, fileID)
			con.execute(sql, sqlIn)
		else:
			print(f"File {fileID} already has tag {tagID}")
	print("---")

def removeTag():
	fileID = input("Enter file ID to remove tag from: ")
	tagID = input("Enter tag ID to remove: ")
	with con:
		sql = "SELECT tags FROM files WHERE id = (?) LIMIT 1"
		sqlIn = [(fileID)]
		data = con.execute(sql, sqlIn)
		for row in data:
			currTags = row[0]
		if ("_" + tagID + "_") in currTags:
			newTags = currTags.replace("_" + tagID + "_", "_", 1)
			#print(f"Want to change tags to: {sqlIn}")
			sql = "UPDATE files SET tags = (?) WHERE id = (?)"
			sqlIn = (newTags, fileID)
			con.execute(sql, sqlIn)
		else:
			print(f"File {fileID} does not have tag {tagID}")
	print("---")
	
def deleteItem():
	choice = input("Delete from which table? (F)iles or (T)ags?\n")
	if choice.upper() == "F":
		tableName = "files"
		sql = 'DELETE FROM files WHERE id = (?)'
	elif choice.upper() == "T":
		tableName = "tags"
		sql = 'DELETE FROM tags WHERE id = (?)'
	else:
		print("Invalid option.\n---")
		return
	deleteID = input(f"Enter ID of {tableName[:-1]} to delete: ")
	data = [(deleteID)]
	with con:
		con.execute(sql, data)
	print("---")

if __name__ == "__main__":
	print("welcome")
	choice = ""
	while (choice.upper() != "Q"):
		print(menu)
		choice = input()
		if choice.upper() == "I":
			reinitTables()
		elif choice.upper() == "P":
			printAll()
		elif choice.upper() == "A":
			addEntry()
		elif choice.upper() == "T":
			tagFile()
		elif choice.upper() == "R":
			removeTag() #TODO
		elif choice.upper() == "D":
			deleteItem()