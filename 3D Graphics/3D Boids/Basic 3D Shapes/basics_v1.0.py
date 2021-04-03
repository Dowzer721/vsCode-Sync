
"""
Although this file has a lot of lines (756), there are only actually 134 lines of code, which is 
approximately 17.72% of the file. The rest is comments and explanation! So go grab a cup of 
tea and get comfy!

Here's a video for you to watch before getting into this file.
It's obviously a piss take but it really hits home what it's like when trying to learn how to program!
https://youtu.be/_WH6cbwZ5m8?t=23

So I haven't explained the basics of Python in this file, but if you would like me to, I'd be 
more than happy to, as I'm pretty sure I could do quite easily, and with some sweeeeet analogies!
"""


def hoverYourMouseOverMe():
    """
    By using these triple quotes, it allows me to write large blocks of text as comments. 
    Multiple lines and formatted as I choose. What it also means is that when you hover over a method 
    which is being called in the code, all of the comment block will pop up in the description. 
    This means that you don't need to keep scrolling around if you forget what a method does; instead 
    just hover over it and it should pop up with a little window which you can scroll through and 
    interact with. I would still advise reading through it though on the first pass, just because 
    formatting and stuff won't neccessarily show correctly in the little window.

    As you can see, I've included this comment block inside a function, meaning you can hover your mouse 
    over Line 32 and you should get the pop up window that I was talking about. If your IDE doesn't have 
    this, don't worry too much as it won't be a massive concern. When I finish this file I will triple 
    check that every time I write "Line n" it is correct, so hopefully they will all link to the correct 
    places! :)
    """
hoverYourMouseOverMe()



""" 
I'm not using "import tkinter as tk" just to keep from getting confusing later on. 
All that does is mean instead of writing "tkinter." each time, you can write "tk.". 
But just to keep it easier to read, I am not using that. Feel free to change that if you would prefer.
"""
import tkinter

"""
# I'm using the maths library so as to make use of some basic geometric functions, 
# such as sine and cosine.
"""
import math

def mapRange(value, inputMin, inputMax, outputMin, outputMax):
    """
    This function allows me to pass in an input, along with the minimum and maximum the input could be, 
    then get the equivalent output between the minimum and maximum possible output.
    For example:
    mapRange(50, 0, 100, 250, 750) ==> 500
    mapRange(10, 0, 100, 0, 75) ==> 7.5
    mapRange(30, 10, 90, 5, 10) ==> 6.25
    mapRange(0.23, 0.1, 0.9, 12, 15) ==> 12.4875

    The maths here isn't too difficult, but the only real way to understand is to derive the equation 
    yourself on paper. It's quite difficult to explain here in text. Although I derived it myself, it is 
    a commonly known function and so if you search Google with "map range to another range", you'll get 
    the same result. 
    
    At the top of this linked page, is the mathematical equation of this function, and then after is the 
    function written in basically every programming language: https://rosettacode.org/wiki/Map_range
    """
    inputRange = inputMax - inputMin
    outputRange= outputMax - outputMin

    # a, b, c, d, e = value, inputMin, inputMax, outputMin, outputMax
    # return d + ((e-d)*((a-b)/(c-b)) )
    return outputMin + (outputRange * ((value - inputMin) / inputRange) )

# input(mapRange(25, 0, 100, 25, 255))

"""
The scale of the object. When there's only one object in the 3D space, distance and scale will do 
the exact same thing. Because whether you move the camera back and forward or just change the size 
of the object won't make a difference in terms of what you are seeing. However, as soon as there are 
more than one objects, that's when distance and scale will become independant. 
Distance will now move the camera in and out, essentially scaling each object equally, but then 
scale will scale each object individually.

Originally, these values were inside the engine class (Line 114), but I have moved them outside to make it 
easier to find and alter. What this does mean, however, is that if there were more than one objects in 
the scene, they will scale equally, essentially cancelling the scale out. 
Instead, you would want to change distance and scale for each object, so that how close their center's 
are to the camera and how big they are changes per object. But that's a task for you!
"""
xScale = 50
yScale = 50
zScale = 50



"""
I'm declaring an engine class which is basically the heart of the program, in that it provides 
'energy' to the rest of the program. You could think of it much the same as the engine on a train 
(the bit at the front that pulls everything else). 
Without the engine, the rest of the carriages of the train wouldn't be able to 'perform'. 
And so, without the engine of the program, the rest of the functions and code would be unable to 
perform correctly. Of course, this same program could be achieved without using a class, but it would 
likely become so messy and unreadable that debugging and expanding would be damn-near-impossible.

Also, the reason that I have called it "Engine" is because when game studios create games, they tend to 
use software colloquially named engines, as the following examples show. Although I know this isn't a 
video game, it is 3D graphics for software, so it made sense to me to call it "Engine". If you have a 
better name, feel free to change it, but of course, also change it anywhere else that it is mentioned. 
"Ctrl+F" is your best friend there.

https://en.wikipedia.org/wiki/Game_engine
https://en.wikipedia.org/wiki/List_of_game_engines
"""
class Engine:
    """
    This function ("__init__") is called automatically whenever a new object of type Engine is created, 
    for example: newEngine = Engine(*args)
    The first 3 arguments (self, points_, triangles_) are required, ie. they do not have an equals sign 
    beside them. The rest of the arguments do have an equals sign, which means if nothing is provided 
    for them, they will default to whatever value is on the other side of the equals sign. 
    Meaning if a width isn't provided, it will be set to 600, otherwise it'll be set to what is 
    provided. 
    This does not account for error checking though, so "banana" could be provided to "windowWidth_", 
    which obviously would cause a problem. Error checking and handling is something that you could do 
    later on. Here's a brief explanation of error handling in Python: https://docs.python.org/3/tutorial/errors.html#handling-exceptions
    However, I tend not to worry if I am writing the code for myself and don't plan on 
    having anyone else alter it, as you likely won't make that mistake yourself. And if you do, it 
    should be quite obvious to track down the issue anyway.
    Just as a small note, I use an underscore after an argument in a function or method, as it just 
    allows me to quickly see which variables are being passed into the function/method, and which are 
    being created inside. This is just a simple rule that I try to stick to, but sometimes I forget and 
    won't do it, so apologies if there are some arguments that don't have underscores where they should; 
    feel free to change them if you want to.
    """
    def __init__(self, points_, triangles_, windowWidth_ = 600, windowHeight_ = 400, distance_ = 6):
        """
        The first argument "self" is a reference to the current instance of the class. 
        This means that "self" is how an object of type Engine refers to the variables held within it. 
        As an analogy, if you had a contact list, with each contact being an object of class "contact", 
        then each detail inside a contact would be referred to by the contact as "self.something", 
        for example, "self.mobilePhoneNumber", "self.homePhoneNumber", "self.homeAddress" etc. etc.

        During this initialisation method, you are able to create new variables with the "self.", to be 
        used later on in the class. I do believe that you can also create new variables with the "self." 
        later on outside of this initialisation method, but I cannot see it being good practice, 
        as you may forget where it was declared and that may cause issues. 
        I just say, as a rule of thumb, that all "self." variable should be declared and initialised 
        within the initialisation method.
        """
        
        self.window = tkinter.Tk()
        """
        This quite simply is just setting the title of the window. 
        This format of "program name", "version", "author name and year" is just my own standard. 
        There are likely better standards to follow, but this is just how I do it.
        """
        self.window.title("Basic 3D Shapes - v1.0 - Luke Shears 2021")

        # Here I am creating a canvas to which I will draw to on top of the window
        self.canvas = tkinter.Canvas(self.window, width=windowWidth_, height=windowHeight_)
        
        self.canvas.pack()
        """
        If you are unsure as to what a function does, as I was with "pack()", you should be able to right 
        click the function name, and click "Go to Definition". This will open the library file which 
        contains the selected function, and if you scroll up a few lines, you'll see a big comment which 
        will hopefully provide you with some understanding of what the function is doing. 

        !!! Remember though, these functions have not been written for a beginner to understand, so don't 
        be disheartened if you don't understand it, because it hasn't been written to teach, but instead 
        to achieve some goal. !!! 

        If you do that "Go to Definition" on this function ("pack()"), it should redirect you into 
        tkinter, and then to Line 2391. Notice on this line that it says: 
        "pack = configure = config = pack_configure". 
        What this means is that any calls of the function "pack", "configure" or "config" will be 
        redirected to "pack_configure". Of course, every author of libraries is different, and they'll 
        have their own reasoning for this, but my guess is it's been done for backwards compatibility. 
        So if someone has written a program which at some point calls "config" but the author of tkinter 
        updates tkinter and removes "config", then the program in question won't work anymore. So to save 
        from that happening, they have linked the 4 functions together to call the same function. 
        But again, that is just my own guess, so take that with a pinch of salt.

        You can also, of course, just Google "[library name] [function name]" and you should also be 
        able to find some help on it ("tkinter pack").
        """

        """
        I attempted to put buttons into the window so that you could rotate the model easily, but I was 
        struggling with aligning the buttons. Although that isn't the most important thing, I actually 
        ended up implementing mouse control (Line 693), which is just easier to control. 
        I will, however, leave this code here incase you want to read it. I mean it works in terms of 
        adding buttons, and I am sure if I had continued I would have gotten it working, but honestly 
        I did the mouse stuff just to test the rotation was working and then prefered it so stuck with it.
        """
        #------------------------------------------------------------------------------------------------
        # self.buttonFrame = tkinter.Frame(self.window)
        # self.buttonFrame.pack(expand = "true")

        # self.rotateXPos = tkinter.Button(self.window, text="Rotate X Positive")
        # self.rotateXPos.pack()
        # self.rotateXPos.update()

        # self.rotateXNeg = tkinter.Button(self.window, text="Rotate X Negative")
        # self.rotateYPos = tkinter.Button(self.window, text="Rotate Y Positive")
        # self.rotateYNeg = tkinter.Button(self.window, text="Rotate Y Negative")
        # self.rotateZPos = tkinter.Button(self.window, text="Rotate Z Positive")
        # self.rotateZNeg = tkinter.Button(self.window, text="Rotate Z Negative")
        
        # self.rotateXPos.place(x = (windowWidth_ / 2) - (self.rotateXPos.winfo_width() / 2), y = 0)
        # self.rotateXNeg.pack(side = "left")
        # self.rotateYPos.pack(side = "top")
        # self.rotateYNeg.pack(side = "bottom")
        # self.rotateZPos.pack(side = "bottom")
        # self.rotateZNeg.pack(side = "top")
        #------------------------------------------------------------------------------------------------


        # The width and height of the window.
        self.width = windowWidth_
        self.height = windowHeight_

        # The distance from the "camera" to the object.
        self.distance = distance_

        
        """
        I'm not going to explain these here, but instead later on when they are being used. 
        For now, I will just say that "self.points" will contain a list of (x,y,z) points, and 
        "self.triangles" will contain a list of points to link. This will make more sense later on, 
        when I explain it further.
        """
        self.points = points_
        self.triangles = triangles_
        self.shapes = []
    
    def project3DPointTo2D(self, point_):
        """
        Because this program is working in 3-dimensions, but can only display in 2-dimensions 
        (because the computer screen only has a width and height), there needs to be a method to project 
        the coordinates from 3D to 2D. This is what the following code does.
        You can read more on how this works here: https://en.wikipedia.org/wiki/3D_projection, but here 
        are the two equations that we are concerned with:
        
        Using the following:
        o = (x, y, z) # Original 3D point ("o" is for original)
        p = (x, y)    # Projected 2D point ("p" is for projected)
        middleX = (xMax - xMin) / 2.0 # (self.width / 2.0)
        middleY = (ymax - yMin) / 2.0 # (self.height/ 2.0)
        distance= (zMax - zMin) # (self.distance)
        scale = a scaling factor (number) # self.scale
        
        The equation is:
        p_x = middleX + ((o_x * distance) / (o_z + distance)) * scale
        p_y = middleY + ((o_y * distance) / (o_z + distance)) * scale

        The axis of 3D space should also be noted here, as sometimes they are different depending on 
        application. So the following axis is what this program is using (Ctrl+Click should open link):
        https://bobcad.com/wp-content/uploads/2019/05/image-1-right-hand-rule.png
        """

        (x, y, z) = (point_[0], point_[1], point_[2])

        middleX = self.width / 2.0
        middleY = self.height/ 2.0

        projectedX = int( middleX + ((x * self.distance) / (z + self.distance)) * xScale )
        projectedY = int( middleY + ((y * self.distance) / (z + self.distance)) * yScale )

        """
        Notice that I convert the whole equation to an integer. This is because technically there are no 
        floating point locations on a screen, only whole integers. You may already understand this, so 
        feel free to skip past (Line 297), but I'm going to draw a little diagram in ASCII:
        
        Let's say this is your unbelievable low resolution screen (7x5 wow). 
        Well if you were to calculate the locations of a load of points in a circle around the centre 
        (3,2), you'd use this equation (just for x): x = 3 + (cos(angle) * radius).
        But cos(angle) can only return a floating point number between -1.0 and 1.0, which no matter what 
        the radius is you multiply by, you're inevitably not going to be guaranteed to get a whole integer 
        every time. And without a whole number, there is nowhere to point to on the screen, because for 
        example; (4.2, 1.3) doesn't exist as a location, and therefore there would be an error. 
        This link: http://math.hws.edu/graphicsbook/c2/s1.html explains it a hell of a lot better than I 
        can. If the link doesn't take you there, it's section "2.1.1 Pixel Coordinates".
        But maybe my ASCII drawing of the low-res screen might help with explanation; I don't know!
        #     0   1   2   3   4   5   6
        #   +---+---+---+---+---+---+---+
        # 0 |   |   |   | O |   |   |   |
        #   +---+---+---+---+---+---+---+
        # 1 |   |   | O |   | O |   |   |
        #   +---+---+---+---+---+---+---+
        # 2 |   | O |   |   |   | O |   |
        #   +---+---+---+---+---+---+---+
        # 3 |   |   | O |   | O |   |   |
        #   +---+---+---+---+---+---+---+
        # 4 |   |   |   | O |   |   |   |
        #   +---+---+---+---+---+---+---+
        """


        return (projectedX, projectedY)
    
    def createTriangleFromPoints(self, points_):
        """
        Usually, a graphics program will draw it's graphics using a series of triangles. 
        This linked answer explains why that is much better than I can: https://gamedev.stackexchange.com/a/9513
        I believe the gist of it is that all 3 points of a triangle are always in the same plane, 
        and so therefore can be used to join any 3 points, and so using many of them can in turn be 
        used to create a plane in any direction and of any size.
        """

        """
        Here is a perfect example of readability over efficiency. Obviously, when you are learning, the 
        following code is neither helpful or easy to understand, and so the code which is actually being 
        used after this comment is better for learning. However, this chunk of code will achieve the same, 
        but will also be considerably more efficient, both in time and also memory allocation. 
        
        self.shapes.append(
            self.canvas.create_polygon(
                sum([list(point) for point in points], []), fill="", outline="black"
            )
        )
        
        Don't get too involved in the previous code here, as it is just an example of how you might 
        improve this program later on. If at some point you want it explained let me know.
        """

        pointA, pointB, pointC = points_[0], points_[1], points_[2]
        pointCoordinates = [
            pointA[0], pointA[1], #pointA: x, y
            pointB[0], pointB[1], #pointB: x, y
            pointC[0], pointC[1]  #pointC: x, y
        ]
        """
        This "create_polygon" method is outside my understanding. I mean I understand what it is 
        returning, but my goodness if you right click it and "Go to Definition", good luck! 
        I have tried to follow the path to the source of where it creates the shape, but honestly, 
        I gave up, because it certainly has NOT been written to be easy to understand!
        Although "fill" and "outline" are pretty self-explanatory.
        """
        newTriangle = self.canvas.create_polygon(pointCoordinates, fill="", outline="black")
    
        """
        Here is "self.shapes", declared on Line 235. When I create the list of triangles to pass into 
        this Engine class, I will finally explain what is going on with them.
        """
        self.shapes.append(newTriangle)
    
    def rotateShape(self, rotationAroundXAxis = 0.0, rotationAroundYAxis = 0.0, rotationAroundZAxis = 0.0):
        """
        This function will rotate the shape around the 3 axis, specified by the rotation angles provided.
        The angles are in radians (-2.0 * Pi ==> 2.0 * Pi)

        The maths here are not my own, and are quite confusing if you are not well versed in matrix 
        multiplication, so don't worry too much about the maths here. 
        Remember, I've written this program to help with code, not maths!

        If you reeeallllly want to read up where this comes from and how it is derived.... here you go:
        https://en.wikipedia.org/wiki/Rotation_matrix#General_rotations
        """


        """
        Some debugging here. This is a perfect example of why you are taught to print to the console when you first start learning. 
        This method was not receiving the correct values, and so was causing the rotation to go mental. 
        Instead of ranging from -3.14 ==> 3.14, it was instead going from 0 ==> 4000. I wasn't sure what 
        was causing it, so I printed out the values here so that I could monitor them in the terminal 
        easily. This helped greatly to track down the problem, and that shows because that problem 
        no longer exists.
        """
        # print(f"x: {round(rotationAroundXAxis,3)}, y: {round(rotationAroundYAxis,3)}, z: {round(rotationAroundZAxis,3)}")

        def multiplyMatrices(matrixA, matrixB):
            """
            This function will multiply "matrixA" by "matrixB". I am not going to explain it, because it 
            is matrix maths, and that's not the point of this program. I'll link where I got the 
            understanding of how to loop through etc. Warning; it is NOT written for tutorial purposes!
            
            Oh, and just as a note, at this link there is a symbol that looks like a pointy E. 
            This is Sigma. I'm pretty sure we used it in Electronics, for Inverting Op-Amps, so you may 
            already know it, but it is just used to signify the sum of. 
            The statement underneath "k=1" is saying "here's a variable 'k', and initially set it to 1. 
            Then the number on top "n", says that 'k' must count up by one until it equals 'n'.
            https://en.wikipedia.org/wiki/Matrix_multiplication#Definition
            
            I also have NOT written the code to be readable, as I wanted to just crank it out as I knew it 
            wasn't going to be something that I was going to explain anyway. If you do want me to rewrite it, 
            or explain it properly, let me know and I will sort it out. 
            I wrote it all myself so it won't be a problemo :) 
            """
            # A = m*n, B = n*p
            # A: m=rows, n=cols, 
            # B: n=rows, p=cols
            m = len(matrixA)
            An = len(matrixA[0])

            Bn = len(matrixB)
            p = len(matrixB[0])

            # Number of columns must equal number of rows:
            if not (An == Bn):
                print(f"An({An}) != Bn({Bn})")
                return
            
            n = An
            
            """
            If you are reading this comment, then all I'll say is good luck with the next bit!
            Again, I wrote this not to teach, but to get the job done. So it works, and it is 
            efficient and quite elegant, but my goodness is it difficult to read!
            """
            
            # matrixC:
            return [
                [
                    sum(
                        [matrixA[i][k] * matrixB[k][j] for k in range(n)]
                    )
                    for j in range(p)
                ]
                for i in range(m)
            ]

        # I have written some explanation here, but just not hugely in depth because 
        # I didn't feel it was particularly necessary. 

        # The reason for this notation is just because this is the standard form that I am used to. 
        # If it's easier to understand, do a Find-and-Replace-All for "alpha", "beta" and "gamma" and 
        # replace with "rotationAroundZAxis", "rotationAroundYAxis" and "rotationAroundXAxis", 
        # and then comment out the following three lines:
        alpha = rotationAroundZAxis
        beta  = rotationAroundYAxis
        gamma = rotationAroundXAxis

        # Declaring them here to speed up the process so they don't have to be recalculated 
        # every time during the "rotationMatrix" creation.
        cA = math.cos(alpha)
        cB = math.cos(beta)
        cG = math.cos(gamma)
        sA = math.sin(alpha)
        sB = math.sin(beta)
        sG = math.sin(gamma)

        # This equation has been derived from the Wikipedia page linked at Line 358, 
        # but don't worry about it too much.
        rotationMatrix = [
            [cA * cB, (cA * sB * sG) - (sA * cG), (cA * sB * cG) + (sA * sG)],
            [sA * cB, (sA * sB * sG) + (cA * cG), (sA * sB * cG) - (cA * sG)],
            [-sB, cB * sG, cB * cG]
        ]

        # Creating an empty array to store the newly rotated points into, aptly named "rotatedPoints".
        rotatedPoints = []
        for point in self.points:
            startX, startY, startZ = point[0], point[1], point[2]
            
            # The reason this is a 2D matrix, but with only one row is because it needs to be 2D to 
            # multiply with the rotation matrix.
            pointMatrix = [[startX, startY, startZ]]
            
            # multiplyMatrices returns a list, but the rest of the class expected that "self.points" 
            # will be in tuple form, so we convert.
            rotatedPoint = tuple(multiplyMatrices(pointMatrix, rotationMatrix)[0])
            
            rotatedPoints.append(rotatedPoint)
        
        # Once all the points have been rotated, we simply swap out the old points for the newly 
        # rotated ones
        self.points = rotatedPoints


    def render(self):
        """
        If we don't delete("all"), the canvas doesn't clear, and so you just end up drawing over what 
        was already there. Meaning the canvas has a shape drawn to it, then each time it redraws the 
        shape again over the top. 
        Analogy: Drawing a full page image with pencil on paper, and then not erasing the image before 
        restarting. 
        """
        self.canvas.delete("all")
        
        
        """
        Now comes the time to render the 3D shape that we've been building up to.

        When a new object is created, of class Engine, it receives a list of points and triangles. 
        Points is a list of tuples containing 3D coordinates, as they would be located in real-3D space. 
        Triangles however, is a list of tuples which each point to a location in the list of points. 
        For example (drawing a flat square on the x-z axis (see Line 506-526 for axis)):

        Using unit measurements (-1 ==> 0 ==> 1). These units could then be multiplied by a scale factor 
        and the shape would scale accordingly.
        points = [
            (-1, 0, -1),    # Far left corner
            (1, 0, -1),     # Far right corner
            (1, 0, 1),      # Close right corner
            (-1, 0, 1)      # Close left corner
        ]

        Then triangles, to create the square from two triangles:
        triangles = [
            (3, 0, 1), # (Close left, far left, far right)
            (3, 2, 1)  # (Close left, close right, far right)
        ]

        The following diagram should hopefully explain this better. 
        The axis are drawn with:
        x: _
        y: | 
        z: .
        While the square is drawn with: 
        x: --- 
        z: + 
        Then the four corners of the square are labeled with numbers:

                        +y
                        |          .
                        |        .
                    0   |      .      1
                    +---|----.--------+
                  +     |  .        +
        ________+_______|.________+_____+x
              +        .|       +
            +        .  |     +
          +--------.--------+
          3      .      |   2
               .+z      |


        """

        # Store all of the coordinates in a list:
        allTriangleCornerCoordinates = []

        # Each point is made of 3D coordinates (x, y, z), but we can only display in 2D (x, y), 
        # so we have to project each point from 3D to 2D:
        for point3D in self.points:
            point2D = self.project3DPointTo2D(point3D) # Projection

            # Then we "append" or "add-to-end" of the list
            allTriangleCornerCoordinates.append(point2D)

        # I don't feel like this needs any more explanation, other than what is on Line 499. 
        # If you disagree, and want more explanation, let me know.
        for triangleIndices in self.triangles:
            thisTriangleCornerCoordinates = (
                allTriangleCornerCoordinates[triangleIndices[0]],
                allTriangleCornerCoordinates[triangleIndices[1]],
                allTriangleCornerCoordinates[triangleIndices[2]]
            )
            self.createTriangleFromPoints(thisTriangleCornerCoordinates)


"""
Now we are outside of the "Engine" class, and so are going to declare some variables, and then create 
a new object of class "Engine", and then render the shape. I will attempt to make an interesting shape, 
or something that might be of interest to you, but if it turns out as just something boring, 
then it was probably that I got fed up with this tedious part of trying to geo-locate the 3D space.

Okay I'm leaving this block of text here because it's kind of funny, because lo and behold, it is a 
boring shape! Haha there is probably an easier way to import 3D models into a program like this, instead 
of trying to manually do it. 
I attempted to model a really basic resistor, and that was too confusing. It was literally just a 
cylinder with two wires poking out of either end, and as you will see..... It did not happen!
"""


"""
I am using unit coordinates here, meaning: 
    -1 is as far negative as possible
     0 is right in the middle
    +1 is as far positive as possible

This isn't neccesarily required but I think it is easier to understand and use in practice. 
After these have been set in unit form, they are then scaled (Line 590) according to the 
x,y,z scale (Line 90).
"""
points = [
    #              The letters here are explained at Line 599:
    (-1,  1, -1), # LTB
    ( 1,  1, -1), # RTB
    ( 1,  1,  1), # RTF
    (-1,  1,  1), # LTF

    (-1, -1, -1), # LBB
    ( 1, -1, -1), # RBB
    ( 1, -1,  1), # RBF
    (-1, -1,  1)  # LBF
]

# Now we scale the points according to the x,y,z scale factors:
for point in points:
    scaledX = point[0] * xScale
    scaledY = point[1] * yScale
    scaledZ = point[2] * zScale
    point = (scaledX, scaledY, scaledZ)

LTB, RTB, RTF, LTF, LBB, RBB, RBF, LBF = range(0, 8)
"""
The letters equate to the following:
(L/R)(T/B)(F/B)
L/R : Left / Right : -x / +x
T/B : Top / Bottom : +y / -y
F/B : Front / Back : +z / -z

And writing them out with commas and then the equals is called Unpacking (Line 597). 
Basically what is happening is that "range(0, 8)" returns a list of integers, from 0 ==> (8-1). 
So we can write out a load of variables, and assign them all to the result of the range function. 
It is exactly the same as writing them each out, but is just a quicker way of doing it. 
There are also other reasons for using packing and unpacking, but in this instance, this is why I am 
using it; to write cleaner code.
For example:
range(0, 3) ==> [0, 1, 2]

So you could write:
a, b, c = range(0, 3)

And then:
a ==> 0, b ==> 1, c ==> 2

I hope this makes sense. It's actually something I've only learnt about recently, so if you don't get it, 
don't dwell on it, just ignore and use the standard way of declaring variables:
LTB = 0
RTB = 1
RTF = 2
LTF = 3
LBB = 4
RBB = 5
RBF = 6
LBF = 7

Using these three-letter variables should make it easier to reference each point in the triangle creation.
Originally, when I was writing this code, I had this:
triangles = [
    # Create the top square from two triangles:
    (3, 0, 1), # Neither 3, 0 or 1 are intuitive to represent a direction
    (3, 2, 1), 
    ...
]

But now, I can simply write:
triangles = [
    # Create the top square from two triangles:
    (LTF, LTB, RTB), # This is much more intuitive; Left Top Front, Left Top Back, Right Top Back
    (LTF, RTF, RTB)  # Left Top Front, Right Top Front, Right Top Back
]

At least in my visual mind it makes more sense to be able to reference a point in 3D space according to 
directions from the camera, instead of just some integers which are dimensionless.
"""

triangles = [
    # Create the top square from two triangles:
    (LTF, LTB, RTB),
    (LTF, RTF, RTB),

    # Create the bottom square:
    (LBF, LBB, RBB),
    (LBF, RBF, RBB),

    # # Create the front face:
    (LTF, RTF, RBF),
    (LTF, LBF, RBF),

    # Create the back face:
    (LTB, LBB, RBB),
    (LTB, RTB, RBB),

    # Create the left face:
    (LTB, LBB, LBF),
    (LTB, LTF, LBF),

    # Create the right face:
    (RTB, RBB, RBF),
    (RTB, RTF, RBF)
]

engineObject = Engine(points, triangles)

"""
The window has to be updated before the width and height will be correct. 
I am not actually sure why this is, but I don't feel that it's too important for understanding. 
I'll suggest not getting stuck on this, but that's up to you! ;)
"""
engineObject.window.update()
windowWidth = engineObject.window.winfo_width()
windowHeight= engineObject.window.winfo_height()

# I call this once here just so that the shape is drawn before the mouse event is fired, 
# so that the shape can be seen before it is rotated by the mouse.
engineObject.render()

# This event gets fired every time the mouse moves, and the event argument receives the mouse position. 
def mouseMotionFunction(event):

    # I can't really explain this line any better than it explains itself
    mouseX, mouseY = event.x, event.y
    
    # The x,y rotations here are being multiplied by 0.01 just to calm down the rotations 
    # when the mouse is moved. This is just an arbitrary value found through testing. 
    # There is probably some smart way to calculate a suitable value for this, such as by using 
    # the x,y,z scales to decide how fast the shape can rotate. But that is not important here 
    # so I have just set them to working values.
    xRotation = mapRange(mouseY, 0, windowHeight, math.pi * -0.01, math.pi * 0.01)
    yRotation = mapRange(mouseX, 0, windowWidth, math.pi * -0.01, math.pi * 0.01)

    # Every time the shape has been rotated, it needs to be redrawn to the screen otherwise 
    # you won't see that rotation.
    engineObject.rotateShape(xRotation, yRotation)
    engineObject.render()


"""
Every element of the user interface is known as a widget.
An event is something which happens to application, such as the user pressing a key 
or moving the mouse.

Each widget has it's own build in events, which can be called, but it is also possible 
to attach a custom event (function) to a widget. This is done with the "bind()" method. 

Here is the some documentation I could find for the "bind()" method. It isn't very
exhaustive though, so hopefully my explanation + this link will help enough:
https://docs.python.org/3/library/tkinter.html?#bindings-and-events
 
"""
engineObject.window.bind('<Motion>', mouseMotionFunction)


"""
So this linked answer to the question "What is mainloop()" really goes into some detail, 
and gives an alternate block of code for using instead of it:
https://stackoverflow.com/a/29158947

The main takeaway I think is that "mainloop()" blocks the process, meaning once called, 
any code after it will never execute, and therefore that is why it is placed at the end of the program. 
But what happens if you want the "main loop" to run and run, but then at some point stop so something 
else can happen, and then restart again? Well as the answer I've linked explains; with this code:

loopRunning = True
while loopRunning:
    # [Do all looping code]
    # [Some method of breaking out of this infinite loop]

    tk.update_idletasks()
    tk.update()

This acheives the same as calling "mainloop()", but as far as I can garner, calling "mainloop()"
assumes that you never want any code after it to run. No matter where it is in the program, be it 
at the start, the end, or in some kind of conditional loop (for, while), it will halt all 
proceedings and hold the program at that line. This won't crash the program, because it isn't doing 
anything wrong technically, but if you put it mid-way through your program, it would render the 
rest of your code void. 
"""
engineObject.window.mainloop()


# ------------------------------------------------------------------------------------------------------
"""
I don't honestly see why you would want this, but the following is the exact same file, just without 
any comments and explanation; purely raw code:

import tkinter
import math

def mapRange(value, inputMin, inputMax, outputMin, outputMax):
    inputRange = inputMax - inputMin
    outputRange= outputMax - outputMin
	return outputMin + (outputRange * ((value - inputMin) / inputRange) )

xScale = 50
yScale = 50
zScale = 50

class Engine:
    def __init__(self, points_, triangles_, windowWidth_ = 600, windowHeight_ = 400, distance_ = 6):
        self.window = tkinter.Tk()
        self.window.title("Basic 3D Shapes - v1.0 - Luke Shears 2021")
		self.canvas = tkinter.Canvas(self.window, width=windowWidth_, height=windowHeight_)
        self.canvas.pack()
        self.width = windowWidth_
        self.height = windowHeight_
		self.distance = distance_
		self.points = points_
        self.triangles = triangles_
        self.shapes = []

    def project3DPointTo2D(self, point_):
        (x, y, z) = (point_[0], point_[1], point_[2])
		middleX = self.width / 2.0
        middleY = self.height/ 2.0
        projectedX = int( middleX + ((x * self.distance) / (z + self.distance)) * xScale )
        projectedY = int( middleY + ((y * self.distance) / (z + self.distance)) * yScale )
		return (projectedX, projectedY)

    def createTriangleFromPoints(self, points_):
        pointA, pointB, pointC = points_[0], points_[1], points_[2]
        pointCoordinates = [
            pointA[0], pointA[1], #pointA: x, y
            pointB[0], pointB[1], #pointB: x, y
            pointC[0], pointC[1]  #pointC: x, y
        ]
        newTriangle = self.canvas.create_polygon(pointCoordinates, fill="", outline="black")
		self.shapes.append(newTriangle)

    def rotateShape(self, rotationAroundXAxis = 0.0, rotationAroundYAxis = 0.0, rotationAroundZAxis = 0.0):
        def multiplyMatrices(matrixA, matrixB):
            m = len(matrixA)
            An = len(matrixA[0])
			Bn = len(matrixB)
            p = len(matrixB[0])
			if not (An == Bn):
                print(f"An({An}) != Bn({Bn})")
                return
            n = An
            return [
                [
                    sum(
                        [matrixA[i][k] * matrixB[k][j] for k in range(n)]
                    )
                    for j in range(p)
                ]
                for i in range(m)
            ]

        alpha = rotationAroundZAxis
        beta  = rotationAroundYAxis
        gamma = rotationAroundXAxis
        cA = math.cos(alpha)
        cB = math.cos(beta)
        cG = math.cos(gamma)
        sA = math.sin(alpha)
        sB = math.sin(beta)
        sG = math.sin(gamma)
        rotationMatrix = [
            [cA * cB, (cA * sB * sG) - (sA * cG), (cA * sB * cG) + (sA * sG)],
            [sA * cB, (sA * sB * sG) + (cA * cG), (sA * sB * cG) - (cA * sG)],
            [-sB, cB * sG, cB * cG]
        ]
        rotatedPoints = []
        for point in self.points:
            startX, startY, startZ = point[0], point[1], point[2]
            pointMatrix = [[startX, startY, startZ]]
            rotatedPoint = tuple(multiplyMatrices(pointMatrix, rotationMatrix)[0])
            rotatedPoints.append(rotatedPoint)
        self.points = rotatedPoints

    def render(self):
        self.canvas.delete("all")
        allTriangleCornerCoordinates = []
        for point3D in self.points:
            point2D = self.project3DPointTo2D(point3D)
            allTriangleCornerCoordinates.append(point2D)
        for triangleIndices in self.triangles:
            thisTriangleCornerCoordinates = (
                allTriangleCornerCoordinates[triangleIndices[0]],
                allTriangleCornerCoordinates[triangleIndices[1]],
                allTriangleCornerCoordinates[triangleIndices[2]]
            )
            self.createTriangleFromPoints(thisTriangleCornerCoordinates)

points = [
    (-1,  1, -1),
    ( 1,  1, -1),
    ( 1,  1,  1),
    (-1,  1,  1),
    (-1, -1, -1),
    ( 1, -1, -1),
    ( 1, -1,  1),
    (-1, -1,  1)
]
for point in points:
    scaledX = point[0] * xScale
    scaledY = point[1] * yScale
    scaledZ = point[2] * zScale
    point = (scaledX, scaledY, scaledZ)

LTB, RTB, RTF, LTF, LBB, RBB, RBF, LBF = range(0, 8)
triangles = [
    (LTF, LTB, RTB),
    (LTF, RTF, RTB),
	(LBF, LBB, RBB),
    (LBF, RBF, RBB),
	(LTF, RTF, RBF),
    (LTF, LBF, RBF),
	(LTB, LBB, RBB),
    (LTB, RTB, RBB),
	(LTB, LBB, LBF),
    (LTB, LTF, LBF),
	(RTB, RBB, RBF),
    (RTB, RTF, RBF)
]
engineObject = Engine(points, triangles)
engineObject.window.update()
windowWidth = engineObject.window.winfo_width()
windowHeight= engineObject.window.winfo_height()
engineObject.render()

def mouseMotionFunction(event):
	mouseX, mouseY = event.x, event.y
    xRotation = mapRange(mouseX, 0, windowWidth, math.pi * -0.01, math.pi * 0.01)
    yRotation = mapRange(mouseY, 0, windowHeight, math.pi * -0.01, math.pi * 0.01)
    engineObject.rotateShape(xRotation, yRotation)
    engineObject.render()
engineObject.window.bind('<Motion>', mouseMotionFunction)

engineObject.window.mainloop()

"""