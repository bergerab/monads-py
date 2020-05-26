from monad.maybe import Maybe, Just, Nothing

def lift_input(prompt):
    text = input(prompt)
    if text:
        return Just(text)
    return Nothing()

def try_parse_int(s):
    try:
        return Just(int(s))
    except ValueError:
        return Nothing()

def input_int(prompt):
    m = lift_input(prompt).bind(try_parse_int)
    if isinstance(m, Nothing):
        return input_int(prompt)
    return m

input_int('X = ') \
    .bind(lambda x: input_int('Y = ').bind(lambda y: Maybe.lift(x + y))) \
    .fmap(lambda sum: print('X + Y = ' + str(sum)))
