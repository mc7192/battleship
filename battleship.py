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
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render('Your board', 1, (255,255,255))
    surface.blit(label, ((WINDOW_WIDTH - label.get_width()) // 2 - 400, 180))
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render("Opponent's board", 1, (255,255,255))
    surface.blit(label, ((WINDOW_WIDTH - label.get_width()) // 2 + 350, 180))

def start_text(surface, text):
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render(text, 1, (255,255,255))
    surface.blit(label, ((WINDOW_WIDTH - label.get_width()) // 2, 100))

def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    # Calculate center position
    text_x = (WINDOW_WIDTH - label.get_width()) // 2
    text_y = (WINDOW_HEIGHT - label.get_height()) // 2
    if "Sunk" in text:
        text_y += 80

    # Draw text in the center of the screen
    surface.blit(label, (text_x, text_y))


class Piece:
    def __init__(self, name, orientation, x, y, color=(255,0,0)):
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
        self.pieces = {}  # List of Piece objects : locations
        self.player = player
        self.hit = [] #tuple of positions 

    def add_piece(self, piece):
        """Attempts to add a ship to the board if all locations are valid."""
        locations = self.get_locations(piece, piece.x, piece.y)
        if not locations or any(self.board[col][row] != (0, 0, 0) for col, row in locations):
            return False  

        for col, row in locations:
            self.board[col][row] = piece.color  

        if piece.name not in self.pieces:
            self.pieces[piece.name] = locations
        return True  
    
    def attack(self, x, y, board, surface):
        if self.player:
            row, col = board.get_grid_position(x, y)
        else: 
            while True:
                row = random.randint(0, 9) 
                col = random.randint(0, 9)
                if (col, row) not in board.hit:
                    break

        if board.board[col][row] == (0,0,0):
            board.board[col][row] = (100, 100, 100)
            board.hit.append((col, row))
            if self.player:
                draw_text_middle("miss!", 50, (255,255,255), surface)
            return False
                    
        else:
            board.board[col][row] = (255, 0, 255)

            for name, locations in board.pieces.items():
                if (col, row) in locations:
                    locations.remove((col, row))
                    if self.player:
                        draw_text_middle("hit!", 50, (255,255,255), surface)
                        pygame.display.update()
                        pygame.time.delay(500)
                    if not locations:
                        del board.pieces[name]
                        if self.player:
                            draw_text_middle(f"Sunk {name}", 60, (0,0,200), surface)
                            pygame.display.update()
                            pygame.time.delay(500)
                        break
        
        return True
    

    def draw_board(self, surface, grid_only=False):
        grid_y_offset = WINDOW_HEIGHT - BOARD_HEIGHT - 50  
        if self.player:
            grid_x_offset = 50  

        else:
            grid_x_offset = WINDOW_WIDTH - BOARD_WIDTH - 50 

        # Draw vertical grid lines
        for i in range(GRID_SIZE + 1):  # +1 to draw the last line
            pygame.draw.line(
                surface,
                (255, 255, 255),  
                (grid_x_offset + i * CELL_SIZE, grid_y_offset), 
                (grid_x_offset + i * CELL_SIZE, grid_y_offset + BOARD_HEIGHT)  
            )

        for i in range(GRID_SIZE + 1):  
            pygame.draw.line(
                surface,
                (255, 255, 255),  
                (grid_x_offset, grid_y_offset + i * CELL_SIZE),  
                (grid_x_offset + BOARD_WIDTH, grid_y_offset + i * CELL_SIZE) 
            )
        
        if not grid_only:
            for col in range(len(self.board)):  
                for row in range(len(self.board[col])): 
                    if self.board[col][row] != (0, 0, 0):  
                        pygame.draw.rect(
                            surface, 
                            self.board[col][row], 
                                (
                                (grid_x_offset + col * CELL_SIZE, 
                                grid_y_offset + row * CELL_SIZE, 
                                CELL_SIZE, CELL_SIZE),
                                )
                            )
                    
    def hide_board(self, surface):
        if not self.player:
            grid_y_offset = WINDOW_HEIGHT - BOARD_HEIGHT - 50 
            grid_x_offset = WINDOW_WIDTH - BOARD_WIDTH - 50 
            for col in range(len(self.board)):  
                for row in range(len(self.board[col])): 
                    if self.board[col][row] == (255, 0, 0):
                        pygame.draw.rect(
                        surface, 
                        (0,0,0), 
                            (
                            (grid_x_offset + col * CELL_SIZE, 
                            grid_y_offset + row * CELL_SIZE, 
                            CELL_SIZE, CELL_SIZE),
                            )
                        )
            #redraw grid
            for i in range(GRID_SIZE + 1):  # +1 to draw the last line
                pygame.draw.line(
                    surface,
                    (255, 255, 255),  
                    (grid_x_offset + i * CELL_SIZE, grid_y_offset), 
                    (grid_x_offset + i * CELL_SIZE, grid_y_offset + BOARD_HEIGHT)  
                )

            for i in range(GRID_SIZE + 1):  
                pygame.draw.line(
                    surface,
                    (255, 255, 255),  
                    (grid_x_offset, grid_y_offset + i * CELL_SIZE),  
                    (grid_x_offset + BOARD_WIDTH, grid_y_offset + i * CELL_SIZE) 
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
                else:
                    highlight_col = col
                    highlight_row = row 

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
   
    def get_locations(self, piece, x, y):
        locations = []

        if piece.orientation == "left":
            locations = [(x - i, y) for i in range(piece.length)]
        elif piece.orientation == "right":
            locations = [(x + i, y) for i in range(piece.length)]
        elif piece.orientation == "up":
            locations = [(x, y - i) for i in range(piece.length)]
        elif piece.orientation == "down":
            locations = [(x, y + i) for i in range(piece.length)]
        
        if any(pos[0] < 0 or pos[0] >= len(self.board) or pos[1] < 0 or pos[1] >= len(self.board[0]) for pos in locations):
            return []  
        
        return locations


def start_game(surface):
    pygame.init()
    board1 = Board()
    board2 = Board(player=False)
    index1 = 0
    index2 = 0
    orientations = ["left", "right", "up", "down"]
    current_orientation2 = "right"

    #ai ship placement
    while index1 < len(battleship_pieces):
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        orientation = random.choice(orientations)
        current_piece = Piece(battleship_pieces[index1]["name"], orientation, x, y)
        if board2.add_piece(current_piece):
            index1 += 1


    while index2 < len(battleship_pieces):
        current_length = battleship_pieces[index2]["length"] 
        create_window(surface)    
        start_text(surface, "Please choose your ship positions")
        board1.draw_board(surface)
        board2.draw_board(surface)
        board1.draw_board(surface, grid_only=True)
        board2.hide_board(surface)

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if current_orientation2 == "right":
                    current_orientation2 = "down"
                elif current_orientation2 == "down":
                    current_orientation2 = "left"
                elif current_orientation2 == "left":
                    current_orientation2 = "up"
                else:
                    current_orientation2 = "right"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                grid_pos = board1.get_grid_position(mouse_x, mouse_y)  # Get updated grid position
                if grid_pos:
                    row, col = grid_pos
                    current_piece = Piece(
                        battleship_pieces[index2]["name"], current_orientation2, col, row, (255, 0, 0)
                    )
                    if board1.add_piece(current_piece):
                        index2 += 1  # Move to the next ship
                    else: 
                        print("try again")

        board1.highlight_cell(surface, mouse_x, mouse_y, current_orientation2, current_length)
        pygame.display.update()  # Refresh screen

    return board1, board2 

def main(surface, board1, board2):
    pygame.init()
    run = True
    current_player = board1
    opponent = board2

    while run:
        create_window(surface)
        start_text(surface, "Please choose your targets")
        board1.draw_board(surface)
        board2.draw_board(surface)
        board1.draw_board(surface, grid_only=True)
        board2.hide_board(surface)
        x, y = pygame.mouse.get_pos()

        if not current_player.player:
            pygame.time.delay(200)
            hit = current_player.attack(x, y, opponent, surface)

            if not hit:
                current_player, opponent = opponent, current_player
                    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
    
                if current_player.player:
                    hit = current_player.attack(x, y, opponent, surface)
                    
                    if not hit:
                        pygame.time.delay(200)
                        current_player, opponent = opponent, current_player
                    

        if not opponent.pieces:
            if current_player == board1:
                draw_text_middle("You win!", 50, (255,255,255), surface)
            else:
                draw_text_middle("You lose!", 50, (255,255,255), surface)

            pygame.display.update()
            pygame.time.delay(1000)
            pygame.quit()
        
        board2.highlight_cell(win, x, y, "none", 1)
        pygame.display.update()
        

if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Battleship")
    board1, board2 = start_game(win)
    main(win, board1, board2)







    