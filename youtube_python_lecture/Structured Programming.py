# variable scope
"""
global vs local varibles
"""

def Mymethod() :
    my_var = "Local"
    print(my_var)

Mymethod()
print(my_var) # local var


def Mymethod() :
    global my_var
    my_var = "Local"
    print(my_var)

Mymethod()
print(my_var) # global var
