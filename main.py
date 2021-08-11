import pygame

pygame.init()
screen = pygame.display.set_mode((1080,720))
DEFAULT_COLOR = (0,0,0)
SELECTED_COLOR = (255,0,0)
FONT_COLOR = (0,0,0)

class SudokuField:

    def __init__(self, x, y, width, height, text, number_locked):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = DEFAULT_COLOR
        self.text = text
        self.txt_surface = pygame.font.Font(None, 70).render(text, True, FONT_COLOR)
        self.active = False
        self.number_locked = False

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 15, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = SELECTED_COLOR
            else:
                self.active = False
                self.color = DEFAULT_COLOR


def main():
    done = False
    screen.fill((255,255,255))
    test = SudokuField(100,100,50,50, "9")
    while done is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            else:
                test.handle_input(event)
        pygame.display.flip()
        test.draw(screen)

if __name__ == '__main__':
    main()
    pygame.quit()