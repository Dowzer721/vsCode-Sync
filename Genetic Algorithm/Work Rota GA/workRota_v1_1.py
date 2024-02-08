"""
TODO:   Implement the actual GA. 
        This file only has the building blocks for the Class and the creation of a random week. 
        Although this is important, the point in this system is to use a GA to develop a week, 
        instead of just doing it manually and mathematically.

TODO:   Implementing actual hours into the system and allowing for hours to be allocated throughout the day. 
        I think what I will do is use a list containing the hours available each day (0700 -> 2400) to allow 
        the system to allocate staff into the available hours, to avoid unwanted crossover (for example 
        having 2 KP's working when only 1 is required).

TODO:   __________COMPLETE__________
        Implement a better system for specifying days which people are unavailable (H- / NA). 
        The current system is not particularly user friendly or easily readable. 
        Perhaps it could be a good idea to allow the user to specify specific days to take off, 
        using the actual name of the day, instead of the index (starting from 0, as that's confusing).


________

FIXME:  __________COMPLETE__________
        Making variable names more understandable.
        They are confusing and don't always make sense in context. 
        For example, "rankIndex" and "ruleIndex". Those names do not give much information as to what they are. 
        It may be wise to use snake_case and have more descriptive variable names, 
        or perhaps use comments above the lines where I am declaring variables. 
        I think the latter is probably my prefered fix.
"""

import random

fullRankNames = {
    "H":    "Head Chef",
    "SS":   "Senior Sous Chef",
    "JS":   "Junior Sous Chef",
    "SL":   "Senior Line Chef",
    "L":    "Line Chef",
    "KP":   "Kitchen Porter"
}

dayNames = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

hoursInWorkingDay = []

class Employee:
    def __init__(self, name_, rank_, contractedHours_, over18_=True):
        self.ID = 0
        self.NAME = name_
        self.RANK = rank_
        self.OVER18 = over18_

        self.CONTRACTED_HOURS = contractedHours_
        self.MAXIMUM_HOURS = int(contractedHours_ * 1.37) if over18_ else contractedHours_

        self.AVAILABILITY_THIS_WEEK = []
        self.resetAvailability()

        # Under 18 Hours:
        self.dailyAvailableHours = [1 for _ in range(22-7 +1)] + [0, 0]

        # Over 18's can work past 10pm:
        if over18_:
            self.dailyAvailableHours = self.dailyAvailableHours[:-2] + [1, 1]

        # Non managers and non-KP's don't need to start before 9am:
        if not (rank_ in ["H", "SS", "JS", "SL", "KP"]):
            self.dailyAvailableHours = [0, 0] + self.dailyAvailableHours[2:]
        
        self.IS_MANAGER = bool(rank_ in ["H", "SS", "JS", "SL"])
        
        # self.dailyAvailableHours = [1 for _ in range(24-7+1)]
        # if not (rank_ in ["H", "SS", "JS", "SL"]): 
        #     self.dailyAvailableHours
        # if not over18_:
        #     self.dailyAvailableHours = [0, 0, 0] + [1 for _ in range(22-10+1)] + [0, 0]
        



    def resetAvailability(self):
        self.AVAILABILITY_THIS_WEEK = [True for _ in range(7)]
    
    def setAvailability(self, daysUnavailable_):
        for day in daysUnavailable_:
            if type(day) == type(int):
                self.AVAILABILITY_THIS_WEEK[day] = False
            if type(day) == str:
                self.AVAILABILITY_THIS_WEEK[dayNames.index(day)] = False
    
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
    Employee("Isaac", "KP", 30),
    Employee("Jake", "KP", 20),
    Employee("Louis", "KP", 20, False),
    Employee("Oscar", "KP", 30),
]
for i in range(len(STAFF)):
    STAFF[i].ID = i

def getEmployeeByName(employeeName_):
    _employee = [E for E in STAFF if E.NAME == employeeName_]
    if len(_employee)==1: 
        return _employee[0]

    raise Exception(f"'{employeeName_}' not in staff.")
    


def setAvailability(employeeName_, daysUnavailable_):
    _employee = getEmployeeByName(employeeName_)

    _employee.setAvailability(daysUnavailable_)

def printEmployee(employeeName_):
    _employee = getEmployeeByName(employeeName_)

    startTime = 7 + _employee.dailyAvailableHours.index(1)
    backwardsHours = _employee.dailyAvailableHours
    backwardsHours.reverse()
    endTime = 24 - backwardsHours.index(1)

    print(
        #f"ID:\t{_employee.ID}\n" + 
        f"NAME:\t{_employee.NAME}\n" + 
        f"RANK:\t{fullRankNames[_employee.RANK]}\n" +
        f"HOURS:\t{_employee.CONTRACTED_HOURS} -> {_employee.MAXIMUM_HOURS}\n" +
        f"WEEK:\t{_employee.AVAILABILITY_THIS_WEEK}\n" +
        f"START:\t0{startTime}:00\n" +
        f"END:\t{endTime}:00\n"
    )

setAvailability("Enka",          ["Tuesday", "Wednesday", "Thursday"] )
setAvailability("Iain",          [0, 1, 2, 3, 4, 5, 6] )
setAvailability("Oscar",         [2, 3, 4, 5, 6] )
setAvailability("Louis",         [0, 1, 2, 3, 4, 5, 6] )
setAvailability("Archie",        [0, 1, 6] )
setAvailability("Josh",          [2, 3, 4] ) # Made up for testing
# setAvailability("NOT_IN_STAFF",  [0, 1, 6] )

# printEmployee("Enka")
# printEmployee("Luke")
# printEmployee("Louis")

hoursOccupiedByRank = [0 for _ in range(len(fullRankNames))]

randomDayOrder = [i for i in range(7)]
random.shuffle(randomDayOrder)

chosenStaffForWeek = [[] for _ in range(7)]
for day in randomDayOrder:

    staffAvailableToday = [E for E in STAFF if E.AVAILABILITY_THIS_WEEK[day]]

    managersAvailableToday = [E for E in staffAvailableToday if E.IS_MANAGER]
    kpsAvailableToday = [E for E in staffAvailableToday if E.RANK == "KP"]
    linesAvailableToday = [E for E in staffAvailableToday if E.RANK == "L"]
    
    morningManager = random.choice(managersAvailableToday)
    morningKP = random.choice(kpsAvailableToday)

    closingManager = random.choice(managersAvailableToday)
    closingKP = random.choice(kpsAvailableToday)
    
    prepChefCount = 1
    if day >= 5: prepChefCount = 2
    prepChefs = random.sample([E for E in STAFF if E.RANK == "L"], prepChefCount)

    morningGrillChef = random.choice(linesAvailableToday)
    morningBainChef = random.choice(linesAvailableToday)

    chosenStaffForWeek[day].append(morningManager.NAME)
    chosenStaffForWeek[day].append(morningKP.NAME)
    chosenStaffForWeek[day].extend([chef.NAME for chef in prepChefs])
    chosenStaffForWeek[day].append(morningGrillChef.NAME)
    chosenStaffForWeek[day].append(morningBainChef.NAME)
    chosenStaffForWeek[day].append(closingManager.NAME)
    chosenStaffForWeek[day].append(closingKP.NAME)

    # print(f"Day: {dayNames[day]}\tCook: {morningManager.NAME}\tKP: {morningKP.NAME}\tPrep: {', '.join([chef.NAME for chef in prepChefs])}")

for day in range(7):
    morningManager = chosenStaffForWeek[day][0]
    morningKP = chosenStaffForWeek[day][1]
    prepChefCount = 2 if day >= 5 else 1
    prepChefs = chosenStaffForWeek[day][2:2+prepChefCount]
    morningGrillChef = chosenStaffForWeek[day][2+prepChefCount +1]
    morningBainChef = chosenStaffForWeek[day][2+prepChefCount +2]
    print(
        f" {dayNames[day]}:" + 
        f"\tCook: {morningManager}" + 
        f"\tKP (Morning): {morningKP}" + 
        f"\tPrep: {', '.join(prepChefs)}" + 
        f"\tGrill: {morningGrillChef}" + 
        f"\tBain: {morningBainChef}" +
        f""
    )