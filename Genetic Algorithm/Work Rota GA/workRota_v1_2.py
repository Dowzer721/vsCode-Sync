
import random

class Employee:
    def __init__(self, name_, rank_, contractedHours_, over18_=True):
        self.ID = 0

        self.NAME = name_
        self.RANK = rank_
        self.CONTRACTEDHOURS = contractedHours_

        self.MAXIMUMHOURS = int(contractedHours_ * 1.2) if over18_ else contractedHours_

        self.DAYS_AVAILABLE_THIS_WEEK = [True for _ in range(7)]

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

randomDayOrder = [i for i in range(7)]
random.shuffle(randomDayOrder)
# print(randomDayOrder)

for day in randomDayOrder:
    staffAvailableToday = [E for E in STAFF if E.DAYS_AVAILABLE_THIS_WEEK[day]]

    staffWhoCan = {
        "Cook": [E for E in staffAvailableToday if (E.RANK in ["H", "SS", "JS", "SL"])],
        "Prep": [E for E in staffAvailableToday if (E.RANK in ["H", "SS", "JS", "SL", "L", "P"])],
        "Line": [E for E in staffAvailableToday if (E.RANK in ["H", "SS", "JS", "SL", "L"])],
        # "KP":   [E for E in staffAvailableToday if (E.RANK in ["H", "SS", "JS", "SL", "L", "P", "KP"])]
        "KP": staffAvailableToday,
    }

    cookChef = random.choice(staffWhoCan["Cook"])
    prepChefs= random.sample(staffWhoCan["Prep"], 2)
    lineChefs= random.sample([E for E in staffAvailableToday if (E in staffWhoCan["Line"]) and (E not in prepChefs)], 3)
    kp       = random.choice(staffWhoCan["KP"])

    print(
        f"{day}. Cook:{cookChef.NAME} \t" + 
        f"Prep:{', '.join([P.NAME for P in prepChefs])} \t" + 
        f"Line:{', '.join([L.NAME for L in lineChefs])} \t" +
        f"KP:{kp.NAME}"
    )
    
    