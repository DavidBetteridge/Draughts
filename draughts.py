import pygame
import math

# UI
COLOUR_WHITE = (255,255,255) 
COLOUR_BLACK = (0,0,0) 
COLOUR_RED = (255,0,0) 
COLOUR_BLUE = (0,0,255) 
COLOUR_YELLOW = (255,255,0) 
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

class Board:
    def __init__(this, pieces):
        this.pieces = pieces
        this.highlight = None
        this.available_moves = []
        this.clicked = []

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
    return Board(pieces)

def draw_board():
    surface = pygame.surface.Surface((8 * SQUARE_SIZE, 8 * SQUARE_SIZE))

    for rowNumber in range(8):
        for columnNumber in range(8):
            if (rowNumber + columnNumber) % 2 == 0:
                colour = COLOUR_WHITE
            else:
                colour = COLOUR_BLACK

            pygame.draw.rect(surface, colour, pygame.Rect(SQUARE_SIZE * columnNumber, SQUARE_SIZE * rowNumber, SQUARE_SIZE, SQUARE_SIZE)) 

    return surface

def draw_piece(screen, board, rowNumber, columnNumber, whiteCounter, blackCounter):
    pieces = board.pieces
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

def in_bounds(columnNumber, rowNumber):
    return 0 <= columnNumber < 8 and 0 <= rowNumber < 8

def calculate_available_moves(pieces, columnNumber, rowNumber, isKing, isWhite):
    moves = []
    capture_moves = []

    directions = []

    if isWhite or isKing:
        directions.append((-1,-1))
        directions.append((+1,-1))

    if (not isWhite) or isKing:
        directions.append((-1,+1))
        directions.append((+1,+1))

    for (xOffset, yOffset) in directions:
        next = (columnNumber + xOffset, rowNumber + yOffset)
        if in_bounds(*next):
            index = build_index(*next)
            if not is_piece(pieces[index]):
                moves.append(next)
            else:
                if is_white(pieces[index]) != isWhite:
                    next2 =  (columnNumber + xOffset + xOffset, rowNumber + yOffset + yOffset)
                    if in_bounds(*next2):
                        index2 = build_index(*next2)
                        if not is_piece(pieces[index2]):
                            capture_moves.append(next2)

    if capture_moves:
        return (capture_moves, True)
    else:
        return (moves, False)

def all_available_moves(board, whiteToPlay):
    pieces = board.pieces
    moves = []
    capture_moves = []
    for rowNumber in range(8):
        for columnNumber in range(8):
            index = build_index(columnNumber, rowNumber)
            if is_piece(pieces[index]) and whiteToPlay == is_white(pieces[index]):
                (legal_moves, isCapture) = calculate_available_moves(pieces, columnNumber, rowNumber, is_king(pieces[index]), is_white(pieces[index]))
                if len(legal_moves) > 0:
                    if isCapture:
                        capture_moves.append((columnNumber, rowNumber)) 
                    else:
                        moves.append((columnNumber, rowNumber)) 
    if capture_moves:
        return capture_moves
    else:
        return moves

def draw_pieces(screen, board, whiteCounter, blackCounter):
    for rowNumber in range(8):
        for columnNumber in range(8):
            draw_piece(screen, board, rowNumber, columnNumber, whiteCounter, blackCounter)      

def square_under_mouse(x,y):
    if (BORDER < x < BORDER + (8 * SQUARE_SIZE)):
        if (BORDER < y < BORDER + (8 * SQUARE_SIZE)):
            rowNumber = (y - BORDER) // SQUARE_SIZE
            columnNumber = (x - BORDER) // SQUARE_SIZE
            return (columnNumber, rowNumber)
    return None

def draw_all(screen, board, backgroundSurface, whiteCounter, blackCounter, whiteToPlay):
    screen.blit(backgroundSurface,(BORDER,BORDER))

    for (x,y) in board.available_moves:
        pygame.draw.rect(screen, COLOUR_BLUE, pygame.Rect(BORDER + (SQUARE_SIZE * x), BORDER + (SQUARE_SIZE * y), SQUARE_SIZE, SQUARE_SIZE))     

    for (x,y) in board.clicked:
        pygame.draw.rect(screen, COLOUR_RED, pygame.Rect(BORDER + (SQUARE_SIZE * x), BORDER + (SQUARE_SIZE * y), SQUARE_SIZE, SQUARE_SIZE))     

    if (board.highlight != None):
        (columnNumber, rowNumber) = board.highlight
        pygame.draw.rect(screen, COLOUR_YELLOW, pygame.Rect(BORDER + (SQUARE_SIZE * columnNumber), BORDER + (SQUARE_SIZE * rowNumber), SQUARE_SIZE, SQUARE_SIZE)) 

    draw_pieces(screen, board, whiteCounter, blackCounter)   
    pygame.display.flip() 


def find_middle_square(square1, square2):
    (x1, y1) = square1
    (x2, y2) = square2
    if abs(x1 - x2) == 2:
        x3 = x1 - 1 if x1 > x2 else x1 + 1
        y3 = y1 - 1 if y1 > y2 else y1 + 1
        return (x3, y3)
    else:
        return None

def main():
    pygame.init()
    pygame.display.set_caption("Draughts")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(( (8 * SQUARE_SIZE) + (2 * BORDER) ,(8 * SQUARE_SIZE) + (2 * BORDER)))
    screen.fill(COLOUR_BACKGROUND)
    
    whiteCounter = load_counter_image("white-counter.png")
    blackCounter = load_counter_image("black-counter.png")

    board = setup_board()
    backgroundSurface = draw_board()

    whiteToPlay = False

    board.available_moves = all_available_moves(board, whiteToPlay)
    draw_all(screen, board, backgroundSurface, whiteCounter, blackCounter, whiteToPlay)  

    running = True
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

            elif event.type == pygame.MOUSEMOTION:
                square = square_under_mouse(*event.pos)
                board.highlight = square

            elif event.type == pygame.MOUSEBUTTONDOWN:
                square = square_under_mouse(*event.pos)    
                if (square != None and square in board.available_moves):
                    index = build_index(*square)
                    if board.clicked:
                        fromIndex = build_index(*board.clicked[0])
                        board.pieces[index] = board.pieces[fromIndex]
                        board.pieces[fromIndex] = 0

                        jumped = find_middle_square(square, board.clicked[0])
                        if jumped != None:
                            jumpIndex = build_index(*jumped)
                            board.pieces[jumpIndex] = 0

                        whiteToPlay = not whiteToPlay
                        board.clicked = []     
                        board.available_moves = all_available_moves(board, whiteToPlay) 
                    else:
                        (board.available_moves, _) = calculate_available_moves(board.pieces, *square, is_king(board.pieces[index]), is_white(board.pieces[index]) )
                        board.clicked = [square]     
                else:
                    board.clicked = []     
                    board.available_moves = all_available_moves(board, whiteToPlay)       

            draw_all(screen, board, backgroundSurface, whiteCounter, blackCounter, whiteToPlay)  

        clock.tick(60)
     
if __name__=="__main__":
    main()