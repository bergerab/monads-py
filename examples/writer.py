from monad.writer import Writer

v = Writer.lift(3) \
        .bind(lambda v: \
            Writer.tell(['OK baznar', 'Pee']) \
              .bind(lambda v2: Writer.lift(v + 2))).run()

print(v)
