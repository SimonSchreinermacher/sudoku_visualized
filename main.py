import pygame
import random
import numpy as np
from time import sleep

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
        self.font = pygame.font.Font(None, 70)
        self.txt_surface = self.font.render(text, True, FONT_COLOR)
        self.active = False
        self.number_locked = False

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 15, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def set_number(self,number):
        screen.fill((255,255,255))
        self.text = number
        self.txt_surface = self.font.render(self.text,True,FONT_COLOR)
        #screen.blit(self.txt_surface, (self.rect.x + 15, self.rect.y + 5))
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
                    elif event.key == pygame.K_BACKSPACE:
                        self.set_number(str(""))


class Button:
    def __init__(self,x,y,width,height,text):
        self.rect = pygame.Rect(x,y,width,height)
        self.text = text
        self.font = pygame.font.Font(None, 30)
        self.color = DEFAULT_COLOR
        self.txt_surface = self.font.render(self.text, True, FONT_COLOR)

    def is_pressed(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return 1
        return 0

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def change_text(self, text):
        screen.fill((255,255,255))
        self.text = text
        self.txt_surface = self.font.render(self.text, True, FONT_COLOR)
        self.draw(screen)


def handle_all_fields(grid, event):
    for i in range(0, 9):
        for j in range(0, 9):
            grid[i][j].handle_input(event)

def draw_all_field(grid):
    for i in range(0, 9):
        for j in range(0, 9):
            grid[i][j].draw(screen)
    pygame.display.flip()

def search_for_empty_spot(grid):
	for i in range(0, 9):
		for j in range(0, 9):
			if(grid[i][j].text == ""):
				return i, j	
	return None

def is_allowed(grid,i,j,number):
	for x in range(0, 9):
		if(grid[x][j].text == str(number) or grid[i][x].text == str(number)):
			return False

	for x in range(0, 3):
		for y in range(0,3):
			upper_left_corner_x = i-i%3
			upper_left_corner_y = j-j%3
			if(grid[upper_left_corner_x + x][upper_left_corner_y + y].text == str(number)):
				return False
	return True

def fill_sudoku(grid, do_visualize):    #This can be used for either solving or creating (= solving a completely empty sudoku)
    if(do_visualize):
        sleep(0.1)      #For visualizing purposes (creating would be too quickly otherwise)
    if(search_for_empty_spot(grid) != None):
        (i,j) = search_for_empty_spot(grid)
    else:
        return grid
    remaining_numbers = [1,2,3,4,5,6,7,8,9]
    while len(remaining_numbers) != 0:
        index = random.randint(0, len(remaining_numbers)-1)
        number = remaining_numbers[index]
        del remaining_numbers[index]
        if(is_allowed(grid, i, j, number)):
            grid[i][j].set_number(str(number))
            grid[i][j].number_locked = True
            if do_visualize:
                draw_all_field(grid)
            if(fill_sudoku(grid, do_visualize) is not None):
                return grid
            grid[i][j].set_number(str(""))
            grid[i][j].number_locked = False
    return None

def remove_some_numbers(grid, probability_to_remove):
    for i in range(0, 9):
        for j in range(0, 9):
            x = random.random()
            if x <= probability_to_remove:
                grid[i][j].set_number(str(""))
                grid[i][j].number_locked = False

def initialization():
    start_game = Button(700,100, 300,30, "Start Sudoku")
    start_game.draw(screen)
    do_visualize = True

    if(do_visualize):
        visualize_button_text = "Visualization enabled"
    else:
        visualize_button_text = "Visualization disabled"

    visualize_button = Button(700,400, 300, 30, visualize_button_text)
    visualize_button.draw(screen)

    screen.fill((255,255,255))
    grid = []
    for i in range(0, 9):
        grid.append([])
        for j in range(0, 9):
            field = SudokuField(100+ i*60, 100 + j*60, 50, 50, "", False)
            grid[i].append(field)
            field.draw(screen)

    game_started = False
    do_visualize = True

    while not game_started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu_active = False
                pygame.quit()
                return
            else:
                if visualize_button.is_pressed(event) == 1:
                    do_visualize = not do_visualize
                    if do_visualize:
                        visualize_button.change_text("Visualization enabled")
                    else:
                        visualize_button.change_text("Visualization disabled")
                if start_game.is_pressed(event) == 1:
                    game_started = True
                    start_game.change_text("Another round!")
        
        start_game.draw(screen)
        visualize_button.draw(screen)
        draw_all_field(grid)
        pygame.display.flip()
    
    game(start_game, visualize_button, do_visualize, grid)

def game(start_game, visualize_button, do_visualize, grid = []):
    if(len(grid) == 0):             #In first game round, grid is passed from the initialization, in all subsequent rounds, grid is created here, because it needs to be cleared before each round
        screen.fill((255,255,255))
        grid = []
        for i in range(0, 9):
            grid.append([])
            for j in range(0, 9):
                field = SudokuField(100+ i*60, 100 + j*60, 50, 50, "", False)
                grid[i].append(field)
                field.draw(screen)

    start_game.draw(screen)
    visualize_button.draw(screen)
    draw_all_field(grid)
    pygame.display.flip()

    grid = fill_sudoku(grid, do_visualize)
    remove_some_numbers(grid, 0.5)
    game_active = True

    solve_button = Button(700,200, 300, 30, "Solve")

    while game_active:
        start_game.draw(screen)
        visualize_button.draw(screen)
        solve_button.draw(screen)
        draw_all_field(grid)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
                pygame.quit()
                return
            else:
                if visualize_button.is_pressed(event) == 1:
                    do_visualize = not do_visualize
                    if do_visualize:
                        visualize_button.change_text("Visualization enabled")
                    else:
                        visualize_button.change_text("Visualization disabled")
                elif start_game.is_pressed(event) == 1:
                    game(start_game, visualize_button, do_visualize)
                    return
                elif solve_button.is_pressed(event) == 1:
                    fill_sudoku(grid,do_visualize)
                else:
                    handle_all_fields(grid, event)    


if __name__ == '__main__':
    initialization()