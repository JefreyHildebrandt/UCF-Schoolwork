import random
from collections import deque

class BarberSchedule:
    def __init__(self, barbers, services, dollarDifference):
        self.barbers = barbers
        self.services = services
        self.dollarDifference = dollarDifference

    def start(self):
        print("d =",self.dollarDifference)
        print("Total Services:",len(self.services),"Services:")
        count = 1
        for service in self.services:
            if count % 12 != 0:
                print(service," ",end="")
            else:
                print(service)
            count += 1
        print()
        print("Barber order:")
        self.printBarbers()
        while not self.nextRound():
            self.printBarbers()
        self.printBarbers()

    def nextRound(self):
        highest = 0
        for i in range(len(self.barbers)):
            self.barbers[i].earnings += self.services.popleft()
            if self.barbers[i].earnings > self.barbers[highest].earnings:
                highest = i
            elif self.barbers[i].earnings + self.dollarDifference <= self.barbers[highest].earnings:
                self.barbers.insert(highest, self.barbers.pop(i))
            if len(self.services) <= 0:
                return True

    def printBarbers(self):
        for barber in self.barbers:
            print(barber.name,",",barber.earnings," ", end="")
        print()

class Barber:
    def __init__(self, name):
        self.earnings = 0
        self.name = name

def main():
    barbers = [Barber("A"), Barber("B"), Barber("C"), Barber("D"), Barber("E")]
    services = deque([])
    servicePrices = [10, 20, 30, 40]
    for x in range(random.randint(0, 100)):
        services.append(servicePrices[random.randint(0, 3)])
    random.shuffle(barbers)
    dollarDifference = servicePrices[random.randint(0, 3)]
    barberSchedule = BarberSchedule(barbers, services, dollarDifference)
    barberSchedule.start()

main()