import json
from copy import deepcopy

def classToDict(obj):
    obj = deepcopy(obj)
    if isinstance(obj, list):
        return [classToDict(i) for i in obj]
    elif isinstance(obj, dict):
        return {i: classToDict(obj[i]) for i in obj}
    elif isinstance(obj, tuple):
        return tuple(classToDict(i) for i in obj)
    elif isinstance(obj, set):
        return set(classToDict(i) for i in obj)
    else: # base type or class
        try:
            hilf = vars(obj)
        except: # base type
            return obj
        else: # class
            for i in hilf:
                hilf[i] = classToDict(hilf[i])
            return hilf

class A:
    def __init__(self):
        self.xa = "AAA"
        
class B:
    def __init__(self):
        self.xb = [A()]
        self.xc = {"c": A()}

z = B()
print(classToDict(z))