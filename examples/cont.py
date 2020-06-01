def plus(x, k):
    k(x[0] + x[1])

def div(x, k):
    if x[1] == 0:
        return print('Error: div by zero!')
    else:
        k(x[0] / x[1])

# m a -> (a -> m b) -> m b
# what does it mean to lift a value?


class Cont:
    def __init__(self, f):
        self.f = f # (a -> r) -> r
    
    @staticmethod
    def lift(x):
        return Cont(lambda k: k(x))

    def bind(self, f):
        '''
        Cont r a -> (a -> Cont r b) -> Cont r b
        '''
        return Cont(lambda k: )

# Cont.lift(1 + 3).bind(lambda v: Cont.callCC(lambda k: k(v - 5)))
    
# When you run a continuation you have to flip it inside out.
# because you evaluate inner expressions before outer

# bind gives you the value (if it ever exists). You need to call "callCC" to get the current continuation. Sometimes there is no one listening to the continuation. But that's OK, callCC will still give you a continuation to call.

# what is k?
plus((1, 2), lambda x: \
    div((1, x), lambda v: \
        print(v)))

a :: (Int, Int)
plus :: a -> (a -> r) -> r
# the "a" is the operands to add, the (a -> r) is the continuation (the computation above this one that is waiting on this value), the r at the end is the result of the computation that is waiting on this value
div :: a -> (a -> r) -> r


# how to combine?

a -> ((b -> (b -> r) -> r) -> r)

# data Cont r a = (a -> r) -> r
# r is the return value of the continuation
# a is the input value

#if __name__ == '__main__':
#    plus(3, -3, lambda x: div(3, x, lambda y: print('The answer is ', x)))

