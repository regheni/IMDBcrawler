class Parent:
    """docstring for Parent"""

    def __init__(self, age=10):
        super(Parent, self).__init__()
        self.age = age

    def get_age(self):
        return self.age


class Child(Parent):
    def get_age(self):
        age = super().get_age()
        return age - 5


parent = Parent()
print(parent.get_age())
child = Child()

print(child.get_age())
