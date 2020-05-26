from monad.either import Either, Left, Right

def safe_div(n, d):
    if d == 0:
        return Left('Division by zero')
    return Right(n / d)

def safe_parse_int(s):
    try:
        return Right(int(s))
    except ValueError:
        return Left('Input "%s" could not be interpreted as an integer.' % s)

def safe_input_int(prompt):
    s = input(prompt)
    return safe_parse_int(s)
    
if __name__ == '__main__':
   assert Right(1).fmap(lambda x: x + 2).get()  == 3

   # fmap skips Left values
   assert Left(1).fmap(lambda x: x + 2).get()  == 1

   assert Right('one').fmap(lambda x: lambda y: x + y).app(Right('two')).get() == 'onetwo'
   e = safe_input_int('Enter a number to divide 42 by: ').bind(lambda i: \
            safe_div(42, i).bind(lambda v: print('42 / %s = %s' % (i, v))))
   if (isinstance(e, Left)):
       print('The Either monad indicated an error: ', end='')
       print(e.get())
