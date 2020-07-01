class Animal():
    pass


    class Dog(Animal):

        def __init__(self, name):
            self.name = name


    class Cat(Animal):

        def __init__(self, name):
            self.name = name

    class Person():

        def __init__(self, name):
            self.name = name
            self.pet = None

    class Employee(Person):

        def __init__(self, name, salary):
            super(Employee, self).__init__(name)
            self.salary = salary

    class Fish():
        pass


    class Salmon(Fish):
        pass


    class Halibut(Fish):
        pass

    rover = Dog("Rover")
    satan = Cat('Satan')
    mary = Person('Mary')
    mery.pet = satan
    frank = Employee('Frank', 1200)
    frank.pet = rover
    flipper = Fish()
    salmon = Salmon()
    harry = Halibut()