class Car:
    wheels = 4

    def __init__(self, model):
        self.model = model

    def drive(self):
        print(f"{self.model} is driving")

my_car = Car("Tesla")
my_car.drive()