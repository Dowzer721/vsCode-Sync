
"""
In version 1.x, I was deciding who was available in the week, who wanted hours etc before beginning to choose the random week. 
This isn't really the point of a GA. 

Instead I am going to generate a totally random week, then go through each employee and have them each decide how 'happy' they are with 
the week, depending on their requirements. 

Then from this I can work out the 'fitness' of the generated week, and begin comparing it to other random weeks and actually start GA-ing.
"""

import random

class Employee:
    def __init__(self, name_, rank_, contractedHours_, acceptedClopenCount_=2, over18_=True):
        self.ID = 0
        self.NAME = name_
        self.RANK = rank_
        self.HOURS= contractedHours_
        self.MAXHOURS = int(contractedHours_ * 1.2) if over18_ else contractedHours_
        # if not over18_: self.MAXHOURS = contractedHours_
        self.CLOPEN = acceptedClopenCount_
        self.OVER18 = over18_

        self.AVAILABILITY = [
            (random.randint(0, 1), random.randint(0, 1))
            for _ in range(7)
        ]
    
    def setAvailability(self, day_, availability_):
        if type(day_) != int: raise Exception(f"Incorrect type of day_: ({type(day_)})")
        if len(availability_) != 2: raise Exception(f"Availability length not 2: ({len(availability_)})")

        self.AVAILABILITY[day_] = availability_
    
    def evaluateWeek(self, week_):
        happinessWithWeek = 0.0
        for day in week_:
            pass

STAFF = [
    Employee("Enka", "H", 48),
    #Employee("Test", "H", 30),

    Employee("Iain", "SS", 45),
    Employee("Peter", "SS", 45),
    
    Employee("Josh", "JS", 45),
    
    Employee("Archie", "L", 20),
    Employee("Grey", "L", 20),
    Employee("Jack", "L", 20),
    Employee("Luke", "L", 30),
    Employee("Seb", "L", 30),
    Employee("Skye", "L", 20),
    
    Employee("Bill", "KP", 30),
    Employee("Isaac FW", "KP", 30),
    Employee("Isaac", "KP", 30),
    Employee("Jake", "KP", 20),
    Employee("Louis", "KP", 20, over18_=False),
    Employee("Oscar", "KP", 30),
]
for i in range(len(STAFF)):
    STAFF[i].ID = i



def crossover(week1, week2):
    newWeek = []
    for day in range(7):
        if random.randint(0, 100) <= 50:pass


# exampleWeek = {
#     "Monday":  {"Enka": [1, 1], "Peter":[0,1], "Grey":[1,0], "Luke":[1,0], "Bill":[1,0], "Oscar":[0,1]},
#     "Tuesday": {"Enka": [0, 1], "Josh":[1,0], "Isaac FW":[1,0], "Skye":[0,1], "Louis":[1,0], "Oscar":[0,1]}
# }

# for day in exampleWeek.keys():
#     print(day)
#     for staffName in exampleWeek[day].keys():
#         shifts = exampleWeek[day][staffName]
#         hours = sum([8 * shift for shift in shifts])-1
#         print(f"{staffName} : {shifts}={hours}")
#     print()

dayNames = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
staffNames = [E.NAME for E in STAFF]
# print(staffNames)

# for dayIndex, day in enumerate(dayNames):
#     # print(f"{dayIndex}: {day}")
#     staffCount = random.randint(4, 10)
#     randomStaff = random.sample(staffNames, staffCount)
#     for Employee in randomStaff:
        
#     print(f"{day}: Staff x{staffCount}:- {randomStaff}")

def sortStaffByID(staff_):
    orderedStaff = []
    
    for i in range(len(staff_)):
        for E in staff_:
            if E.ID == i:
                orderedStaff.append(E)
                break
    return orderedStaff


for dayIndex, dayName in enumerate(dayNames):
    print(dayName)
    staffCount = random.randint(4, 10)
    randomStaff = sortStaffByID( random.sample(STAFF, staffCount) )

    randomHours = [
        (random.randint(0, 1), random.randint(0, 1))
        for _ in range(7)
    ]

    for i, E in enumerate(randomStaff):
        hoursValid = True

        availability = E.AVAILABILITY[dayIndex]

        hours = randomHours[dayIndex]

        if availability != hours: hoursValid = False

        print(f"{E.NAME}: Available:{availability}, Hours:{hours}, Valid:{hoursValid}")
    print()

