import pygame
import random

battleship_pieces = [
    {"name": "Carrier", "length": 5,},
    {"name": "Battleship", "length": 4},
    {"name": "Cruiser", "length": 3},
    {"name": "Submarine", "length": 3},
    {"name": "Destroyer", "length": 2}
]

# Constants
CELL_SIZE = 50  # Each grid cell is 50x50 pixels
GRID_SIZE = 10   # 10x10 board
BOARD_WIDTH = CELL_SIZE * GRID_SIZE  # 500 pixels
BOARD_HEIGHT = CELL_SIZE * GRID_SIZE # 500 pixels

# Layout Settings (Side by Side)
WINDOW_WIDTH = BOARD_WIDTH * 2 + 100  # 1100 pixels (for spacing and UI)
WINDOW_HEIGHT = BOARD_HEIGHT + 100  # 600 pixels (for UI elements)

# Creating the window for pygame
def create_window(surface):
    surface.fill((0,0,0))
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Battleship', 1, (255,255,255)) # render the word tetris
    win.blit(label, )



class Piece:
    def __init__(self, name, orientation, x, y, color):
        self.name = name
        self.length = self.get_length()
        self.orientation = orientation
        self.x = x
        self.y = y
        self.color = color 
    
    def get_length(self):
        for piece in battleship_pieces:
            if piece["name"] == self.name:
                return piece["length"]
        return 0 # Piece not found
    
    
class Board:
    def __init__ (self, player = True):
        self.board = [[(0,0,0) for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
        self.pieces = []  # List of Piece objects
        self.player = player

    def add_piece(self, piece):
        locations = self.get_locations(piece, piece.x, piece.y)
        for x, y in locations:
            self.board[x][y] = piece.color
        self.pieces.append(piece)

    def draw_board(self, surface):
        pass


    def valid_space(self, x, y):
        """Checks if (x, y) is inside the board and unoccupied."""
        if x < 0 or x >= len(self.board) or y < 0 or y >= len(self.board[0]):
            return False

        if self.board[x][y] != (0, 0, 0):  
            return False
        
        return True
    
    def get_locations(self, piece, x, y):
        locations = []

        if piece.orientation == "left":
            for i in range(piece.length):
                if self.valid_space(x - i, y):
                    locations.append((x - i, y))
                else:
                    break
        if piece.orientation == "right":
            for i in range(piece.length):
                if self.valid_space(x + i, y):
                    locations.append((x + i, y))
                else:
                    break
        if piece.orientation == "top":
            for i in range(piece.length):
                if self.valid_space(x, y - i):
                    locations.append((x, y - i))
                else:
                    break
        if piece.orientation == "bottom":
            for i in range(piece.length):
                if self.valid_space(x, y + i):
                    locations.append((x, y + i))
                else:
                    break

        return locations



if __name__ == "__main__":
    board = Board()
    piece1 = Piece("Carrier", "right", 0, 0, (255,0,0))
    piece2 = Piece("Battleship", "bottom", 9, 0, (255,0,0))
    board.add_piece(piece1)
    board.add_piece(piece2)
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Battleship")
    create_window(win)








    