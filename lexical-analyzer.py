import sys

charClass = 0
lexeme = 'a'
nextChar = 'a'
lexLen = 0
token = 0
nextToken = 0
charPos = 0
comment = False

EOF = None
LETTER = 0
DIGIT = 1
UNKNOWN = 99

INT_LIT = 10
IDENT = 11
ASSIGN_OP = 20
ADD_OP = 21
SUB_OP = 22
MULT_OP = 23
DIV_OP = 24
LEFT_PAREN = 25
RIGHT_PAREN = 26

INPUT = 30
OUTPUT = 31
IF_CODE = 32
ELSE_CODE = 33
BEGIN_CODE = 34
END_CODE = 35
WHILE_CODE = 36
FOR_CODE = 37
COMMENT = 38

N = 0

def main(file):
    global N
    in_fp = open(file, "r")
    txtdata = in_fp.read()
    N = len(txtdata)
    
    if in_fp is None:
        print("Cannot open file")
    else:
        getChar()
        while nextToken != EOF:
            lex()

    in_fp.close()
    return 0


def translate(token):
    if token == EOF:
        return '<EOF>'

    if token == 10:
        return '<number>'
    elif token == 11:
        return '<id>'

    elif token == 20:
        return '<assign_op>'
    elif token == 21:
        return '<add_op>'
    elif token == 22:
        return '<sub_op>'
    elif token == 23:
        return '<mult_op>'
    elif token == 24:
        return '<div_op>'
    elif token == 25:
        return '<lparen>'
    elif token == 26:
        return '<rparen>'

    elif token == 30:
        return '<input>'
    elif token == 31:
        return '<output>'
    elif token == 32:
        return '<if>'
    elif token == 33:
        return '<else>'
    elif token == 34:
        return '<begin>'
    elif token == 35:
        return '<end>'
    elif token == 36:
        return '<while>'
    elif token == 37:
        return '<for>'
    elif token == 38:
        return '<comment>'

    else:
        return '<error>'


def lookup(ch):
    global nextToken
    if ch == '(':
        addChar()
        nextToken = LEFT_PAREN
    elif ch == ')':
        addChar()
        nextToken = RIGHT_PAREN
    elif ch == '+':
        addChar()
        nextToken = ADD_OP
    elif ch == '*':
        addChar()
        nextToken = MULT_OP
    elif ch == '/':
        addChar()
        nextToken = DIV_OP
    elif ch == '=':
        addChar()
        nextToken = ASSIGN_OP
    elif ch == "/*":
        addChar()
        nextToken = BEGIN_CODE
    elif ch == "*/":
        addChar()
        nextToken = END_CODE
    else:
        addChar()
        nextToken = EOF

    return nextToken


def addChar():
    global lexeme
    if lexLen <= 98:
        if lexeme == ' ':
            lexeme = nextChar
        else:
            lexeme = lexeme + nextChar
    else:
        print("Lexeme is too long")


def getChar():
    global charPos
    global nextChar
    global charClass
    global comment

    if N > charPos:
        nextChar = txtdata[charPos]
        charPos += 1
        if nextChar == "/" and txtdata[charPos] == "*":
            nextChar = nextChar + txtdata[charPos]
            charClass = BEGIN_CODE
            charPos += 1
            comment = True

        elif nextChar == "*" and txtdata[charPos] == "/":
            nextChar = nextChar + txtdata[charPos]
            charClass = END_CODE
            charPos += 1
            comment = False

    else:
        nextChar = EOF
        charPos += 1

    if nextChar != EOF:
        if nextChar.isalpha():
            charClass = LETTER
        elif nextChar.isdigit():
            charClass = DIGIT
        else:
            charClass = UNKNOWN
    else:
        charClass = EOF


def getNonBlank():
    if nextChar != EOF:
        while nextChar == ' ' or nextChar == '\n':
            getChar()


def lex():
    global lexeme
    global charClass
    global nextToken
    global comment
    lexeme = ' '
    lexLen = 0
    getNonBlank()
    if charClass == LETTER:
        addChar()
        getChar()
        while charClass == LETTER or charClass == DIGIT:
            addChar()
            getChar()
        if lexeme == 'input':
            nextToken = INPUT
        elif lexeme == 'output':
            nextToken = OUTPUT
        elif lexeme == 'if':
            nextToken = IF_CODE
        elif lexeme == 'else':
            nextToken = ELSE_CODE
        elif lexeme == 'begin':
            nextToken = BEGIN_CODE
        elif lexeme == 'end':
            nextToken == END_CODE
        elif lexeme == 'while':
            nextToken == WHILE_CODE
        elif lexeme == 'for':
            nextToken = FOR_CODE
        elif comment is True:
            nextToken = COMMENT
        else:
            nextToken = IDENT

    elif charClass == DIGIT:
        addChar()
        getChar()
        while charClass == DIGIT:
            addChar()
            getChar()

        nextToken = INT_LIT

    elif charClass == UNKNOWN:
        lookup(nextChar)
        getChar()

    elif charClass == EOF:
        nextToken = EOF
        lexeme = 'EOF'

    print("(" + translate(nextToken) + ", " + lexeme + ")")


if __name__ == "__main__":
    input_file = sys.argv[1]
    if input_file:
        main(input_file)
    else:
        print("please enter a file name")
