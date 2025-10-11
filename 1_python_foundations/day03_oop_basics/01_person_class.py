class Person:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"Hi, I'm {self.name} and I am {self.age} years old.")

person = Person("Alex",22)
person.greet()

