import pygame

pygame.init()
screen = pygame.display.set_mode((1080,720))

def main():
    done = False
    screen.fill((255,255,255))
    while done is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()

if __name__ == '__main__':
    main()
    pygame.quit()