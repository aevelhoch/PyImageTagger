# max subquery/parens: 2
MAX_PARENS = 1
TAGS = [(1,"red"),(2,"orange"),(3,"yellow"),(4,"green"),(5,"blue"),(7,"purple")]

# split sentence into tokens list, separating parens if possible
def tokenizeExpression(expression):
    # split on whitespace
    splitExp = expression.split()
    finalExp = []
    for token in splitExp:
        # extract inner tokens '(like_this)' but not these '()'
        if token[0] == "(" and token[-1] == ")":
            if len(token) > 2:
                finalExp.append(token[1:-1])
        # extract left parens tokens '(like_this' but not this '('
        elif token[0] == "(":
            finalExp.append("(")
            if len(token) > 1:
                finalExp.append(token[1:])
        # extract right parens tokens 'like_this)' but not this ')'
        elif token[-1] == ")":
            if len(token) > 1:
                finalExp.append(token[:-1])
            finalExp.append(")")
        # extract all other tokens
        else:
            finalExp.append(token)
    # return tokens list
    return finalExp
    
# validate tokens list, ensure all tokens are valid and that there are not more than MAX_PARENS parens
def validateTokensExp(expTokens, tags):
    # create a list of valid tokens to check against
    validTokens = ["v","^","x"]
    for tag in tags:
        validTokens.append(str(tag[1]))
    parens = 0
    # ensure all tokens are either valid or parens, and make sure there are the correct number of parens
    for token in expTokens:
        if token not in validTokens:
            if token == "(":
                parens += 1
            elif token == ")":
                parens -= 1
            else:
                return False
        if parens < 0 or parens > MAX_PARENS:
            return False
    if parens != 0: return False
    return True
    
# validate tokens list, converts expressions to typeTokens format so helper function can validate them
def validateExpressionExp(expTokens):
    currParens = 0
    typeTokens = []
    typeTokensSub = []
    inSub = False
    for token in expTokens:
        if not inSub:
            if token != "(" and token != ")":
                if token in ["v","^","x"]:
                    typeTokens.append("op")
                else:
                    typeTokens.append("tag")
            if token == "(":
                inSub = True
                typeTokens.append("tag")
        elif inSub:
            if token in ["v","^","x"]:
                typeTokensSub.append("op")
            elif token != ")":
                typeTokensSub.append("tag")
            elif token == ")":
                inSub = False
                for index, type in enumerate(typeTokensSub):
                    if type == "tag":
                        if index % 2 == 1:
                            return False
                    if type == "op":
                        if index % 2 == 0:
                            return False
                typeTokensSub = []
    for index, type in enumerate(typeTokens):
        if type == "tag":
            if index % 2 == 1:
                return False
        if type == "op":
            if index % 2 == 0:
                return False
    return True
    
# convert tokenized expression to proper expression and tags list
def convertTokenizedExp(expTokens,tagsIn):
    tags = []
    convertTags = []
    for tag in tagsIn:
        tags.append(tag[1])
        convertTags.append(tag[0])
    operators = ["v","x","^","(",")"]
    convertOperators = ["OR", "NOT", "AND", "(", ")"]
    tagsList = []
    finalExpression = ""
    for token in expTokens:
        if token in operators:
            finalExpression += convertOperators[operators.index(token)]
        else:
            finalExpression += "(?)"
            tagsList.append(f"%_{convertTags[tags.index(token)]}_%")
        finalExpression += " "
    return finalExpression, tagsList
    
# convert tokenized expression to SQLite query
def translateToSQLite(expTokens):
    sqlQuery = ""
    operators = ["v","x","^","(",")"]
    convertOperators = ["UNION ","EXCEPT ","INTERSECT ","SELECT * FROM ( ",") "]
    tagConvert = "SELECT * FROM files WHERE tags LIKE (?) "
    for token in expTokens:
        if token in operators:
            sqlQuery += convertOperators[operators.index(token)]
        else:
            sqlQuery += tagConvert
    return sqlQuery
    

if __name__ == "__main__":
    print(f"tags: {TAGS}")
    exp = input("""
    Enter a boolean expressions using ONLY:
    () - perform first (must be paired)
    v - OR (for UNION)
    ^ - AND (for INTERSECTION)
    x - NOT (for EXCEPT)
    tagname - the name of any tag
    ' ' - spaces to seperate
>""")
    exp = tokenizeExpression(exp)
    print(f"tokenized Expression: {exp}")
    tokens = validateTokensExp(exp, TAGS)
    expression = validateExpressionExp(exp)
    if tokens and expression:
        print("Expression is valid!")
        convertResults = convertTokenizedExp(exp, TAGS)
        print(f"converted expression: {convertResults[0]}")
        print(f"data for execute expression: {convertResults[1]}")
        finalSQLData = convertResults[1]
        print(f"Final translation:\n {translateToSQLite(exp)}")
    else:
        print(f"Valid tokens: {tokens}")
        print(f"Valid expression: {expression}")