
"""
I think instead of starting at the base, and then creating a new segment with the previous segment 
as it's parent, I want to start at the end of the Tentacle, and then create the next one towards 
the base as the parent of the previous. 

So the current tentacle will know it's parent segment, but not it's child segment. 
This should allow each segment to move, then update it's parent, but not allow it to 
move then affect it's child.

"""

from math import pi, cos, sin, atan2

import pygame
canvasW, canvasH = 600, 400
canvas = pygame.display.set_mode((canvasW, canvasH))
base = (canvasW//2, canvasH)

segmentCount = 3
# segmentLength = int(canvasH / (segmentCount * 1.5)) # 35

# class Segment:
#     def __init__(self, id_ = None):
        
#         self.ID = id_
        
#         self.start = base
#         # If there is a parent, set the start to the parent's end, otherwise leave it at the base.
#         if parent_ != None:
#             self.start = parent_.end

#         self.angle = pi * 1.5
#         self.end = (0, 0)
#         self.setEnd()
#         # print(f"Start: {self.start}, End: {self.end}")
    
#     def update(self):
#         pass
    
#     def setEnd(self):
#         self.end = (
#             self.start[0] + (cos(self.angle) * segmentLength),
#             self.start[1] + (sin(self.angle) * segmentLength)
#         )
    
#     def render(self, thickness):
#         x1, y1 = int(self.start[0]), int(self.start[1])
#         x2, y2 = int(self.end[0]), int(self.end[1])
#         pygame.draw.line(
#             canvas, 
#             (0, 0, 0), 
#             (x1, y1), 
#             (x2, y2), 
#             thickness
#         )

#         if self.parent == None:
#             pygame.draw.circle(
#                 canvas, 
#                 (255, 0, 0), 
#                 (x2, y2), 
#                 thickness, 
#                 0
#             )

# Tentacle = []
# for i in range(segmentCount):
#     if i==0: Tentacle.append(Segment())
#     else: Tentacle.append(Segment(Tentacle[i-1]))

# segmentStart = [0, 0]

segmentCount = 7
segmentLength = int((canvasH*0.9) / segmentCount) # 35
start = [[0, 0] for _ in range(segmentCount)]
end = [[0, 0] for _ in range(segmentCount)]

base = [canvasW//2, canvasH]

# mouseX = mouseY = 0
target = [0, 0]
vel = [cos(pi * 0.4) / 10, sin(pi * 0.4) / 10]
while True:
    canvas.fill((255, 255, 255))

    target[0] += vel[0]
    target[1] += vel[1]
    if target[0] < 0 or target[0] > canvasW:
        vel[0] *= -1
    if target[1] < 0 or target[1] > canvasH:
        vel[1] *= -1
    
    pygame.draw.circle(
        canvas, 
        (100, 255, 100), 
        (int(target[0]), int(target[1])), 
        segmentCount, 
        0
    )

    # for s in range(segmentCount):
    #     Tentacle[s].update()
        
    #     Tentacle[s].render(segmentCount-s)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = pygame.mouse.get_pos()
    
    # pygame.draw.circle(
    #     canvas, (100, 255, 100),
    #     (mouseX, mouseY), 4, 0
    # )

    for i in range(segmentCount):
        
        if i == 0: 
            x1 = target[0] # mouseX
            y1 = target[1] # mouseY
        else:
            x1 = start[i-1][0]
            y1 = start[i-1][1]
        
        dx = x1 - start[i][0]
        dy = y1 - start[i][1]
        theta = atan2(dy, dx)
        
        start[i] = [
            x1 + (cos(theta + pi) * segmentLength),
            y1 + (sin(theta + pi) * segmentLength)
        ]
        end[i] = [x1, y1]
    
    dx = start[-1][0] - base[0]
    dy = start[-1][1] - base[1]

    for i in range(segmentCount):
        start[i][0] -= dx
        start[i][1] -= dy
        end[i][0] -= dx
        end[i][1] -= dy

        thickness = (i + 1) * segmentCount
        pygame.draw.line(canvas, (0,0,0), start[i], end[i], thickness)
        pygame.draw.circle(
            canvas, 
            (0,0,0), 
            (
                int(end[i][0]),
                int(end[i][1])
            ), 
            int(thickness * 0.5), 
            0
        )

    pygame.display.flip()