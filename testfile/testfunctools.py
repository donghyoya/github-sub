from functools import singledispatch

class A:
    def getOne(self):
        return 1
    
    def getTwo(self):
        return 2

class B:
    def getThree(self):
        return 3
    
    def getFour(self):
        return 4

@singledispatch
def add(num1: int, num2):
    raise NotImplementedError("Unsupported type")


@add.register(A)
def _(num1:int, num2: A):
    result = num2.getOne()
    print(result)
    return result

@add.register(int)
def _(num1:int, num2: int):
    print(num2)
    return num2


testB = A()
add(1,testB)