import pygame
from go_board import GoBoard
from go_stone import Stone
from game_logic import GameLogic

SIZE = (1400, 900)
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
LIGHT_GRAY = [192, 192, 192]
BLUE = [0, 0, 255]
FPS = 60

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

def draw_board():
    screen.fill(LIGHT_GRAY)
    for row in range(19):
        pygame.draw.line(screen, BLACK, (100, 50 + row * 45), (910, 50 + row * 45), 2)
    for col in range(19):
        pygame.draw.line(screen, BLACK, (100 + col * 45, 50), (100 + col * 45, 860), 2)
    
    for row in [3, 9, 15]:
        for col in [3, 9, 15]:
            pygame.draw.circle(screen, BLACK, (101 + row * 45, 51 + col * 45), 7)

def draw_stone(board):
    for i in range(19):
        for j in range(19):
            stone = board.board[i][j]
            x = 101 + i * 45
            y = 51 + j * 45

            if stone != 0 and stone.color == "black":
                pygame.draw.circle(screen, BLACK, (x, y), 22)
        
            if stone != 0 and stone.color == "white":
                pygame.draw.circle(screen, WHITE, (x, y), 22)

def locate_stone(position):
    x, y = position
    
    loc_row = round(abs(x  - 101) / 45)
    loc_col = round(abs(y - 51) / 45)

    return (loc_row, loc_col)

class Button:
    def __init__(self, text, loc_x, loc_y):
        self.text = text
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.button = pygame.Rect(self.loc_x, self.loc_y, 300, 100)
    
    def draw_button(self):
        font = pygame.font.SysFont(None, 70)
        button_text = font.render(self.text, True, BLACK, BLUE)
        screen.blit(button_text, [self.loc_x + 10, self.loc_y + 10])
    
    def is_clicking_button(self):
        loc = pygame.mouse.get_pos()
        if self.button.collidepoint(loc):
            return True
        return False

def new_game_button():
    new_game_button = Button("New Game", 1000, 400)
    new_game_button.draw_button()
    return new_game_button.is_clicking_button()

def main_interface(board):
    play = GameLogic(board)
    while True:
        clock.tick(FPS)
        draw_board()
        draw_stone(play.board)
        new_game_button()

        loc = pygame.mouse.get_pos()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and 90 <= loc[0] <= 920 and \
                40 <= loc[1] <= 870:
                stone = Stone(locate_stone(loc), play.board.turn, play.board)
                
                if play.move(stone):
                    if play.board.turn == "black":
                        play.board.turn = "white"
                    elif play.board.turn == "white":
                        play.board.turn = "black"
            
            if event.type == pygame.MOUSEBUTTONDOWN and new_game_button():
                play.step = 0
                play.record = []
                play.board.reset_board()
        
        pygame.display.update()


def main():
    pygame.init()
    pygame.display.set_caption("Go")
    main_interface(GoBoard())

if __name__ == "__main__":
    main()