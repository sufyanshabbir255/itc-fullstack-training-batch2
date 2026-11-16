class Car():
    def __init__(self,make, model):
        self.make = make
        self.model = model

    def driving(self):
        print("this car is driving")

    def stopping(self):
        print("The car has stopped")

car_1 = Car("Kia","Sportage")

print(car_1.make)
print(car_1.model)

car_1.driving()
car_1.stopping()