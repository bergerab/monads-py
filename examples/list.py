import math

from monad.list import List
from monad.either import Left, Right
from either import safe_input_int

def validate_max(v):
    return Left('The max triangle side length must be between 10 and 1000.') if 10 > v < 1000 else Right(v)

class Answer:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.is_integer = c % 1 == 0

    def __repr__(self):
        return '%s^2 + %s^2 = %s^2' % (self.a, self.b, int(self.c) if self.is_integer else self.c)

if __name__ == '__main__':
    v = safe_input_int('Enter a max triangle side length [10 - 1000]: ') \
        .bind(validate_max) \
        .bind(lambda max: \
              Right(List(range(1, max)).bind(lambda a: \
                    List(range(1, max)).bind(lambda b: List.lift(Answer(a, b, math.sqrt(a*a + b*b)))) \
                            .filter(lambda ans: ans.is_integer))))
    if isinstance(v, Left):
        print('An error has occured: ' + v.get())
    else:
        print('\n'.join(map(repr, v.get().get())))
