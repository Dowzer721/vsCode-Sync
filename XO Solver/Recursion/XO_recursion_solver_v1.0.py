
import pygame

board = [
    "wwwwwww",
    "bwwwwww",
    "wwwxwww",
    "bbbwwww",
    "xwxxwwb",
    "wwbwwww",
    "xbbxwwo"
]

boardH, boardW = len(board), len(board[0])

cellW = cellH = 50

canvasW = canvasH = (cellW * boardW)
canvas = pygame.display.set_mode((canvasW, canvasH))

def renderBoard():
    for r in range(boardH):
        for c in range(boardW):

            x = c * cellW
            y = r * cellH

            pygame.draw.rect(
                canvas, 
                (0, 0, 0) if (board[r][c] == 'b') else (255, 255, 255),
                (x, y, cellW, cellH), 0
            )

            if board[r][c] != 'b':
                pygame.draw.polygon(
                    canvas, 
                    (0,0,0), 
                    [(x,y), (x+cellW,y), (x+cellW, y+cellH), (x, y+cellH)], 
                    1
                )
            
            if board[r][c] == 'x':
                
                pygame.draw.line(
                    canvas, 
                    (0,0,0), 
                    (int((c+0.25) * cellW), int((r+0.25) * cellH)), 
                    (int((c+0.75) * cellW), int((r+0.75) * cellH)), 
                    4
                )
                pygame.draw.line(
                    canvas, 
                    (0,0,0), 
                    (int((c+0.75) * cellW), int((r+0.25) * cellH)), 
                    (int((c+0.25) * cellW), int((r+0.75) * cellH)), 
                    4
                )
            elif board[r][c] == 'o':
                pygame.draw.circle(
                    canvas, 
                    (0,0,0), 
                    (int((c+0.5) * cellW), int((r+0.5) * cellH)), 
                    int(cellW * 0.3), 
                    2
                )

def valid(r, c, v):
    if board[r][c] != 'w': return False

    # 0 1 2
    # 3   4
    # 5 6 7

    neighbours = [
        board[r-1][c-1] if r>0 and c>0 else 'w', #              0
        board[r-1][c+0] if r>0 else 'w', #                      1
        board[r-1][c+1] if r>0 and c<boardW-1 else 'w', #       2
        board[r][c-1] if c>0 else 'w', #                        3
        board[r][c+1] if c<boardW-1 else 'w', #                 4
        board[r+1][c-1] if r<boardH-1 and c>0 else 'w', #       5
        board[r+1][c] if r<boardH-1 else 'w', #                 6
        board[r+1][c+1] if r<boardH-1 and c<boardW-1 else 'w' # 7
    ]

    for neighbourIndex in range(9):
        oppositeIndex = 8 - neighbourIndex
        


    # print(neighbours[0:3])
    # print([neighbours[3], board[mouseR][mouseC], neighbours[4]])
    # print(neighbours[5:])
    # print("")

    

def solve():
    pass
solve()

while True:
    canvas.fill((255, 255, 255))
    renderBoard()
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            mouseX, mouseY = pygame.mouse.get_pos()
            mouseC = int(mouseX / cellW)
            mouseR = int(mouseY / cellH)

            pos = [
                0, 1, 2,
                3,    5,
                6, 7, 8
            ]

            for p in pos:
                oppo = 8 - p
                print(f"p:{p}, op:{oppo}")
            

    
    pygame.display.flip()

# input()