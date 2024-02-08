
password = "SUPERsecretPASSWORD"

userInput = "-"
while userInput != "":
    userInput = input("Enter python code: ")
    try:
        eval(userInput)
    except:
        print("Invalid input...")