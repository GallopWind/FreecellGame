def func1():
    return 1, 2


def func2(a, b):
    print(a, b)


func2(*func1())
