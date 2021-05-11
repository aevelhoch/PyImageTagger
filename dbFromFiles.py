import sqlite3 as sq
import glob

con = sq.connect('filesDB.db')

if __name__ == "__main__":
	print("Hello")
	dir = input("Please enter the path you would like to make add to DB: ")
	globDir = glob.glob(dir) # get directory using glob
	if len(globDir) != 1: # returns list of len 1 w/directory if exists
		print("Directory not found")
		quit()
	else:
		print(f"Found {globDir}")
	print("Checking for files in directory...")
	# assuming the thing we found was a directory, make a glob of all items in that directory by using wildcard
	dir = globDir[0]
	print(dir[0:2])
	if (dir[0:2] != "./"):
		dir = "./" + dir
	dir = dir + "/**" 
	globDir = glob.glob(dir,recursive=True)
	imageFiles = [] # list to contain all paths to images of appropriate types
	print("Found these files:")
	for filePath in globDir:
		#print(f"-path: {filePath}")
		#print(filePath.endswith(".jpg") or filePath.endswith(".png") or filePath.endswith(".gif") or filePath.endswith(".bmp"))
		# Add files with appropriate extensions to list
		# TODO: make the appropriate image extensions dynamic
		if (filePath.endswith(".jpg") or filePath.endswith(".png")	or filePath.endswith(".gif") or filePath.endswith(".bmp")):
			filePath = filePath.replace("\\","/")
			imageFiles.append(filePath)
	# display all found images
	print("All valid files are: ")
	for filePath in imageFiles:
		print(filePath)
	# if we want to reset table for different testing, offer choice
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
		# Get the current files, so we don't add duplicates
		currTable = []
		with con:
			currTable = con.execute("SELECT * FROM files")
		fileNames = []
		for entry in currTable:
			fileNames.append(entry[1])
		#print(fileNames)
		first = True # first to make sql statement building easier
		print("Inserting...")
		sql = 'PRAGMA testing' # default options for sql, data so execute doesn't error if no new files found
		data = []
		for filePath in imageFiles: # for each image file we recognized through dir glob
			if filePath not in fileNames: # if it's not already in the db
				if first: # start building the sql statement
					sql = 'INSERT INTO files (address, tags) VALUES(?, ?)'
					data = [filePath, "_"]
					first = False
				else: # or continue if we're at the end
					sql += ',(?, ?)'
					data.append(filePath)
					data.append("_")
		with con: # and finally, execute
			con.execute(sql, data)
	choice = input("Print db? (y/n)")
	if choice.upper() == "Y":
		with con:
			data = con.execute("SELECT * FROM files")
			for row in data:
				print(row)
