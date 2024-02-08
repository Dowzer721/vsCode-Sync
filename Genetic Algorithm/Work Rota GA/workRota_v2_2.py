
from random import randint, sample

possibleRanks = "H,SS,JS,SL,L,P,KP".split(',')
# print(possibleRanks)

class Employee:
    def __init__(self, name_, rank_, contractedHours_, over18_=True):
        self.ID = 0
        self.NAME = name_
        self.RANK = rank_
        self.HOURS= contractedHours_
        self.OVER18 = over18_

        self.MAXHOURS = int(contractedHours_ * 1.75)
        self.morningShiftLength = 17 - 10
        self.eveningShiftLength = 24 - 17

        if not over18_:
            self.MAXHOURS = contractedHours_
            self.morningShiftLength = 17 - 12
            self.eveningShiftLength = 22 - 17
        
        if rank_ in possibleRanks[:4]:
            # print(f"{self.RANK}")
            self.morningShiftLength = 17 - 7
            # self.eveningShiftLength = 24 - 17
        
        self.weeklyProvidedHours = [0 for _ in range(7)]
        self.satisfaction = 0
    def calculateSatisfaction(self):
        totalProvidedHours = sum(self.weeklyProvidedHours)
        dMinHours = totalProvidedHours - self.HOURS
        dMaxHours = totalProvidedHours - self.MAXHOURS
        self.satisfaction = -round(dMaxHours / dMinHours, 2)


STAFF = [
    Employee("Enka", "H", 48),
    
    Employee("Iain", "SS", 45),
    Employee("Peter", "SS", 45),
    
    Employee("Josh", "JS", 45),
    
    Employee("Luke", "L", 30),
    # Employee("Seb", "L", 30),
    # Employee("Grey", "L", 20),
    # Employee("Jack", "L", 20),
    # Employee("Skye", "L", 20),

    # Employee("Isaac FW", "P", 30),
    
    # Employee("Bill", "KP", 30),
    # Employee("Isaac", "KP", 30),
    # Employee("Oscar", "KP", 30),
    # Employee("Jake", "KP", 20),
    # Employee("Louis", "KP", 20, over18_=False),

    Employee("Test!Test!Test", "H", 30),
]
longestStaffNameCount = 0
for i in range(len(STAFF)):
    STAFF[i].ID = i
    longestStaffNameCount = max(longestStaffNameCount, len(STAFF[i].NAME))
for E in STAFF:
    E.NAME = E.NAME + (' ' * (longestStaffNameCount - len(E.NAME)))



dayNames = "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday".split(',')

# staffTotalHours = [0 for _ in range(len(STAFF))]

for dayIndex, dayName in enumerate(dayNames):
    print(dayName)
    randomStaffCount = randint(4, len(STAFF))
    randomStaff = sample(STAFF, randomStaffCount)
    randomStaffIDs = [E.ID for E in randomStaff]
    randomStaffIDs.sort()

    for ID in randomStaffIDs:
        randomShifts = (randint(0, 1), randint(0, 1))
        randomHours = (randomShifts[0] * STAFF[ID].morningShiftLength) + (randomShifts[1] * STAFF[ID].eveningShiftLength)
        # staffTotalHours[ID] += randomHours
        STAFF[ID].weeklyProvidedHours[dayIndex] = randomHours
        # print(f"{E.NAME}: {randomShifts} = {randomHours}h")
    # print()

# staffTotalHours[-1] = (STAFF[-1].HOURS + STAFF[-1].MAXHOURS) / 2
# STAFF[-1].weeklyProvidedHours = [0 for _ in range(6)] + [(STAFF[-1].HOURS + STAFF[-1].MAXHOURS) / 2]

staffSatisfaction = []

for E in STAFF:
    # E = STAFF[ID]
    
    providedHours = sum(E.weeklyProvidedHours)
    withinHours = (providedHours > E.HOURS) and (providedHours < E.MAXHOURS)

    # satisfaction = 0
    # if withinHours:
    dMinHours = providedHours - E.HOURS
    dMaxHours = providedHours - E.MAXHOURS
    satisfaction = -round(dMaxHours / dMinHours, 2)
    staffSatisfaction.append(satisfaction)

minSatisfaction = min(staffSatisfaction)

for i in range(len(STAFF)):
    staffSatisfaction[i] -= minSatisfaction

for E in STAFF:
    # E = STAFF[ID]

    # M = 1
    # satisfaction = (2 * M * int(withinHours)) - M
    # dHours = (staffTotalHours[ID] - E.HOURS)
    # if dHours != 0:
    #     satisfaction += 10 / dHours

    E.calculateSatisfaction()
    providedHours = sum(E.weeklyProvidedHours)
    dMinHours = providedHours - E.HOURS
    dMaxHours = providedHours - E.MAXHOURS

    print(
        f"{E.NAME}:\t" + 
        f"{E.HOURS}>" + 
        f"{providedHours}>" + 
        f"{E.MAXHOURS}:\t" +
        f"{(dMinHours, dMaxHours)}\t" +
        f"{E.satisfaction}"
    )