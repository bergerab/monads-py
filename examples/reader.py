import math

from monad.reader import *

class Expr: pass
class Unit(Expr):
    '''
    Indicates an empty value
    '''
    def eval(self):
        return Reader.lift(UnitVal())
class Lit(Expr):
    '''
    A literal value (number, string, etc...)
    '''
    def __init__(self, val):
        self.val = val
        
    def eval(self):
        return Reader.lift(LitVal(self.val))
class Sym(Expr):
    '''
    A symbol (used as identifiers for functions)
    '''
    def __init__(self, name):
        self.name = name
        
    def eval(self):
        return Reader.ask().bind(lambda env: Reader.lift(env.lookup(self.name)))
class App(Expr):
    '''
    Function application (curried)
    '''
    def __init__(self, sym, expr):
        self.sym = sym
        self.expr = expr

    def eval(self):
        return \
            self.sym.eval().bind(lambda f: \
                self.expr.eval().bind(lambda v: \
                                      Reader.lift(f(v))))
class Let(Expr):
    '''
    Binds a name to a value, inside of the body
    '''
    def __init__(self, sym, expr, body):
        self.sym = sym
        self.expr = expr
        self.body = body

    def eval(self):
        return \
            self.expr.eval().bind(lambda v: \
                self.body.eval().local(lambda env: \
                    env.extend(self.sym, v)))
class If(Expr):
    '''
    If predicate ~pred~ is truthy, evaluates ~then~ part, otherwise evaluates ~other~ part
    '''
    def __init__(self, pred, then, other):
        self.pred = pred
        self.then = then
        self.other = other

    def eval(self):
        return self.pred.eval() \
                     .bind(lambda v: \
                        self.then.eval() if bool(v.val) else self.other.eval())

class Val: pass
class UnitVal(Val): pass
class FnVal(Val):
    '''
    A function value
    '''
    def __init__(self, param, body):
        self.param = param
        self.body = body
class LitVal(Val):
    '''
    A literal value
    '''
    def __init__(self, val):
        self.val = val

class Environment:
    '''
    Pure lexical environment
    '''
    def __init__(self, env=None):
        self.env = env if env else []

    def extend(self, name, val):
        return Environment(self.env + [[name, val]])

    def lookup(self, name):
        for sym, val in reversed(self.env):
            if name == sym.name:
                return val
        raise Exception('Symbol %s not found in environment' % name)


DEFAULT_ENVIRONMENT = Environment([
    [Sym('+'), lambda x: lambda y: LitVal(x.val + y.val)],
    [Sym('-'), lambda x: lambda y: LitVal(x.val - y.val)],
    [Sym('*'), lambda x: lambda y: LitVal(x.val * y.val)],
    [Sym('/'), lambda x: lambda y: LitVal(x.val / y.val)],
    [Sym('sqrt'), lambda x: LitVal(math.sqrt(x.val))],    
    [Sym('print'), lambda x: [print(x.val), UnitVal()][1]],
    [Sym('input'), lambda x: [input(x.val), UnitVal()][1]],
    [Sym('pi'), LitVal(math.pi)],
])
'''
The built-in library
'''

if __name__ == '__main__':
    v = Lit(32).eval().run(DEFAULT_ENVIRONMENT)
    assert v.val == 32

    v = Lit('goo').eval().run(DEFAULT_ENVIRONMENT)
    assert v.val == 'goo'

    v = If(Lit(0), Lit('a'), Lit('b')).eval().run(DEFAULT_ENVIRONMENT)
    assert v.val == 'b'

    v = If(Lit(1), Lit('a'), Lit('b')).eval().run(DEFAULT_ENVIRONMENT)
    assert v.val == 'a'
    
    v = Let(Sym('x'), Lit(2), Sym('x')).eval().run(DEFAULT_ENVIRONMENT)
    assert v.val == 2

    v = Sym('+').eval().run(DEFAULT_ENVIRONMENT)
    assert v(Lit(2))(Lit(5)).val == 7

    # Variable shadowing
    v = Let(Sym('a'), Lit(98), Let(Sym('a'), Lit(203), Sym('a'))).eval().run(DEFAULT_ENVIRONMENT)
    assert v.val == 203

    # Solve for c in 5^2 + 2^2 = c^2
    p = Let(Sym('x'), Lit(5),
            Let(Sym('y'), Lit(2),
                Let(Sym('squaredSum'), App(App(Sym('+'), App(App(Sym('*'), Sym('x')), Sym('x'))),
                                           App(App(Sym('*'), Sym('y')), Sym('y'))),
                    App(Sym('sqrt'), Sym('squaredSum')))))
    v = p.eval().run(DEFAULT_ENVIRONMENT)
    assert v.val == math.sqrt(5*5 + 2*2)

    # Make sure console printed the answer
    v = App(Sym('print'), p).eval().run(DEFAULT_ENVIRONMENT)
    assert isinstance(v, UnitVal) # side-effecting operations return Unit
