def funcKWArger(arcdspcmd, **kwargs):
    """
    **kwargs lets you pass in arbitrary amounts of keyword arguments
    """
    print("arcdspcmd:", arcdspcmd)
    if len(*kwargs) != 0:
        for key, value in kwargs.items():
            print(key, value)


def funcArger(arcdspcmd, *args):
    """
    *args lets you pass in arbitrary amounts of non-keyword arguments
    """
    print("arcdspcmd:", arcdspcmd)
    if len(args) != 0:
        for i, value in enumerate(args):
            print(i+1, value)


if __name__ == "__main__":
    arg1 = "Hello"
    arg2 = "World"
    arg3 = "in"
    arg4 = "function"

    funcKWArger("funcKWArger", arg1=arg1)
    funcArger("funcArger", arg1, arg2)
