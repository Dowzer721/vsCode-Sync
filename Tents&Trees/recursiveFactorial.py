
def factorial(value):
    if value == 1: return 1
    return value * factorial(value - 1)

TotalSpaces = 5
Tents = 2
Spaces = TotalSpaces - Tents

Perms = factorial(Tents + Spaces) / (factorial(Tents) * factorial(Spaces))
print(Perms)

permStrings = []
counter = 2
while len(permStrings) < Perms:
    binaryString = str(bin(counter))[2:]
    binaryString = ('0'*(TotalSpaces-len(binaryString))) + binaryString
    if binaryString.count('1') == Tents:
        permStrings.append((binaryString, counter))
    # input(binaryString)
    counter += 1

print(permStrings)