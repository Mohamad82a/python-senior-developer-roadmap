class Vehicle:
    def move(self):
        print("Vehicle moving on")

class Car(Vehicle):

    def move(self):
        print(f'Car moving on')


car = Car()
car.move()