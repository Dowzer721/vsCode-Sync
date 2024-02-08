
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
PURPLE = (200, 0, 200)

canvasW, canvasH = 600, 400
canvas = pygame.display.set_mode((canvasW, canvasH))

circleLocation = [
    (int(canvasW * 0.4), int(canvasH * 0.8)),
    (0, 0)
]

circleRadius = [
    min(circleLocation[0]),
    1
]

def solveQuadratic(a, b, c):
    # print(a,b,c)
    bSquared = b ** 2
    fourac = 4 * a * c
    root = (bSquared - fourac) ** 0.5
    twoa = 2 * a

    return [
        (-b + root) / twoa,
        (-b - root) / twoa
    ]

    # return (
    #     (-b + ((b**2) - 4*a*c)**0.5) / 2*a,
    #     (-b - ((b**2) - 4*a*c)**0.5) / 2*a
    # )

def calculateIntersections(location1, location2, radius1, radius2):
    
    ax, ay = location1
    bx, by = location2
    aR, bR = radius1, radius2
    
    
    aEquation = [1, 1, ax * -2, ay * -2, (ax**2) + (ay**2), aR**2]
    bEquation = [1, 1, bx * -2, by * -2, (bx**2) + (by**2), bR**2]

    
    b_minus_a = [bEquation[i] - aEquation[i] for i in range(6)]

    if b_minus_a[2] == 0: 
        b_minus_a[2] = 1
    
    b_minus_a[5] -= b_minus_a[4]
    b_minus_a[4] = 0

    b_minus_a[3] /= b_minus_a[2]
    b_minus_a[5] /= b_minus_a[2]
    b_minus_a[2] = 1
    

    aSubstitute_x = [
        b_minus_a[3] ** 2, b_minus_a[5] * -b_minus_a[3] * 2, b_minus_a[5] ** 2,
        0, aEquation[2] * -b_minus_a[3], aEquation[2] * b_minus_a[5]
    ]

    yQuadratic = [
        aSubstitute_x[0] + 1, 
        aSubstitute_x[1] + aSubstitute_x[4] + aEquation[3],
        aSubstitute_x[2] + aSubstitute_x[5] + aEquation[4] - aEquation[5]
    ]

    yPositions = solveQuadratic(yQuadratic[0], yQuadratic[1], yQuadratic[2])

    xPositions = [
        b_minus_a[5] - (b_minus_a[3] * yPositions[0]),
        b_minus_a[5] - (b_minus_a[3] * yPositions[1])
    ]

    # print(aEquation)

    # print(bEquation)
    # print(b_minus_a)

    # print(f"{b_minus_a[5]} - {b_minus_a[3]}y")

    # print(aSubstitute_x)

    # print(yQuadratic)

    # print(yPositions)
    # print(xPositions)

    if complex in [
        type(xPositions[0]), type(xPositions[1]),
        type(yPositions[0]), type(yPositions[1])
    ]: return False


    return [
        (int(xPositions[0]), int(yPositions[0])),
        (int(xPositions[1]), int(yPositions[1])),
    ]


while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        
        if ev.type == pygame.MOUSEMOTION:
            newX, newY = pygame.mouse.get_pos()
            radiusX = min(max(1, newX), canvasW - newX)
            radiusY = min(max(1, newY), canvasH - newY)
            
            circleLocation[1] = (newX, newY)
            circleRadius[1] = min(radiusX, radiusY)
        
        if ev.type == pygame.MOUSEBUTTONUP:
            circleLocation[0] = circleLocation[1]
            circleRadius[0] = circleRadius[1]
        
    canvas.fill(WHITE)
    
    circleDx = circleLocation[0][0] - circleLocation[1][0]
    circleDy = circleLocation[0][1] - circleLocation[1][1]
    circleDist = ((circleDx**2) + (circleDy**2)) ** 0.5
    if circleDist < sum(circleRadius):
        iP = calculateIntersections(circleLocation[0], circleLocation[1], circleRadius[0], circleRadius[1])
        if iP:
            pygame.draw.circle(canvas, BLACK, iP[0], 4, 0)
            pygame.draw.circle(canvas, BLACK, iP[1], 4, 0)
            # pygame.draw.line(canvas, BLACK, iP[0], iP[1], 1)
            # pygame.draw.line(canvas, BLACK, iP[0], circleLocation[0], 1)
            # pygame.draw.line(canvas, BLACK, iP[0], circleLocation[1], 1)
            # pygame.draw.line(canvas, BLACK, iP[1], circleLocation[0], 1)
            # pygame.draw.line(canvas, BLACK, iP[1], circleLocation[1], 1)

    

    pygame.draw.circle(canvas, BLACK, circleLocation[0], circleRadius[0], 1)
    pygame.draw.circle(canvas, BLACK, circleLocation[1], circleRadius[1], 1)
    
    pygame.display.update()