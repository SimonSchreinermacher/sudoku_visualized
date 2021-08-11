import pygame

pygame.init()
screen = pygame.display.set_mode((1080,720))
font = pygame.font.Font(None, 70)
DEFAULT_COLOR = (0,0,0)
SELECTED_COLOR = (255,0,0)
FONT_COLOR = (0,0,0)

class SudokuField:

    def __init__(self, x, y, width, height, text, number_locked):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = DEFAULT_COLOR
        self.text = text
        self.txt_surface = font.render(text, True, FONT_COLOR)
        self.active = False
        self.number_locked = False

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 15, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def set_number(self,number):
        screen.fill((255,255,255))
        self.text = number
        self.txt_surface = font.render(self.text,True,FONT_COLOR)
        screen.blit(self.txt_surface, (self.rect.x + 15, self.rect.y + 5))
        self.draw(screen)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = SELECTED_COLOR
            else:
                self.active = False
                self.color = DEFAULT_COLOR
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if self.number_locked == False:
                    if event.unicode in ["1","2","3","4","5","6","7","8","9"]:
                        self.set_number(event.unicode)


def handle_all_fields(grid, event):
    for i in range(0, 10):
        for j in range(0, 10):
            grid[i][j].handle_input(event)

def draw_all_field(grid):
    for i in range(0, 10):
        for j in range(0, 10):
            grid[i][j].draw(screen)

def main():
    done = False
    screen.fill((255,255,255))
    grid = []
    for i in range(0, 10):
        grid.append([])
        for j in range(0, 10):
            field = SudokuField(100+ i*60, 100 + j*60, 50, 50, "", False)
            grid[i].append(field)
            field.draw(screen)

    while done is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            else:
                handle_all_fields(grid, event)
        pygame.display.flip()
        draw_all_field(grid)

if __name__ == '__main__':
    main()
    pygame.quit()