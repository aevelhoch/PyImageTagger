import sqlite3 as sq
import glob
import sys

if len(sys.argv[:]) == 2:
    print(f"Attempting to load db:\'{sys.argv[1]}\'")
    con = sq.connect(sys.argv[1])
else:
    print("No arguments supplied, loading \'model.db\'")
    con = sq.connect('model.db')

menu = """Choose option: (In any function, enter x to cancel)
Display: P - Print all dbs
         V - Print all files with certain tag
Folders: F - Add all image files in folder to files db
Entries: A - Add file or tag entry to db
         D - Delete file or tag entry
Tags:    T - Tag file with tag
         R - Remove tag from file
         M - Tag multiple files with tag
Z - Test helper functions
I - Reinitialize dbs
Q - Quit"""

helperMenu = """======
C - checkDuplicate (see if filepath/tag is already in table)
======"""

""" Reference for Tables:
files_____________|_tags_____|_view______________
id, address, tags | id, name | id, address, tags """

# HELPER
# Helper function to check if a given object is already in the table
def checkDuplicate(name, type):
    dupeFound = False
    if type == "files" or type == "tags":
        getAll = f"SELECT * FROM {type}"
        data = con.execute(getAll)
        for row in data:
            if name == row[1]:
                #print("duplicate found!")
                dupeFound = True
    return dupeFound

# MENU OPTION
# Helper function to print current status of all databases
def printAll():
    x = input("(P)retty print or (D)ump out all DB info: ")
    if x.upper() == "D":
        with con:
            print("======------ - - -")
            print("files:")
            data = con.execute("SELECT * FROM files") # get all from files
            for row in data: # for each row
                print(row) # print it
            print("tags:")
            data = con.execute("SELECT * FROM tags")
            for row in data:
                print(row)
            print("view:")
            data = con.execute("SELECT * FROM view")
            for row in data:
                print(row)
            print("- - - ------======")
    elif x.upper() == "P":
        with con:
            # data = con.execute("SELECT * FROM files")
            data = con.execute("SELECT * FROM tags")
            tagsList = []
            for row in data:
                tagsList.append(row)
            data = con.execute("SELECT * FROM files")
            for row in data:
                entryTags = ""
                firstTag = True
                for tag in tagsList:
                    if ("_" + str(tag[0]) + "_" in row[2]):
                        if not firstTag: entryTags += ", "
                        entryTags += tag[1]
                        firstTag = False
                print(f"ID: {row[0]}, Path: {row[1]}, Tags: {entryTags}")
    else:
        print("Invalid choice")

# MENU OPTION
# Destroy and recreate all existing tables as empty tables- in case you goof up test db too much
def reinitTables():
    with con:
        con.execute("DROP TABLE IF EXISTS files") # drop all three tables
        con.execute("DROP TABLE IF EXISTS tags")
        con.execute("DROP TABLE IF EXISTS view")
        # create all three tables anew
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

# MENU OPTION
# Add an individual file or tag to corresponding table
def addEntry():
    choice = input("Add to which table? (F)iles or (T)ags?\n")
    if choice.upper() == "F":
        inAddress = input("Enter address for file: ")
        if inAddress.upper() == "X": return
        if checkDuplicate(inAddress, "files"):
            print("File already in db. Cancelling add.")
            return
        sql = 'INSERT INTO files (address, tags) VALUES(?, ?)'
        data = (inAddress, "_")
    elif choice.upper() == "T":
        inName = input("Enter name of tag: ")
        if inName.upper() == "X": return
        if checkDuplicate(inName, "tags"):
            print("Tag already in db. Cancelling add.")
            return
        sql = 'INSERT INTO tags (name) VALUES(?)'
        data = [(inName)]
    else:
        print("Invalid option.\n---")
        return
    with con:
        con.execute(sql, data)
    print("---")

# MENU OPTION
# apply an existing tag to a file in the files db
def tagFile():
    # don't need to check tagID for valid as GUI will get tagID from comboBox w/no invalid choices
    fileID = input("Enter file ID to tag: ")
    tagID = input("Enter tag ID to apply: ")
    if fileID.upper() == "X" or tagID.upper() == "X": return
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

# MENU OPTION
# apply the same tag to multiple files in the files db
def multiTagFile():
    tagID = input("Enter tag to apply to multiple files: ")
    fileInput = input("Enter comma-separated list of file IDs to tag: ")
    if tagID.upper() == "X" or fileInput.upper() == "X": return
    fileIDs = fileInput.split(',')
    with con:
        for id in fileIDs:
            print(f"tagging File id {id} with tag {tagID}...")
            sql = "SELECT tags FROM files WHERE id = (?) LIMIT 1"
            sqlIn = [(id)]
            data = con.execute(sql, sqlIn)
            currTags = None
            for row in data:
                currTags = row[0]
            #print(f"currTags = {currTags}")
            if ("_" + tagID + "_") not in currTags:
                currTags += tagID + "_"
                #print(f"will set it to {currTags}")
                sql = "UPDATE files SET tags = (?) WHERE id = (?)"
                sqlIn = (currTags, id)
                con.execute(sql, sqlIn)
            else:
                print(f"File {fileID} already has tag {tagID}")

# MENU OPTION
# remove a tag from a file in the files db
def removeTag():
    fileID = input("Enter file ID to remove tag from: ")
    tagID = input("Enter tag ID to remove: ")
    if fileID.upper() == "X" or tagID.upper() == "X": return
    with con:
        sql = "SELECT tags FROM files WHERE id = (?) LIMIT 1"
        sqlIn = [(fileID)]
        data = con.execute(sql, sqlIn)
        for row in data:
            currTags = row[0]
        if ("_" + tagID + "_") in currTags:
            newTags = currTags.replace("_" + tagID + "_", "_", 1)
            sql = "UPDATE files SET tags = (?) WHERE id = (?)"
            sqlIn = (newTags, fileID)
            con.execute(sql, sqlIn)
        else:
            print(f"File {fileID} does not have tag {tagID}")
    print("---")

# MENU OPTION
# delete item from files or tags db
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
    if deleteID.upper() == "X": return
    data = [(deleteID)]
    with con:
        con.execute(sql, data)
    print("---")

# MENU OPTION
# Add all image files from a folder to the images db
def folderToDB():
    # Get user input on whether search will be recursive or not
    choice = input("Would you like to search recursively? (Y/N)")
    if choice.upper() == "Y":
        recur = True
        print("Recursive search selected")
    else: recur = False
    dir = input("Please enter the path you would like to add to DB: ")
    if dir.upper() == "X": return
    globDir = glob.glob(dir) # get directory using glob
    if len(globDir) != 1: # returns list of len 1 w/directory if exists
        print("Directory not found")
        return
    else:
        print(f"Found directory {globDir}")
    print("Checking for files in directory...")
    # assuming the thing we found was a directory, make a glob of all items in that directory by using wildcard
    dir = globDir[0]
    dir = dir + "/*"
    if recur: dir += "*"
    # assure that directories consistently start with ./
    if (dir[0:2] != "./"):
        dir = "./" + dir
    globDir = glob.glob(dir, recursive=recur)
    imageFiles = [] # list to contain all paths to images of appropriate types
    #print("Found these files:")
    for filePath in globDir:
        #print(f"-path: {filePath}")
        #print(filePath.endswith(".jpg") or filePath.endswith(".png") or filePath.endswith(".gif") or filePath.endswith(".bmp"))
        # Add files with appropriate extensions to list
        # TODO: make the appropriate image extensions dynamic
        if (filePath.endswith(".jpg") or filePath.endswith(".png")    or filePath.endswith(".gif") or filePath.endswith(".bmp")):
            filePath = filePath.replace("\\","/")
            imageFiles.append(filePath)
    # display all found images
    print("All valid files are: ")
    for filePath in imageFiles:
        print(filePath)
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
    print("---")

# simple REPL to show working functions
if __name__ == "__main__":
    print("welcome")
    choice = ""
    while (choice.upper() != "Q"):
        print(menu)
        choice = input(">")
        if choice.upper() == "I":
            x = input("Are you sure? (Y/N)\n")
            if x.upper() == "Y":
                reinitTables()
        elif choice.upper() == "P":
            printAll()
        elif choice.upper() == "A":
            addEntry()
        elif choice.upper() == "T":
            tagFile()
        elif choice.upper() == "R":
            removeTag()
        elif choice.upper() == "D":
            deleteItem()
        elif choice.upper() == "F":
            folderToDB()
        elif choice.upper() == "M":
            multiTagFile()
        elif choice.upper() == "Z":
            print(helperMenu)
            x = input(">")
            if x.upper() == "C":
                y = input("Enter name (for tag) or path (for file): ")
                z = input("Enter type (\'files\' or \'tags\'): ")
                print(checkDuplicate(y,z))