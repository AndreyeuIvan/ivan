'''Creating my own game with a plot, of how to become a python_programmer'''
from sys import exit
from random import randint


class Programmer:

    def enter(self):
        print('Let"s start programming')
        exit(1)

class Work:

    def __init__(self, programmer_experience):
        self.programmer_experience = programmer_experience

    def change(self):
        current_role = self.programmer_experience.opening_role()
        last_role = self.programmer_experience.next_role('senior')

        while current_role != last_role:
            next_role_name = current_role.enter()
            current_role = self.programmer_experience.next_role(next_role_name)

        current_role.enter()


class Intern(Programmer):

    def enter(self):
        print('Hello! Young fellow.')

        action = input(
            '''Answer a following questions: 
            if you write this?
            what will be the output?  '''
            )

        if action == 'Zen of Python':
            return 'junior'


class Junior(Programmer):

    def enter(self):
        print('Keep up')

        action = input('Enter your favorite freamwork: ')

        if action == 'Django':
            return 'middle'


class Middle(Programmer):

    def enter(self):
        print('Great Job')
        return 'middle'


class Senior(Programmer):


    def enter(self):
        super().enter('Junior')
        return 'senior'


class Experience:

    roles = {
        'intern': Intern(),
        'junior': Junior(),
        'middle': Middle(),
        'senior': Senior(),
    }

    def __init__(self, start_role):
        self.start_role = start_role

    def next_role(self, role):
        val = Experience.roles.get(role)
        return val

    def opening_role(self):
        return self.next_role(self.start_role)

class Fail(Programmer):
    quips = [
        'Please try again',
        'Keep hard working'
    ]

    def enter(self):
        print(Fail.quips[randint(0, len(self.quips) -1)])
        exit(1)


a_role = Experience('intern')
a_change_work = Work(a_role)
a_change_work.change()
