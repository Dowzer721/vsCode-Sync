
from math import pi, cos, sin
from PIL import Image

imagePath = "C:/Users/Luke/Pictures/Mum Driving Photos/Jackie-0020.jpg"
image = Image.open(imagePath)

threshold = 0.1

imageSize = (300, 200)
image = image.resize(imageSize)
# # print(image)

# image = Image.new("RGB", imageSize)

# image.putpixel((1, 1), (255, 255, 255))
# image.putpixel((4, 7), (255, 255, 255))
# image.putpixel((3, 5), (255, 255, 255))
# image.putpixel((2, 3), (255, 255, 255))


pixelData = list(image.getdata())

def index(colRow):
    c, r = colRow
    return c + (r * imageSize[0])

def pixelBrightness(colours):
    return int(sum(colours) / (3*255) )

def neighbours(col, row, neighbourMultiplier=-1):
    neighbourPositions = [
        (col-1, row-1), (col, row-1), (col+1, row-1),
        (col-1, row), (col+1, row),
        (col-1, row+1), (col, row+1), (col+1, row+1)
    ]
    neighbourBrightnessValues = [
        pixelBrightness(pixelData[index(neighbourPositions[n])]) for n in range(8)
    ]
    return sum([value * neighbourMultiplier for value in neighbourBrightnessValues])


for i, (r, g, b) in enumerate(pixelData):
    # input(f"{i}: rgb:{r} {g} {b}")
    row = int(i / imageSize[0])
    col = i % imageSize[0]

    if row == 0 or row == imageSize[1]-1 or col == 0 or col == imageSize[0]-1:
        # image.putpixel((col, row), (255,0,0))
        continue

    

    currentBrightness = int( (r + g + b) / (3*255) * 8 )

    neighbourIndexes = [
        index((col-1, row-1)), index((col, row-1)), index((col+1, row-1)), 
        index((col-1, row)),                        index((col+1, row)), 
        index((col-1, row+1)), index((col, row+1)), index((col+1, row+1))
    ]
    
    neighbourBrightnessValues = [
        sum(pixelData[neighbourIndexes[n]]) / (3*255) * -1
        for n in range(8)
    ]

    # input( )
    totalBrightness = currentBrightness + sum(neighbourBrightnessValues)
    if totalBrightness >= threshold:
        image.putpixel((col, row), (255, 255, 255))
    else:
        image.putpixel((col, row), (0, 0, 0))

    # input(neighbourBrightnessValues)

    # currentValue = brightness * 8
    # neighbourValues = neighbours(col, row)
    # sum_ = currentValue + neighbourValues 
    # sum_ = brightness
    
    # image.putpixel((col, row), (sum_, sum_, sum_))

image.show()