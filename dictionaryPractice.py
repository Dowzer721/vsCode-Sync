
"""
This don't work and I don't know why...
"""


import random

database = []

class DataEntry:
    def __init__(self, name_, age_, mobilePhoneNumber_ = -1):
        self.data = {
            "name": name_,
            "age": age_,
            "mobile": mobilePhoneNumber_
        }
    
    def printData(self):
        print(f"Name: {self.data[0]}, Age: {self.data[1]}, Mobile Phone: {self.data[2]}")

for _ in range(10):
    nameLength = random.randint(5, 10)
    newName = str([chr(random.randint(0, 26)) for _ in range(nameLength)] )
    newAge = random.randint(12, 30)
    newMobile = str([random.randint(0, 9) for _ in range(11)])

    newEntry = DataEntry(newName, newAge, newMobile)
    database.append(newEntry)


for entry in database:
    entry.printData()