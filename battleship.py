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
WINDOW_WIDTH = BOARD_WIDTH * 2 + 300  
WINDOW_HEIGHT = BOARD_HEIGHT + 300  

# Creating the window for pygame
def create_window(surface):
    surface.fill((0,0,0))
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Battleship', 1, (255,255,255)) 
    surface.blit(label, ((WINDOW_WIDTH - label.get_width()) // 2, 20))


class Piece:
    def __init__(self, name, orientation, x, y, color):
        self.name = name
        self.length = self.get_length(name)
        self.orientation = orientation
        self.x = x
        self.y = y
        self.color = color 
    
    def get_length(self, name):
        for piece in battleship_pieces:
            if piece["name"] == name:
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
        """Draws the game board grid for the player (bottom-left) and AI (bottom-right)."""

        # Define Y offset to position both grids at the bottom
        grid_y_offset = WINDOW_HEIGHT - BOARD_HEIGHT - 50  # Moves it upwards

        if self.player:
            # Bottom-left grid offset
            grid_x_offset = 50  # Left grid position

        else:
            # Bottom-right grid offset
            grid_x_offset = WINDOW_WIDTH - BOARD_WIDTH - 50  # Moves the grid to the right

        # Draw vertical grid lines
        for i in range(GRID_SIZE + 1):  # +1 to draw the last line
            pygame.draw.line(
                surface,
                (255, 255, 255),  # White lines
                (grid_x_offset + i * CELL_SIZE, grid_y_offset),  # Start position
                (grid_x_offset + i * CELL_SIZE, grid_y_offset + BOARD_HEIGHT)  # End position
            )

        # Draw horizontal grid lines
        for i in range(GRID_SIZE + 1):  
            pygame.draw.line(
                surface,
                (255, 255, 255),  # White lines
                (grid_x_offset, grid_y_offset + i * CELL_SIZE),  # Start position
                (grid_x_offset + BOARD_WIDTH, grid_y_offset + i * CELL_SIZE)  # End position
            )
        

        

    def get_grid_position(self, mouse_x, mouse_y):
        """Converts mouse coordinates to grid position for ship placement."""
        grid_x_offset = 50 if self.player else WINDOW_WIDTH - BOARD_WIDTH - 50
        grid_y_offset = WINDOW_HEIGHT - BOARD_HEIGHT - 50

        col = (mouse_x - grid_x_offset) // CELL_SIZE
        row = (mouse_y - grid_y_offset) // CELL_SIZE

        if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
            return row, col
        return None
            
    def highlight_cell(self, surface, mouse_x, mouse_y, orientation, ship_length):
        """Highlights the ship placement area before placing it."""
        if self.player:
            grid_x_offset = 50  
            grid_y_offset = WINDOW_HEIGHT - BOARD_HEIGHT - 50
        else:
            grid_x_offset = WINDOW_WIDTH - BOARD_WIDTH - 50  
            grid_y_offset = WINDOW_HEIGHT - BOARD_HEIGHT - 50 

        # Convert mouse position to grid coordinates
        col = (mouse_x - grid_x_offset) // CELL_SIZE
        row = (mouse_y - grid_y_offset) // CELL_SIZE

        # Check if mouse is inside the board boundaries
        if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
            # Highlight all cells where the ship would be placed
            for i in range(ship_length):
                if orientation == "right":
                    highlight_col = col + i
                    highlight_row = row
                elif orientation == "left":
                    highlight_col = col - i
                    highlight_row = row
                elif orientation == "down":
                    highlight_col = col
                    highlight_row = row + i
                elif orientation == "up":
                    highlight_col = col
                    highlight_row = row - i

                # Ensure the highlight is within board boundaries
                if 0 <= highlight_col < GRID_SIZE and 0 <= highlight_row < GRID_SIZE:
                    pygame.draw.rect(
                        surface,
                        (255, 100, 100),  # Light gray highlight
                        (grid_x_offset + highlight_col * CELL_SIZE, 
                        grid_y_offset + highlight_row * CELL_SIZE, 
                        CELL_SIZE, CELL_SIZE),
                        3  # Border thickness
                    )

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
        if piece.orientation == "up":
            for i in range(piece.length):
                if self.valid_space(x, y - i):
                    locations.append((x, y - i))
                else:
                    break
        if piece.orientation == "down":
            for i in range(piece.length):
                if self.valid_space(x, y + i):
                    locations.append((x, y + i))
                else:
                    break

        return locations


def start_game(surface):
    pygame.init()
    board1 = Board()
    board2 = Board(player=False)
    index = 0
    current_orientation = "right"

    while index < len(battleship_pieces):
        current_length = battleship_pieces[index]["length"]
        create_window(surface)
        board1.draw_board(surface)
        board2.draw_board(surface)

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if current_orientation == "right":
                    current_orientation = "down"
                elif current_orientation == "down":
                    current_orientation = "left"
                elif current_orientation == "left":
                    current_orientation = "up"
                else:
                    current_orientation = "right"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                grid_pos = board1.get_grid_position(mouse_x, mouse_y)  # Get updated grid position
                if grid_pos:
                    row, col = grid_pos
                    current_piece = Piece(
                        battleship_pieces[index]["name"], current_orientation, col, row, (255, 0, 0)
                    )
                    board1.add_piece(current_piece)  # Ensure valid placement
                    index += 1  # Move to next ship
        
        board1.highlight_cell(surface, mouse_x, mouse_y, current_orientation, current_length)
        pygame.display.update()  # Refresh screen

    

def main(surface, board1, board2):
    pass

if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Battleship")
    start_game(win)







    