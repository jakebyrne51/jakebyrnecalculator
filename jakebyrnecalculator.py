class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__

class Stack:
    '''
        >>> x=Stack()
        >>> x.pop()
        >>> x.push(2)
        >>> x.push(4)
        >>> x.push(6)
        >>> x
        Top:Node(6)
        Stack:
        6
        4
        2
        >>> x.pop()
        6
        >>> x
        Top:Node(4)
        Stack:
        4
        2
        >>> len(x)
        2
        >>> x.peek()
        4
    '''
    def __init__(self):
        self.top = None
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__

    #Checks if stack is empty
    def isEmpty(self):
        # YOUR CODE STARTS HERE
        return self.top == None

    #Gets the length of the stack
    def __len__(self): 
        # YOUR CODE STARTS HERE
        count = 0
        current = self.top
        while current:
            count+=1
            current=current.next
        return count

    #Pushs a new node into the stack
    def push(self, value):
        # YOUR CODE STARTS HERE
            newStackNode = Node(value) #Creates node of given value to be added
            newStackNode.next = self.top #Sets next node to be top node of stack
            self.top = newStackNode #sets top node of stack to node of given value to be added 

    #Removes the last added node to the stack
    def pop(self):
        # YOUR CODE STARTS HERE
        if self.top == None: #Checks if the stack is empty
            return None
        else:
            val = self.top.value #holds the value
            self.top = self.top.next #removes the node 
            return val #returns val of removed node

    #Looks at the value of the last added node without changing it
    def peek(self):
        # YOUR CODE STARTS HERE
        if not self.isEmpty():
            return self.top.value
        else:
            return None

class Calculator:
    def __init__(self):
        self.__expr = None


    @property
    def getExpr(self):
        return self.__expr

#Sets Expression
    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr=new_expr
        else:
            print('setExpr error: Invalid expression')
            return None

#CHecks if txt is valid number
    def _isNumber(self, txt):
        '''
            >>> x=Calculator()
            >>> x._isNumber(' 2.560 ')
            True
            >>> x._isNumber('7 56')
            False
            >>> x._isNumber('2.56p')
            False
        '''
        # YOUR CODE STARTS HERE
        try:
            num = float(txt)
            return True
        except ValueError:
            return False

#Converts expression from infix to postfix notation to allow for easier calculations
    def _getPostfix(self, txt):
        '''
            Required: _getPostfix must create and use a Stack object for expression processing

            >>> x=Calculator()
            >>> x._getPostfix('2 ^ 4')
            '2.0 4.0 ^'
            >>> x._getPostfix('2')
            '2.0'
            >>> x._getPostfix('2.1 * 5 + 3 ^ 2 + 1 + 4.45')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.45 +'
            >>> x._getPostfix('2 * 5.34 + 3 ^ 2 + 1 + 4')
            '2.0 5.34 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('2.1 * 5 + 3 ^ 2 + 1 + 4')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('( 2.5 )')
            '2.5'
            >>> x._getPostfix('( 2 { 5.0 } )')
            '2.0 5.0 *'
            >>> x._getPostfix(' 5 ( 2 + { 5 + 3.5 } )')
            '5.0 2.0 5.0 3.5 + + *'
            >>> x._getPostfix ('( { 2 } )')
            '2.0'
            >>> x._getPostfix ('2 * ( [ 5 + -3 ] ^ 2 + { 1 + 4 } )')
            '2.0 5.0 -3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('[ 2 * ( < 5 + 3 > ^ 2 + ( 1 + 4 ) ) ]')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('( { 2 * { { 5 + 3 } ^ 2 + ( 1 + 4 ) } } )')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix('2 * < -5 + 3 > ^ 2 + < 1 + 4 >')
            '2.0 -5.0 3.0 + 2.0 ^ * 1.0 4.0 + +'
            >>> x._getPostfix('2 * 5 + 3 ^ + -2 + 1 + 4')
            >>> x._getPostfix('2 * 5 + 3 ^ - 2 + 1 + 4')
            >>> x._getPostfix('2    5')
            >>> x._getPostfix('25 +')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^ 2 + ( 1 + 4 ')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^ 2 + ( 1 + 4 ]')
            >>> x._getPostfix(' ( 2 * { 5 + 3 ) ^ 2 + ( 1 + 4 ] }')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^ 2 + ) 1 + 4 (')
            >>> x._getPostfix('2 * 5% + 3 ^ + -2 + 1 + 4')
        '''

        # YOUR CODE STARTS HERE
        postfixStack = Stack()  # method must use postfixStack to compute the postfix expression
        #Dictionaries to handle order of ops, and all types of parenthesis
        orderOfOpsDict = {"^": 3, "*": 2, "/": 2, "+": 1, "-": 1}
        openParen = {'(': 1, '[': 2, '{': 3, '<': 4}
        closedParen = {')': 1, ']': 2, '}': 3, '>': 4}
        postFix = []
        prevElement = None #tracks prev element
        numCount = 0 #counts nums in expressions
        opCount = 0
        parenCount = 0
        for element in txt.split():
            if self.isInvalidSymbol(element, orderOfOpsDict, openParen, closedParen):
                return None
            if self._isNumber(element):
                numCount += 1
                postFix.append(str(float(element)))
            elif element in orderOfOpsDict:
                opCount += 1
                #higher priority in order of ops
                while self.isOperatorWithHigherPriority(postfixStack, orderOfOpsDict, element) and element != "^":
                    postFix.append(postfixStack.pop())
                postfixStack.push(element)
            #element is open parenthesis
            elif element in openParen:
                parenCount += 1
                if prevElement is not None:
                    if self.isImplicitMultiplication(prevElement, closedParen):
                        postfixStack.push("*")
                    #Checks for uneven parenthesis
                    if postfixStack.peek() in closedParen:
                        return None
                    postfixStack.push(element)
                else:
                    postfixStack.push(element)
            #element is closed parenthesis
            elif element in closedParen:
                parenCount += 1
                #adds operations to expression
                while postfixStack.peek() in orderOfOpsDict:
                    postFix.append(postfixStack.pop())
                if postfixStack.peek() not in openParen:
                    return None
                #matching parenthesis check
                if openParen[postfixStack.peek()] == closedParen[element]:
                    postfixStack.pop()
                else:
                    return None
            prevElement = element
        #Handles remaining errors in the expression and remaining parenthesis in the stack.
        while not postfixStack.isEmpty():
            if self.remainingParenthesis(postfixStack, openParen, closedParen):
                postfixStack.pop()
            else:
                postFix.append(postfixStack.pop())
        if self.isInvalidExpression(numCount, opCount, parenCount):
            return None
        return " ".join(postFix)


    #Helper Methods For the getPostfix notation method
    def isInvalidExpression(self, numCount, opCount, parenCount):
        if (numCount == opCount) or (opCount == 0 and numCount > 1 and parenCount == 0) or (opCount == 0 and numCount == 0) or (parenCount % 2 != 0) or (opCount > numCount):
            return True
        return False

    def isOperatorWithHigherPriority(self, postfixStack, orderOfOpsDict, element):
        if postfixStack.peek() in orderOfOpsDict and self.isHigherPriority(orderOfOpsDict, postfixStack, element):
            return True
        else:
            return False

    def isInvalidSymbol(self, element, orderOfOpsDict, openParen, closedParen):
        if not self._isNumber(element) and element not in orderOfOpsDict and element not in openParen and element not in closedParen:
            return True
        return False

    def isHigherPriority(self, orderOfOpsDict, postfixStack, element):
        if orderOfOpsDict[postfixStack.peek()] >= orderOfOpsDict[element]:
            return True
        return False

    def isImplicitMultiplication(self, prevElement, closedParen):
        if self._isNumber(prevElement) or prevElement in closedParen:
            return True
        return False

    def remainingParenthesis(self, postfixStack, openParen, closedParen):
        if postfixStack.peek() in openParen or postfixStack.peek() in closedParen:
            return True
        return False
        

    @property
    def calculate(self):
        '''
            calculate must call _getPostfix
            calculate must create and use a Stack object to compute the final result as shown in the video lectures
            
            >>> x=Calculator()
            >>> x.setExpr('4 + 3 - 2')
            >>> x.calculate
            5.0
            >>> x.setExpr('-2 + 3.5')
            >>> x.calculate
            1.5
            >>> x.setExpr('4 + 3.65 - 2 / 2')
            >>> x.calculate
            6.65
            >>> x.setExpr('23 / 12 - 223 + 5.25 * 4 * 3423')
            >>> x.calculate
            71661.91666666667
            >>> x.setExpr(' 2 - 3 * 4')
            >>> x.calculate
            -10.0
            >>> x.setExpr('7 ^ 2 ^ 3')
            >>> x.calculate
            5764801.0
            >>> x.setExpr(' 3 * ( [ ( 10 - 2 * 3 ) ] )')
            >>> x.calculate
            12.0
            >>> x.setExpr('8 / 4 * { 3 - 2.45 * [ 4 - 2 ^ 3 ] } + 3')
            >>> x.calculate
            28.6
            >>> x.setExpr('2 * [ 4 + 2 * < 5 - 3 ^ 2 > + 1 ] + 4')
            >>> x.calculate
            -2.0
            >>> x.setExpr(' 2.5 + 3 * ( 2 + { 3.0 } * ( 5 ^ 2 - 2 * 3 ^ ( 2 ) ) * < 4 > ) * [ 2 / 8 + 2 * ( 3 - 1 / 3 ) ] - 2 / 3 ^ 2')
            >>> x.calculate
            1442.7777777777778
            >>> x.setExpr('( 3.5 ) [ 15 ]') 
            >>> x.calculate
            52.5
            >>> x.setExpr('3 { 5 } - 15 + 85 [ 12 ]') 
            >>> x.calculate
            1020.0
            >>> x.setExpr("( -2 / 6 ) + ( 5 { ( 9.4 ) } )") 
            >>> x.calculate
            46.666666666666664
            
            # In invalid expressions, you might print an error message, but code must return None, adjust doctest accordingly

            >>> x.setExpr(" 4 + + 3 + 2") 
            >>> x.calculate
            >>> x.setExpr("4  3 + 2")
            >>> x.calculate
            >>> x.setExpr('( ( 2 ) * 10 - 3 * [ 2 - 3 * 2 ) ]')
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 * ( 2 - 3 * 2 ) )')
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 * / ( 2 - 3 * 2 )')
            >>> x.calculate
            >>> x.setExpr(' ) 2 ( * 10 - 3 * ( 2 - 3 * 2 ) ')
            >>> x.calculate
        '''

        if not isinstance(self.__expr,str) or len(self.__expr)<=0:
            print("Argument error in calculate")
            return None

        calcStack = Stack()   # method must use calcStack to compute the expression

        # YOUR CODE STARTS HERE
        #Gets postFix expression
        postFix = self._getPostfix(self.__expr)
        if postFix == None:
            return None
        for element in postFix.split():
            if self._isNumber(element):
                #Nums pushed to stack
                calcStack.push(float(element))
            else:
                if not calcStack.isEmpty():
                    #Operations are used on top two numbers in the stack
                    if element == "+":
                        #Operation done on top two nums, and newVal is added to top of stack
                        newVal = float(calcStack.pop()) + float(calcStack.pop())
                        calcStack.push(newVal)
                    if element == "-":
                        top = float(calcStack.pop())
                        newVal = float(calcStack.pop()) - top
                        calcStack.push(newVal)
                    if element == "*":
                        newVal = float(calcStack.pop()) * float(calcStack.pop())
                        calcStack.push(newVal)
                    if element =="/":
                        top = float(calcStack.pop())
                        newVal = float(calcStack.pop()) / top
                        calcStack.push(newVal)
                    if element == "^":
                        top = float(calcStack.pop())
                        newVal = float(calcStack.pop())**top
                        calcStack.push(newVal)
        #Stack should only contain final value at this point. Theres an issue with the expression otherwise
        if calcStack.__len__() > 1:
            return None
        return calcStack.pop()


class AdvancedCalculator:
    '''
        >>> C = AdvancedCalculator()
        >>> C.states == {}
        True
        >>> C.setExpression('a = 5;b = 7 + a;a = 7;c = a + b;c = a * 0;return c')
        >>> C.calculateExpressions() == {'a = 5': {'a': 5.0}, 'b = 7 + a': {'a': 5.0, 'b': 12.0}, 'a = 7': {'a': 7.0, 'b': 12.0}, 'c = a + b': {'a': 7.0, 'b': 12.0, 'c': 19.0}, 'c = a * 0': {'a': 7.0, 'b': 12.0, 'c': 0.0}, '_return_': 0.0}
        True
        >>> C.states == {'a': 7.0, 'b': 12.0, 'c': 0.0}
        True
        >>> C.setExpression('x1 = 5;x2 = 7 [ x1 - 1 ];x1 = x2 - x1;return x2 + x1 ^ 3')
        >>> C.states == {}
        True
        >>> C.calculateExpressions() == {'x1 = 5': {'x1': 5.0}, 'x2 = 7 [ x1 - 1 ]': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        True
        >>> print(C.calculateExpressions())
        {'x1 = 5': {'x1': 5.0}, 'x2 = 7 [ x1 - 1 ]': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        >>> C.states == {'x1': 23.0, 'x2': 28.0}
        True
        >>> C.setExpression('x1 = 5 * 5 + 97;x2 = 7 * { x1 / 2 };x1 = x2 * 7 / x1;return x1 ( x2 - 5 )')
        >>> C.calculateExpressions() == {'x1 = 5 * 5 + 97': {'x1': 122.0}, 'x2 = 7 * { x1 / 2 }': {'x1': 122.0, 'x2': 427.0}, 'x1 = x2 * 7 / x1': {'x1': 24.5, 'x2': 427.0}, '_return_': 10339.0}
        True
        >>> C.states == {'x1': 24.5, 'x2': 427.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;C = A + B;A = 20;D = A + B + C;return D - A')
        >>> C.calculateExpressions() == {'A = 1': {'A': 1.0}, 'B = A + 9': {'A': 1.0, 'B': 10.0}, 'C = A + B': {'A': 1.0, 'B': 10.0, 'C': 11.0}, 'A = 20': {'A': 20.0, 'B': 10.0, 'C': 11.0}, 'D = A + B + C': {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}, '_return_': 21.0}
        True
        >>> C.states == {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;2C = A + B;A = 20;D = A + B + C;return D + A')
        >>> C.calculateExpressions() is None
        True
        >>> C.states == {}
        True
    '''
    '''
    A = 1
    B = A + 9
    2C = A + B
    A = 20
    D = A + B + C
    return D + A
    '''
    def __init__(self):
        self.expressions = ''
        self.states = {}

    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}

    def _isVariable(self, word):
        '''
            >>> C = AdvancedCalculator()
            >>> C._isVariable('volume')
            True
            >>> C._isVariable('4volume')
            False
            >>> C._isVariable('volume2')
            True
            >>> C._isVariable('vol%2')
            False
        '''
        # YOUR CODE STARTS HERE
        #Checks if first char is a num
        if word[0].isdigit():
            return False
        for char in word:
            if not char.isalnum():
                return False
        return True
       

    def _replaceVariables(self, expr):
        '''
            >>> C = AdvancedCalculator()
            >>> C.states = {'x1': 23.0, 'x2': 28.0}
            >>> C._replaceVariables('1')
            '1'
            >>> C._replaceVariables('105 + x')
            >>> C._replaceVariables('7 ( x1 - 1 )')
            '7 ( 23.0 - 1 )'
            >>> C._replaceVariables('x2 - x1')
            '28.0 - 23.0'
        '''
        # YOUR CODE STARTS HERE
        newExpr = []
        replacedVal = ""
        for element in expr.split():
            #Checks if element is a var and is in the variable states dictionary
            if self._isVariable(element):
                if element in self.states.keys():
                     newExpr += [str(self.states[element])]
                else:
                    return None  
            else:
                newExpr += element
        return " ".join(newExpr)

    def calculateExpressions(self):
        self.states = {} 
        calcObj = Calculator()     # method must use calcObj to compute each expression
        # YOUR CODE STARTS HERE
        #Dict to track expression and var states dict at that point
        expressionDict = {}
        calcObj.setExpr(self.expressions)
        #Tracks currentState and previous expression
        currentState = None
        prevExpression = None
        prevDict = {}
        for expression in self.expressions.split(";"):
            #If expression is last element(which is always has return in it)
            if "return" in expression.split():
                calcExpression = " ".join(expression.split()[1:])
                fixedExpression = self._replaceVariables(calcExpression)
                calcObj.setExpr(str(fixedExpression))
                expressionDict['_return_'] = calcObj.calculate
            currentState = {}
            leftSide = None
            for equationSides in expression.split(" = "):
                #Var below handles expressions that are nums but need to be calculated first (ex. '5 * 5 * 3 + 2')
                neededExprCalc = None
                myExpr = calcObj.setExpr(str(equationSides))
                if calcObj.calculate is not None:
                    neededExprCalc = calcObj.calculate
                if self.isInvalidVariable(leftSide, expression, equationSides):
                    self.states = {}
                    expressionDict = {}
                    return None
                if not calcObj._isNumber(equationSides) and leftSide is None:
                        leftSide = equationSides
                elif self.isRightSideANum(neededExprCalc, leftSide, calcObj):
                    self.states[leftSide] = float(neededExprCalc)
                    currentState[leftSide] = float(neededExprCalc)
                    #Checks if its not first expression
                    if prevExpression is not None:
                        expressionDict[expression] = {**prevExpression, **currentState}
                    else:
                        expressionDict[expression] = currentState
                    prevDict = expressionDict[expression]
                elif self.isRightSideANum(neededExprCalc, leftSide, calcObj) == False:
                    rightSideValue = 0
                    #Checks if there ae variables to be replaced/if variables are valid
                    if self._replaceVariables(equationSides) is not None:
                        newEquation = self._replaceVariables(equationSides)
                        calcObj.setExpr(str(newEquation))
                        rightSideValue = calcObj.calculate
                        self.states[leftSide] = rightSideValue
                        currentState[leftSide] = rightSideValue
                        if prevExpression is not None:
                            expressionDict[expression] = {**prevExpression, **currentState}
                        else:
                            expressionDict[expression] = currentState
                        prevDict = expressionDict[expression]
                    leftSide = equationSides
                    #Checks if expression is in the expression and self.states tracking dict
                if expression in expressionDict:    
                    prevExpression = expressionDict[expression]
        return expressionDict
    
    #My Helper Methods for the calculateExpressions method
    def isInvalidVariable(self, leftSide, expression, equationSides):
        if leftSide is None and "return" not in expression.split() and not self._isVariable(str(equationSides)):
            return True
        return False
    
    def isRightSideANum(self, neededExprCalc, leftSide, calcObj):
        if neededExprCalc is not None and leftSide is not None and calcObj._isNumber(neededExprCalc):
            return True
        return False

def run_tests():
    import doctest

    #- Run tests in all docstrings
    doctest.testmod(verbose=True)
    
    #- Run tests per class - Uncomment the next line to run doctest by function. Replace Stack with the name of the function you want to test
    #doctest.run_docstring_examples(Calculator, globals(), name='HW3',verbose=True)   

if __name__ == "__main__":
    #self, numCount, opCount, parenCount
    '''
    obj = Calculator()
    print(obj.isInvalidExpression(2, 0, 4))
    obj._getPostfix("2 * (5 + 4")
    '''
    run_tests()