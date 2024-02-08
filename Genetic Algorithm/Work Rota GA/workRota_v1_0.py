
"""
I am happy with the progress I have made here, however there are some key features I want to implement/fix:

TODO:   Implement the actual GA. 
        This file only has the building blocks for the Class and the creation of a random week. 
        Although this is important, the point in this system is to use a GA to develop a week, 
        instead of just doing it manually and mathematically.

TODO:   Implementing actual hours into the system and allowing for hours to be allocated throughout the day. 
        I think what I will do is use a list containing the hours available each day (0700 -> 2400) to allow 
        the system to allocate staff into the available hours, to avoid unwanted crossover (for example 
        having 2 KP's working when only 1 is required).

TODO:   Implement a better system for specifying days which people are unavailable (H- / NA). 
        The current system is not particularly user friendly or easily readable. 
        Perhaps it could be a good idea to allow the user to specify specific days to take off, 
        using the actual name of the day, instead of the index (starting from 0, as that's confusing).

________

FIXME:  Making variable names more understandable.
        They are confusing and don't always make sense in context. 
        For example, "rankIndex" and "ruleIndex". Those names do not give much information as to what they are. 
        It may be wise to use snake_case and have more descriptive variable names, 
        or perhaps use comments above the lines where I am declaring variables. 
        I think the latter is probably my prefered fix.
"""




import random


availableRanks = {
    "H": "Head Chef",
    "SS": "Senior Sous Chef",
    "JS": "Junior Sous Chef",
    "L": "Line Chef",
    "KP": "Kitchen Porter",
    #"TEST": "TEST RANK"
}

class Employee:
    def __init__(self, name_, rank_, contractedHours_, over18_=True, maximumhoursMultiplier_=1.2):
        # UPPERCASE = FIXED
        # camelCase = NOT-FIXED

        self.ID = 0
        self.NAME = name_
        self.RANK = rank_
        self.CONTRACTEDHOURS = contractedHours_
        self.OVER18 = over18_
        self.MAXIMUMHOURS = int(contractedHours_ * maximumhoursMultiplier_) if over18_ else contractedHours_



        self.WEEKLY_AVAILABILITY = []
        self.resetAvailability()

        self.FULLRANK = availableRanks[rank_]
    
    def resetAvailability(self):
        self.WEEKLY_AVAILABILITY = [True for _ in range(7)]
    
    def updateAvailability(self, daysUnavailable_):
        for day in daysUnavailable_:
            self.WEEKLY_AVAILABILITY[day] = False
    
    
STAFF = [
    Employee("Enka", "H", 48),
    Employee("Test", "H", 30, maximumhoursMultiplier_=1.7),

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

# for E in STAFF:
#     print(
#         f"Staff Name: {E.NAME}, \t" +
#         f"Rank: {E.fullRank} \t" + 
#         f"Hours: {E.CONTRACTEDHOURS}" +
#         "")


def updateAvailability(staffName_, daysUnavailable_):
    _staffMember = next((E for E in STAFF if E.NAME == staffName_), False)
    if _staffMember: 
        _staffMember.updateAvailability(daysUnavailable_)
    else:
        # raise Exception(f"{staffName_} not in STAFF")
        input((f"{staffName_} not in STAFF. (ENTER to continue)"))



updateAvailability("Enka",          [1, 2, 3] )
updateAvailability("Iain",          [0, 1, 2, 3, 4, 5, 6] )
updateAvailability("Oscar",         [2, 3, 4, 5, 6] )
updateAvailability("Louis",         [0, 1, 2, 3, 4, 5, 6] )
updateAvailability("Archie",        [0, 1, 6] )
updateAvailability("Josh",          [2, 3, 4] ) # Made up for testing
# updateAvailability("NOT_IN_STAFF",  [0, 1, 6] )

# n = "Enka"
# print(f"{n} week availability:", next((E for E in STAFF if E.NAME == n), 0).WEEKLY_AVAILABILITY)

# How many days per week each rank needs to be present in the kitchen.
# Separate ranks by commas if they are interchangeable.
weeklyStaffRules = {
    "H": 2,
    "SS,JS": 7,
    "L": 7,
    "KP": 7
}

rankHourIncreases = {
    "H":    10,
    "SS":   9,
    "JS":   9,
    "L":    8,
    "KP":   8
}

randomDayOrder = [i for i in range(7)] 
random.shuffle(randomDayOrder)
print(randomDayOrder)

staffHours = [0 for _ in range(len(STAFF))]

randomWeek = []
for day in randomDayOrder:
    totalRankDays = [randomWeek.count(rank) for rank in availableRanks.keys()]
    # print(totalRankDays)
    
    personAvailableToday = []
    rankAvailableToday = []

    for E in STAFF:
        if E.WEEKLY_AVAILABILITY[day]: 
            personAvailableToday.append(E)
        
            rankIndex = list(availableRanks).index(E.RANK)
            ruleIndex = [i for i in range(len(weeklyStaffRules)) if E.RANK in list(weeklyStaffRules)[i]][0]
            # print(ruleIndex)
            if totalRankDays[rankIndex] < list(weeklyStaffRules.values())[ruleIndex]:
                rankAvailableToday.append(E)
    
    # print(day)
    # print([E.NAME for E in personAvailableToday])
    # print([E.RANK for E in rankAvailableToday])

    randomChosenStaff = []
    for rank in list(availableRanks):
        if not (rank in [E.RANK for E in rankAvailableToday]): continue
        # input(rank)
        
        staffWithRank = [E for E in personAvailableToday if E.RANK == rank]
        if len(staffWithRank) == 0: continue

        for E in staffWithRank:
            if (staffHours[E.ID] + rankHourIncreases[E.RANK]) > E.MAXIMUMHOURS:
                staffWithRank.remove(E)

        randomStaffMember = random.sample(staffWithRank, min(len(staffWithRank), 3))
        # input(randomStaffMember)
        randomChosenStaff.extend(randomStaffMember)
    
    # print(randomChosenStaff)
    # print([E.NAME for E in randomChosenStaff])

    for E in randomChosenStaff:
        staffHours[E.ID] += rankHourIncreases[E.RANK]

    # staffChosenForToday = []
    # for E in randomChosenStaff:
    #     staffChosenForToday.append(E)
    # randomWeek.append(staffChosenForToday)
    randomWeek.append(randomChosenStaff)
    
    
    # input()

    dailyHours = []

for dayStaff in randomWeek:
    print([E.NAME for E in dayStaff])