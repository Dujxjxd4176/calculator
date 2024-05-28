from enum import Enum
import math 
"""
grammar rules
Str(term) ->assignment->term
factor -> term (* /)-> factor
unary -> factor ( + - ) -> unary
unary(-) ->(unary /function)
unaryFunc -> function(^)->unaryFunc
unaryFunc(sin cos tan) -> primary
primary ( () / number / variable)

"""
class MathType(Enum):
    LEFTBRACKET = 1
    RIGHTBRACKET = 2
    NUMBER = 3
    PLUS = 4
    MINUS =5
    MULTIPLY =6
    DIVIDE =7
    SPACE =8
    NEGATIVE =9 
    EXPONENT =10 
    LETTER = 11
    ASSIGNMENT =12
    VARIABLE = 13
class Function(Enum):
    SIN =1
    COS =2
    TAN =3
class parser :
    def __init__(self):
        self.IteratorPosition = 0
        self.length = 0
        self.sanatizeInput = []
    class variable:
        def __init__(self,var):
            self.name =  var 
        def eval(self):
            if self.name in varDict :
                return varDict[self.name]
            return self.name
    class assignment:
        def __init__(self, left,right):
            self.left = left
            self.right = right
        def eval(self):
            output = str(self.left.name) + " = " + str(self.right.eval())
            varDict[str(self.left.name)] = self.right.eval()
            return output
        
    class operator:
        def __init__(self,Left,Right,Operator):
            self.Left = Left
            self.Right = Right
            self.Operator = Operator
        def eval(self):
            match self.Operator:
                case MathType.PLUS:
                    return self.Left.eval() +self.Right.eval()
                case MathType.MINUS: 
                    return self.Left.eval() - self.Right.eval()
                case MathType.MULTIPLY:
                    return self.Left.eval() * self.Right.eval()
                case MathType.DIVIDE:
                    return self.Left.eval() / self.Right.eval()
    class bracket:
        def __init__(self,contains):
            self.contains = contains
        def eval (self):
            return self.contains.eval()
    class Number:
        def __init__(self,number):
            self.number = number
        def eval(self):
            return self.number
    class Negative:
        def __init__ (self,contains):
            self.contains = contains
        def eval(self):
            return self.contains.eval() * -1
    class Exponent:
        def __init__(self,left, right):
            self.left = left
            self.right = right
        def eval(self):
            return math.pow(self.left.eval(),self.right.eval())
    class trigFunc:
        def __init__(self, type,contain):
            self.contain = contain
            self.type = type
        def eval(self) :
            match self.type:
                case Function.SIN:
                    return math.sin(self.contain.eval())
                case Function.COS:
                    return math.cos(self.contain.eval())
                case Function.TAN:
                    return math.tan(self.contain.eval())
    def match(self,x,y):
        if self.IteratorPosition >= self.length:
            return False
        if (self.sanatizeInput[self.IteratorPosition][0]== x) or (self.sanatizeInput[self.IteratorPosition][0]==y) :
            return True
        return False
    def Assign(self):
        resultTree = self.term()
        if self.match(MathType.ASSIGNMENT,MathType.ASSIGNMENT):
            self.IteratorPosition +=1
            resultTree = self.assignment(resultTree,self.term())
        return resultTree
    def term(self):
        resultTree = self.factor()
        while self.match(MathType.PLUS,MathType.MINUS):
            tempOp =self. sanatizeInput[self.IteratorPosition][0]
            self.IteratorPosition +=1
            x = self.factor()
            resultTree = self.operator(resultTree,x,tempOp)
        return resultTree
    def factor(self):
        resultTree = self.unary()
        while self.match(MathType.MULTIPLY,MathType.DIVIDE):
            tempOp = self.sanatizeInput[self.IteratorPosition][0]
            self.IteratorPosition +=1
            resultTree = self.operator(resultTree,self.unary(),tempOp)
        return resultTree
    def unary(self):
        if self.match(MathType.NEGATIVE,MathType.NEGATIVE):
            self.IteratorPosition +=1
            return self.Negative(self.unary())
        return self.function()
    def function(self):
        resultTree = self.unaryFunc()
        while self.match(MathType.EXPONENT,MathType.EXPONENT):
            self.IteratorPosition +=1
            resultTree = self.Exponent(resultTree,self.unaryFunc())
        return resultTree
    def unaryFunc(self):
        if self.match(MathType.LETTER,MathType.LETTER):
            tempOP = self.sanatizeInput[self.IteratorPosition][1] 
            self.IteratorPosition +=1  
            match tempOP:
                case Function.SIN:
                    resultTree = self.trigFunc(Function.SIN,self.primary())
                case Function.COS:
                    resultTree = self.trigFunc(Function.COS,self.primary())
                case Function.TAN:
                    resultTree = self.trigFunc(Function.TAN,self.primary())
            return resultTree
        return self.primary()     
    def primary(self):
        if self.match(MathType.LEFTBRACKET,MathType.LEFTBRACKET):
            self.IteratorPosition +=1
            resultTree = self.bracket(self.term())
            self.IteratorPosition +=1
            return resultTree
        if self.match(MathType.NUMBER, MathType.NUMBER):
            resultTree = self.Number(self.sanatizeInput[self.IteratorPosition][1])
            self.IteratorPosition +=1
            return resultTree
        if self.match(MathType.VARIABLE,MathType.VARIABLE):
            resultTree = self.variable(self.sanatizeInput[self.IteratorPosition][1])
            self.IteratorPosition +=1
            return resultTree
    def lexing(self,word):
        prevType = MathType.SPACE
        number =""
        Letter = ""
        for x in  word :
            match prevType:
                case MathType.NUMBER:
                    if x.isnumeric() == False and x != ".":
                        self.sanatizeInput.append([MathType.NUMBER,float(number)])
                        number =""
                    if x == "(" :
                        self.sanatizeInput.append([MathType.MULTIPLY,0])
                    if x.isalpha():
                        self.sanatizeInput.append([MathType.MULTIPLY,0]) 
                case MathType.LETTER:
                    if x.isalpha() == False:
                        Letter = Letter.lower()
                        match Letter :
                            case "sin" :
                                self.sanatizeInput.append([MathType.LETTER,Function.SIN])
                            case "cos" :
                                self.sanatizeInput.append([MathType.LETTER,Function.COS])
                            case "tan"  :
                                self.sanatizeInput.append([MathType.LETTER,Function.TAN]) 
                            case "pi" :
                                self.sanatizeInput.append([MathType.NUMBER,math.pi])
                            case _:
                                if Letter != "":
                                    self.sanatizeInput.append([MathType.VARIABLE,Letter]) 
                        Letter = ""
                case MathType.RIGHTBRACKET:
                    if x.isnumeric():
                        self.sanatizeInput.append([MathType.MULTIPLY,0])
                    elif x == "(" :
                        self.sanatizeInput.append([MathType.MULTIPLY,0])
                    elif x.isalpha():
                        self.sanatizeInput.append([MathType.MULTIPLY,0]) 
                case MathType.MULTIPLY:
                    if x == "*":
                        self.sanatizeInput.pop()
                        x = "^"
                case _:
                    if (x == "-"):
                        x = "~"
            match x:
                case a if (a.isnumeric() or a == "."):
                    number +=x
                    prevType = MathType.NUMBER
                case a if(a.isalpha()):
                    Letter += x
                    prevType = MathType.LETTER
                case "+" :
                    self.sanatizeInput.append([MathType.PLUS,0])
                    prevType = MathType.PLUS
                case "-" :
                    self.sanatizeInput.append([MathType.MINUS,0])
                    prevType = MathType.MINUS
                case "*" :
                    self.sanatizeInput.append([MathType.MULTIPLY,0])
                    prevType = MathType.MULTIPLY
                case "/" :
                    self.sanatizeInput.append([MathType.DIVIDE,0])
                    prevType = MathType.DIVIDE
                case "(" :
                    self.sanatizeInput.append([MathType.LEFTBRACKET,0])
                    prevType = MathType.LEFTBRACKET
                case ")" :
                    self.sanatizeInput.append([MathType.RIGHTBRACKET,0])
                    prevType = MathType.RIGHTBRACKET
                case "~":
                    self.sanatizeInput.append([MathType.NEGATIVE,0])
                    prevType = MathType.NEGATIVE
                case "^":
                    self.sanatizeInput.append([MathType.EXPONENT,0])
                    prevType = MathType.EXPONENT
                case "=":
                    self.sanatizeInput.append([MathType.ASSIGNMENT,0]) 
                    prevType = MathType.ASSIGNMENT
                #case " " :
                    #prevType = MathType.SPACE
        if number != "":
            self.sanatizeInput.append([MathType.NUMBER,float(number)])
        if Letter != "":
            Letter = Letter.lower()
            match Letter:
                case "sin" :
                    self.sanatizeInput.append([MathType.NUMBER,Function.SIN])
                case "cos" :
                    self.sanatizeInput.append([MathType.NUMBER,Function.COS])
                case "tan"  :
                    self.sanatizeInput.append([MathType.NUMBER,Function.TAN])   
                case "pi" :
                    self.sanatizeInput.append([MathType.NUMBER,math.pi])
                case _:
                    self.sanatizeInput.append([MathType.VARIABLE,Letter]) 
    def parse(self,word):
        self.sanatizeInput = []
        self.lexing(word)
        self.IteratorPosition = 0
        self.length = len(self.sanatizeInput)
        return self.Assign().eval()
TheParser = parser()
varDict ={}
print ("iam the right one")
while True:
    print ("what do you want" )
    print(TheParser.parse(input()))

    