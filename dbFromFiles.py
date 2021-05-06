import sqlite3 as sq
import glob

con = sq.connect('filesDB.db')

if __name__ == "__main__":
	print("Hello")
	dir = input("Please enter the path you would like to make add to DB: ")
	globDir = glob.glob(dir)
	if len(globDir) != 1:
		print("Directory not found")
		quit()
	else:
		print(f"Found {globDir}")
	print("Checking for files in directory...")
	dir = globDir[0]
	dir = dir + "/*"
	globDir = glob.glob(dir)
	imageFiles = []
	print("Found these files:")
	for filePath in globDir:
		#print(f"-path: {filePath}")
		#print(filePath.endswith(".jpg") or filePath.endswith(".png") or filePath.endswith(".gif") or filePath.endswith(".bmp"))
		if (filePath.endswith(".jpg") or filePath.endswith(".png")		or filePath.endswith(".gif") or filePath.endswith(".bmp")):
			filePath = filePath.replace("\\","/")
			imageFiles.append(filePath)
	print("All valid files are: ")
	for filePath in imageFiles:
		print(filePath)
	choice = input("Re-initialize tables? (y/n)")
	if choice.upper() == "Y":
		with con:
			con.execute("DROP TABLE IF EXISTS files")
			con.execute("""
			CREATE TABLE IF NOT EXISTS files (
			id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			address TEXT,
			tags TEXT
			);
			""")
	choice = input("Add found files to table? (y/n)")
	if choice.upper() == "Y":
		currTable = []
		with con:
			currTable = con.execute("SELECT * FROM files")
		fileNames = []
		for entry in currTable:
			fileNames.append(entry[1])
		#print(fileNames)
		first = True
		print("Inserting...")
		for filePath in imageFiles:
			if filePath not in fileNames:
				if first:
					sql = 'INSERT INTO files (address, tags) VALUES(?, ?)'
					data = [filePath, "_"]
					first = False
				else:
					sql += ',(?, ?)'
					data.append(filePath)
					data.append("_")
		with con:
			con.execute(sql, data)
	choice = input("Print db? (y/n)")
	if choice.upper() == "Y":
		with con:
			data = con.execute("SELECT * FROM files")
			for row in data:
				print(row)
