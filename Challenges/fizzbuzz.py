
divisionsToCheck = [
    3,
    5
]

outputsForDivisions = [
    'Fizz',
    'Buzz'
]

if (len(divisionsToCheck) != len(outputsForDivisions)):
    input(
        "Length of 'divisionsToCheck' does not equal length of 'outputsForDivisions' (%dx%d)" 
        %(
            len(divisionsToCheck), 
            len(outputsForDivisions)
        )
    )
    


# for i in range(1, maxNumber+1):
for i in range(1, int(input("Maximum value: "))+1 ):

    divisions = [
        int(i % divisionsToCheck[div] == 0) for div in range(len(divisionsToCheck))
    ]

    outputString = ""
    for div in range(len(divisionsToCheck)):
        outputString += outputsForDivisions[div] * divisions[div]
    
    outputString += str(i) * (sum(divisions) == 0)
    
    print(outputString)

    
#     fizz = int(i % 3 == 0)
#     buzz = int(i % 5 == 0)
#     print(f"{'Fizz'*fizz}{'Buzz'*buzz}{str(i)*(1-fizz)*(1-buzz)}")

#     print(f"{'Fizz'*int(i%3==0)} {'Buzz'*int(i%5==0)} {str(i) * (1-int(i%3==0)) * (1-int(i%5==0))} ")
    # print(f"{'Fizz' * int(i%3==0)}{'Buzz' * int(i%5==0)}{str(i) * (int(i%3>0)) * (int(i%5>0))} ")