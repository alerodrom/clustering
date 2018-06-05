import time


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print()
        print("*************************")
        print()
        print('La función %s tarda %0.3f s' % (f.__name__, (time2 - time1)))
        print()
        print("*************************")
        print()
        return ret

    return wrap
