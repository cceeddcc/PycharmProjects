class NumBox :
    def __new__(cls, *args, **kwargs):
        if len(args) <1 :
            return None
        else :
            return super(NumBox, cls).__new__(cls)

    def __init__(self, num=None) :
        self.num = num

    def __repr__(self):
        return str(self.num)

a =NumBox()
type(a)

b = NumBox(10)
type(b)

class StrBox :
    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return "A('{}')".format(self.string)

    def __bytes__(self):
        return str.encode(self.string)

    def __format__(self, format):
        if format == "this-sting" :
            return "This string : {}".format(self.string)
        return self.string

a = StrBox("Life is short")
a

repr(a)

import time