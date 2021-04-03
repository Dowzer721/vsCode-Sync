
import math
"""
"math" is a library, containing classes and functions which can be used for mathematical operations. 
For example, instead of writing a function to calculate the sine of an angle, using say the Taylor series, 
one can just call sin(x) and have the calculation done automatically. This file is not supposed to be a 
maths tutorial, but if you fancy learning about the Taylor series, here is a link: 
https://en.wikipedia.org/wiki/Sine#Series_definition
"""

# So instead of having the following function, you can just write sin(x):
def taylorSeries_Sin(x, nMax=10):
    def factorial(value):
        # 3! = 6
        # 5! = 120
        # 7! = 5040

        fact = 1
        for i in range(1, value + 1):
            fact *= i
        return fact


    # sin(x) = x - (x^3)/3! + (x^5)/5! - (x^7)/7! + (x^9)/9! - ...
    seriesSum = 0.0
    for n in range(1, nMax):
        try:
            addOrMinus = (int(n % 2 == 1) * 2) - 1

            equationPowerValue = (n * 2) - 1 

            equationSegment = (x**equationPowerValue) / factorial(equationPowerValue)
            
            seriesSum += addOrMinus * equationSegment
        except:
            print(f"Second argument too large, stopping at {n}")
            break
        
    
    return seriesSum

# So, to demonstrate, you could call this:
Pi = 3.141592654
angle = 0.5 * Pi
taylorSin = taylorSeries_Sin(angle)
print(f"Taylor Series Calculation: {taylorSin}")

# Or just:

mathSin = math.sin(0.5 * math.pi)
print(f"math.sin: {mathSin}")

"""
If you run this, you will see that the terminal prints this:
>>> Taylor Series Calculation: 1.0000000000000435
>>> math.sin: 1.0

0.5 * Pi is an angle pointing straight down. 
We would expect that the y component of this would be +1.0, and although you could round, 
you can see that the second output is the correct one. 

There is also the issue of efficiency to consider. 
Using the built-in timer of Visual Studio Code, I timed the two function calls. 
The self-written function "taylorSeries_Sin" took 0.00011 seconds, 
whereas "math.sin" took 0.0 seconds; so quick that the program couldn't even time it.

I think these two examples are enough to demonstrate why it is often preferable to use 
libraries instead of writing the code manually. Libraries will often have been written by 
professionals, and so will be built for both efficiency and accuracy, unlike the code you 
write yourself which may not satisfy either. 
"""