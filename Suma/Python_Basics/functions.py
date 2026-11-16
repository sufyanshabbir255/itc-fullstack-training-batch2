#reusing the code
def name():
    print("positive")
name()
def add():
    a=8
    b=9
    print(a+b)
add()

#with parameters
def mul(a,b):
    print("result:",a*b)
mul(2,34) 

def sub(c,d):
    print("result:",d-c)
sub(22,8)    


#employee salary
def salary(basic,bonus):
    total=basic+bonus
    return total
result=salary(20000,400)
print("total salary:",result)