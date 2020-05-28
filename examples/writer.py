import math

from monad.reader import *
from monad.writer import Writer

class Expr: pass
class Lit(Expr):
    '''
    A literal value (number, string, etc...)
    '''
    def __init__(self, val):
        self.val = val
        
    def gen(self):
        return Writer.lift(repr(self.val), w=1)
class Sym(Expr):
    '''
    A symbol (used as identifiers for functions)
    '''
    def __init__(self, name):
        self.name = name
        
    def gen(self):
        return Writer.lift(str(self.name), w=0)
class Op(Expr):
    '''
    Function application (curried)
    '''
    def __init__(self, sym, a1, a2):
        self.sym = sym
        self.a1 = a1
        self.a2 = a2

    def gen(self):
        return self.a1.gen().bind(lambda v1: \
            self.sym.gen().bind(lambda v2: \
                self.a2.gen().bind(lambda v3: \
                    Writer.lift('(%s %s %s)' % (v1, v2, v3), w=0)
                )
            )
        )

if __name__ == '__main__':
    v = Op(Sym('+'), Op(Sym('-'), Lit(1), Op(Sym('*'), Lit(2), Lit(8))), Lit(32)).gen().run()
    assert v[0] == '((1 - (2 * 8)) + 32)' # produces the correct output
    assert v[1] == 4 # it counted that there were 4 literals correctly
