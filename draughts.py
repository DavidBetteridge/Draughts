import pygame

# UI
COLOUR_WHITE = (255,255,255) 
COLOUR_BLACK = (0,0,0) 
COLOUR_RED = (255,0,0) 
COLOUR_BLUE = (0,0,255) 
COLOUR_BACKGROUND = (225,255,255) 
SQUARE_SIZE = 60
BORDER = 30

# abc
# c = (0 = empty, 1 = contains piece) 0 1
# b = (0 = normal, 1 = king) 00 10
# a = (0 = black, 1 = white) 000 100
EMPTY = 0b000
HAS_PIECE = 0b001
NORMAL = 0b000
KING = 0b010
BLACK = 0b000
WHITE = 0b100

def is_white(piece):
    return (piece & WHITE) == WHITE

def is_piece(piece):
    return (piece & HAS_PIECE) == HAS_PIECE

def is_king(piece):
    return (piece & KING) == KING

def setup_board():
    pieces = [0] * 64
    for rowNumber in range(3):
        for columnNumber in range(8):
            if (rowNumber + columnNumber) % 2 == 1:
                index = (rowNumber * 8) + columnNumber
                pieces[index] = HAS_PIECE | NORMAL | BLACK

    for rowNumber in range(5, 8):
        for columnNumber in range(8):
            if (rowNumber + columnNumber) % 2 == 1:
                index = (rowNumber * 8) + columnNumber
                pieces[index] = HAS_PIECE | NORMAL | WHITE
    return pieces

def draw_board(screen):
    for rowNumber in range(8):
        for columnNumber in range(8):
            if (rowNumber + columnNumber) % 2 == 0:
                colour = COLOUR_WHITE
            else:
                colour = COLOUR_BLACK

            pygame.draw.rect(screen, colour, pygame.Rect(BORDER + (SQUARE_SIZE * columnNumber), BORDER + (SQUARE_SIZE * rowNumber), SQUARE_SIZE, SQUARE_SIZE)) 

def draw_piece(screen, pieces, rowNumber, columnNumber, whiteCounter, blackCounter):
    index = (rowNumber * 8) + columnNumber
    if is_piece(pieces[index]):
        if is_white(pieces[index]):
            counterImage = whiteCounter
        else:
            counterImage = blackCounter

        imageRect = counterImage.get_rect()
        imageRect.x = BORDER + 5 + (SQUARE_SIZE * columnNumber)
        imageRect.y = BORDER + 5 + (SQUARE_SIZE * rowNumber)
        screen.blit(counterImage, imageRect)

def load_counter_image(imageName):
    counterImage = pygame.image.load(imageName)
    counterImage.convert()
    return pygame.transform.scale(counterImage, (SQUARE_SIZE-10,SQUARE_SIZE-10))

def build_index(columnNumber, rowNumber):
    return (rowNumber * 8) + columnNumber

def available_moves(pieces, columnNumber, rowNumber):
    moves = []

    # TOP-LEFT
    if (columnNumber > 0 and rowNumber > 0):
        index = build_index(columnNumber-1, rowNumber-1)
        if not is_piece(pieces[index]):
            moves.append((columnNumber - 1, rowNumber - 1))
    
    # BOTTOM-LEFT
    if (columnNumber > 0 and rowNumber < 6):
        index = build_index(columnNumber-1, rowNumber+1)
        if not is_piece(pieces[index]):
            moves.append((columnNumber - 1, rowNumber + 1)) 
    
    # BOTTOM-RIGHT
    if (columnNumber < 6 and rowNumber < 6):
        index = build_index(columnNumber+1, rowNumber+1)
        if not is_piece(pieces[index]):
            moves.append((columnNumber + 1, rowNumber + 1)) 

    
    return moves


def main():
    pygame.init()
    pygame.display.set_caption("Draughts")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((560,560))
    screen.fill(COLOUR_BACKGROUND)
    
    whiteCounter = load_counter_image("white-counter.png")
    blackCounter = load_counter_image("black-counter.png")

    pieces = setup_board()
    draw_board(screen)

    for rowNumber in range(8):
        for columnNumber in range(8):
            draw_piece(screen, pieces, rowNumber, columnNumber, whiteCounter, blackCounter)    

    pygame.display.flip() 

    whiteToPlay = False
    running = True
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x,y) = event.pos
                if (BORDER < x < BORDER + (8 * SQUARE_SIZE)):
                    if (BORDER < y < BORDER + (8 * SQUARE_SIZE)):
                        rowNumber = (y - BORDER) // SQUARE_SIZE
                        columnNumber = (x - BORDER) // SQUARE_SIZE

                        index = (rowNumber * 8) + columnNumber
                        if is_piece(pieces[index]) and whiteToPlay == is_white(pieces[index]):
                            pygame.draw.rect(screen, COLOUR_RED, pygame.Rect(BORDER + (SQUARE_SIZE * columnNumber), BORDER + (SQUARE_SIZE * rowNumber), SQUARE_SIZE, SQUARE_SIZE)) 

                            draw_piece(screen, pieces, rowNumber, columnNumber, whiteCounter, blackCounter)    

                            moves = available_moves(pieces, columnNumber, rowNumber)
                            for (x,y) in moves:
                                pygame.draw.rect(screen, COLOUR_BLUE, pygame.Rect(BORDER + (SQUARE_SIZE * x), BORDER + (SQUARE_SIZE * y), SQUARE_SIZE, SQUARE_SIZE)) 

                            pygame.display.flip() 

        clock.tick(60)
     
if __name__=="__main__":
    main()