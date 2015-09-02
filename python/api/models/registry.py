class Registry:
    r = {}

    @classmethod
    def register(cls, name, *args):
        def decorator(fn):
            cls.r[name] = {'f' : fn, 'args' : args}
            return fn
        return decorator
