'''
Created on 2016-4-15

@author: Administrator
'''
class Person:
    """测试不同对象的相互性"""
    num=0
    def __init__(self,name):#可被调用
        self.n=name
        self.num+=1
    def delname(self):
        self.num-=1
a=Person('aaaaaa')
print(a.n)
print(a.num)

a.__init__('bbbbbb')
a.delname()
print(a.num)

b=Person('ccccc')
print(b.n)
print(b.num)
print(Person.num)