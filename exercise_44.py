class Parent():

    def override(self):
        print('Parent override()')

class Child(Parent):
    pass
    #def override(self):
        #print('Child override()')

dad = Parent()
son = Child()

dad.override()
son.override()

class Parent():

    def altered(self):
        print('Parent altered()')

class Child(Parent):
    
    def altered(self):
        print('Child altered before')
        super(Child, self).altered()
        print('Child altered after')

dad = Parent()
son = Child()

dad.altered()
son.altered()
print('*'*50)
class Other():

    def override(self):
        print('Other override()')

    def implicit(self):
        print('Other implicit()')

    def altered(self):
        print('Other altered()')

class Child():

    def __init__(self):
        self.other = Other()

    def implicit(self):
        self.other.implicit()

    def override(self):
        print('Child override()')

    def altered(self):
        print('child, before other altered()')
        self.other.altered()
        print('Child, alter other altered()')

son = Child()
son.implicit()
son.override()
son.altered()
