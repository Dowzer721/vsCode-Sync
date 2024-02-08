
from random import randint, sample

class Employee:
    def __init__(self, name_, rank_, contractedHours_, over18_=True):
        # self.ID = 0
        # self.NAME = name_
        # self.RANK = rank_

        self.INFORMATION = {
            "ID": 0,
            "NAME": name_,
            "RANK": rank_,
            "HOURS": contractedHours_,
            "MAXHOURS": int(contractedHours_ * 1.2) if over18_ else contractedHours_,
            "AVAILABILITY": [(randint(0,1), randint(0,1)) for _ in range(7)]
        }

        self.WEEKFITNESS = 0.0
    
    def calculateWeekFitness(self, employeeShiftsForWeek_):
        fitnessLevels = []
        
        hoursGivenForWeek = sum([sum(day) for day in employeeShiftsForWeek_]) * 8
        fitnessLevels.append(self.INFORMATION["HOURS"] / hoursGivenForWeek)

        if hoursGivenForWeek >= self.INFORMATION["MAXHOURS"]:
            fitnessLevels.append(1/abs(self.INFORMATION["MAXHOURS"] - hoursGivenForWeek))
        
        availabilityFitness = 0.0
        for i, day in enumerate(employeeShiftsForWeek_):
            availableForOpen = self.INFORMATION["AVAILABILITY"][i][0]
            availableForClose= self.INFORMATION["AVAILABILITY"][i][1]

            expectedForOpen = day[0]
            expectedForClose= day[1]

            availabilityFitness += int(availableForOpen == expectedForOpen)
            availabilityFitness += int(availableForClose == expectedForClose)
        availabilityFitness /= (7 * 2) # 7 days, 2 shifts each
        fitnessLevels.append(availabilityFitness)
        
        self.WEEKFITNESS = sum(fitnessLevels) / len(fitnessLevels)

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

def sortStaffByID(staff_):
    orderedStaff = []
    for i in range(len(staff_)):
        for E in staff_:
            if E.ID == i:
                orderedStaff.append(E)
                break
    return orderedStaff


# dayNames = "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday".split(',')
# for dayIndex, dayName in enumerate(dayNames):
#     staffCount = [3,3,3,4,5,6,5][dayIndex]
#     randomStaff = sortStaffByID( sample(STAFF, staffCount) )

#     randomHours = 0

randomHoursForWeek = [
    [(randint(0,1), randint(0,1)) 
     for _ in range(7)]
    for _ in range(len(STAFF))
]

weeklyFitness = 0.0
for E in STAFF:
    E.calculateWeekFitness(randomHoursForWeek[E.INFORMATION["ID"]])
    weeklyFitness += E.WEEKFITNESS

print(weeklyFitness/len(STAFF))

# print(randomHoursForWeek[0])
# print(STAFF[0].INFORMATION["AVAILABILITY"])

# STAFF[0].calculateWeekFitness(randomHoursForWeek[0])
# print(STAFF[0].WEEKFITNESS)

