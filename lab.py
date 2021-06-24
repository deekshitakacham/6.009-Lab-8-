import doctest


# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.


class Symbol:
    
    def __add__(self, other):
        #Var('a')+1
        left = self
        right = other
        return Add(left, right)
    
    def __radd__(self, other):
        #Var('a')+1
        right = self
        left = other
        return Add(left, right)
    
    def __sub__(self, other):
        left = self
        right = other
        return Sub(left, right)
    
    def __rsub__(self, other):
        right = self
        left = other
        return Sub(left, right)
    
    def __mul__(self, other):
        left = self
        right = other
        return Mul(left, right)
    
    def __rmul__(self, other):
        right = self
        left = other
        return Mul(left, right)
    
    def __truediv__(self, other):
        left = self
        right = other
        return Div(left, right)
    
    def __rtruediv__(self, other):
        right = self
        left = other
        return Div(left, right)
    
    


class Var(Symbol):
    
    precedence = 0 
    
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n
        

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Var(' + repr(self.name) + ')'
    
    def deriv(self, var):
        #base case 1: if it's a variable
        #base case 2: if it's a contant 
        if self.name != var:
            return Num(0) 
        
        #if self.name == var:
        return Num(1)
    
    def simplify(self):
        return self
    
    def eval(self, mapping):
        ##return mapping of self b/c no more mapping for left and right
        result = mapping[self.name]
        
        return result
        
        


class Num(Symbol):
    
    precedence = 0
    
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return 'Num(' + repr(self.n) + ')'
    
    def deriv(self, var):
        #base case 1: if it's a variable
        #base case 2: if it's a contant 
        return Num(0) 

    def simplify(self):
        return self
    
    def eval(self, mapping):
        return self.n


class BinOp(Symbol):
    """
    Add docstring
    """
    def __init__(self, left, right):
        """
        Add docstring
        """
        if isinstance(right, Symbol):
            self.right = right
        else:
            if type(right) ==  str:
                self.right = Var(right)
            else:
                self.right = Num(right)
        if isinstance(left, Symbol):
            self.left = left
        else:
            if type(left) ==  str:
                self.left = Var(left)
            else:
                self.left = Num(left)
                
        
        
    def simplify(self):
        
        left = self.left.simplify()
        right = self.right.simplify()
        
        
        if isinstance(left, Num) and isinstance(right, Num):
            #want left and right to be nums
            return Num(self.combine(left.n, right.n))
        
        return self.helper_simp(left, right)
    
    
    def eval(self, mapping): 
        
        left_map = self.left.eval(mapping)
        right_map = self.right.eval(mapping)
        
        return self.combine(left_map, right_map)
    
    def __str__(self):
        """
        
        """
        #Mul(Add(1, 2), Add(3, 4))
        #-> (1+2)*(3+4)

        if self.precedence < self.right.precedence:
            right = '('+str(self.right)+")"
            
        else: 
            right = str(self.right)
            
        if self.precedence < self.left.precedence:
            left = '('+str(self.left)+")"
            
        else: 
            left = str(self.left)
            
        return left+' '+self.expression+' '+right
        
        
        
        
        
    
            

class Add(BinOp):
    """
    Compute the Add class for binop
    """   
    expression = '+'
    precedence = 5 
    
    
    def helper_simp(self, a, b):
        if isinstance(a, Num) and a.n == 0:
            return b
        elif isinstance(b, Num) and b.n == 0:
            return a
        else:
            return a+b
        
    def combine(self, a, b):
        return a+b
                    

    def __repr__(self):
        """
      
        """
        return "Add(" + repr(self.left) + ", " + repr(self.right) + ")"
    
    def deriv(self, var):
        #2x+1
        #symbol
        return self.left.deriv(var)+ self.right.deriv(var) 
        
    
class Sub(BinOp):
    """
    Computes the subtraction function for binop 
    """   
    expression = '-'
    precedence = 5
    
    
    def helper_simp(self, a, b):
        if isinstance(b, Num) and b.n == 0:
            return a
        else:
            return a-b
                
    def combine(self, a, b):
        return a-b
    


    def __repr__(self):
        """
      
        """
        return "Sub(" + repr(self.left) + ", " + repr(self.right) + ")"
        
    
    
    def deriv(self, var):
        #2x+1
        #symbol
        return self.left.deriv(var)-self.right.deriv(var)


class Mul(BinOp):
    """
    Computes the multiplication function for binop 
    """   
    expression = '*'
    precedence = 3
                
    def helper_simp(self, a, b):
        if isinstance(a, Num) and a.n == 0:
            return Num(0)
        elif isinstance(b, Num) and b.n == 0:
            return Num(0)
        elif isinstance(b, Num) and b.n == 1:
            return a
        elif isinstance(a, Num) and a.n == 1:
            return b
        else:
            return a*b
        
    def combine(self, a, b):
        return a*b
                


    def __repr__(self):
        """
      
        """
        return "Mul(" + repr(self.left) + ", " + repr(self.right) + ")"
    
    def deriv(self, var):
        #2x+1
        #symbol
        return self.left.deriv(var)*self.right+ self.right.deriv(var)*self.left
    
class Div(BinOp):
    """

    """   
    expression = '/'
    precedence = 3
    
    def helper_simp(self, a, b):
        if isinstance(a, Num) and a.n == 0:
            return Num(0)
        elif isinstance(b, Num) and b.n == 1:
            return a
        else:
            return a/b
                
    def combine(self, a, b):
        return a/b             


    
    def deriv(self, var):
        #2x+1
        #symbol
        numerator = (self.right*self.left.deriv(var))-(self.left*self.right.deriv(var))
        denominator = self.right*self.right
        return numerator/denominator

    def __repr__(self):
        """
      
        """
        return "Div(" + repr(self.left) + ", " + repr(self.right) + ")"  
    
    
def sym(string):
    symbol = parse(tokenize(string))
    return symbol 

    
def tokenize(string):
    
    result1 = string.split( )
    final_result = []
    
    for segment in result1: 
        
        
        if ')' in segment: 
            index_end = segment.count(')')
            
            token1 = segment[0:-index_end]
            final_result.append(token1)
            
            for i in range(index_end):
                final_result.append(')')
    
        
        elif '(' in segment:
            
            index_beg = segment.count('(')
            token2 = segment[index_beg:]
            
            for i in range(index_beg):
                final_result.append('(')
                
            final_result.append(token2)
                
            
        else: 
            final_result.append(segment)
            
    return final_result
   


    
def parse(tokens):
    
    def parse_expression(index):
        current = tokens[index]
        
        if current.isalpha():
            return (Var(current), index+1)
        
        if current == '(':
            left_parse, left = parse_expression(tokens, index+1)
            right_parse, right = parse_expression(tokens, left+1)
#            left_parse = parse_expression(tokens, index+1)[0]
#            left = parse_expression(tokens, index+1)[1]
#            right_parse = parse_expression(tokens, left+1)[0]
#            right = parse_expression(tokens, left+1)[1]
            
            if tokens[left] == '+':
                return (Add(left_parse, right_parse), right+1)
            
            if tokens[left] == '-':
                return (Sub(left_parse, right_parse), right+1)
            
            if tokens[left] == '*':
                return (Mul(left_parse, right_parse), right+1)
            
            if tokens[left] == '/':
                return (Div(left_parse, right_parse), right+1)
        
        
        return (Num(int(current)), index+1)
    
    return parse_expression(tokens, 0)[0]

    
if __name__ == '__main__':
    doctest.testmod()
    pass

