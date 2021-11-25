import pygame
import random
import numpy as np
from time import sleep

pygame.init()
screen = pygame.display.set_mode((1080,720))
DEFAULT_COLOR = (0,0,0)
SELECTED_COLOR = (255,0,0)
TEXTBOX_COLOR = (255,255,255)
FONT_COLOR = (0,0,0)
USER_INPUT_FONT_COLOR = (100,100,100)
SOLVED_COLOR = (20,200,20)

class SudokuField:

    def __init__(self, x, y, width, height, text, number_locked):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = DEFAULT_COLOR
        self.text = text
        self.font = pygame.font.Font(None, 70)
        self.txt_surface = self.font.render(text, True, FONT_COLOR)
        self.active = False
        self.number_locked = False
        self.number_entered_by_user = False

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 15, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def set_number(self,number, is_user_input):
        screen.fill((255,255,255))
        self.text = number
        if is_user_input:
            self.number_entered_by_user = True
            self.txt_surface = self.font.render(self.text,True,USER_INPUT_FONT_COLOR)
        else:
            self.number_entered_by_user = False
            self.txt_surface = self.font.render(self.text,True,FONT_COLOR)
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
                        self.set_number(event.unicode, True)
                        return 1
                    elif event.key == pygame.K_BACKSPACE:
                        self.set_number(str(""), True)
                        return 0


class DisplayableField:
    def __init__(self,x,y,width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 30)
        self.color = TEXTBOX_COLOR
        self.txt_surface = self.font.render(self.text, True, FONT_COLOR)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def change_text(self, text):
        screen.fill((255,255,255))
        self.text = text
        self.txt_surface = self.font.render(self.text, True, FONT_COLOR)
        self.draw(screen)


class Button(DisplayableField):
    def __init__(self,x,y,width,height,text):
        super().__init__(x,y,width,height,text)
        self.color = FONT_COLOR

    def is_pressed(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return 1
        return 0

def all_fields_filled(grid):
    for i in range(0, 9):
        for j in range(0,9):
            if grid[i][j].text == str(""):
                return False
    return True

def solved_correctly(grid):
    #Do all rows/columns contain every digit exactly once
    for i in range(0,9):
        column_content = []
        row_content = []
        for j in range(0, 9):
            column_content.append(grid[i][j].text)
            row_content.append(grid[j][i].text)
        if not(set(column_content) == set(["1", "2", "3", "4", "5", "6", "7", "8", "9"])):
            return False
        if not(set(row_content) == set(["1", "2", "3", "4", "5", "6", "7", "8", "9"])):
            return False

    #Do all 3x3-Grids contain every digit exactly once
    for i in range(0,3):
        for j in range(0,3):
            grid_content = []
            for a in range(0,3):
                for b in range(0,3):
                    grid_content.append(grid[3*i + a][3*j + b].text)
            if not(set(grid_content) == set(["1", "2", "3", "4", "5", "6", "7", "8", "9"])):
                return False
    return True

def handle_all_fields(grid, event):
    for i in range(0, 9):
        for j in range(0, 9):
            if(grid[i][j].handle_input(event) == 1):
                return 1
    return 0

def draw_all_field(grid):
    for i in range(0, 9):
        for j in range(0, 9):
            grid[i][j].draw(screen)
    pygame.display.flip()

def search_for_empty_spot(grid):
	for i in range(0, 9):
		for j in range(0, 9):
			if(grid[i][j].text == "" or grid[i][j].number_entered_by_user == True):
				return i, j	
	return None

def is_allowed(grid,i,j,number):
	for x in range(0, 9):
		if((grid[x][j].text == str(number) and grid[x][j].number_entered_by_user == False) or (grid[i][x].text == str(number)) and grid[i][x].number_entered_by_user == False):
			return False

	for x in range(0, 3):
		for y in range(0,3):
			upper_left_corner_x = i-i%3
			upper_left_corner_y = j-j%3
			if(grid[upper_left_corner_x + x][upper_left_corner_y + y].text == str(number) and grid[upper_left_corner_x + x][upper_left_corner_y + y].number_entered_by_user == False):
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
            grid[i][j].set_number(str(number), False)
            grid[i][j].number_locked = True
            grid[i][j].number_entered_by_user = False
            if do_visualize:
                draw_all_field(grid)
            if(fill_sudoku(grid, do_visualize) is not None):
                return grid
            grid[i][j].set_number(str(""), False)
            grid[i][j].number_locked = False
            grid[i][j].number_entered_by_user = False
    return None

def remove_some_numbers(grid, probability_to_remain):
    i = random.randint(0,8)                 #One tile is guaranteed to be removed
    j = random.randint(0,8)
    grid[i][j].set_number(str(""), False)
    grid[i][j].number_locked = False

    for i in range(0, 9):                   #All other tiles have the set probability to be removed
        for j in range(0, 9):
            x = random.random()
            if x > probability_to_remain:
                grid[i][j].set_number(str(""), False)
                grid[i][j].number_locked = False

def on_solve(grid):
    for i in range(0,9):
        for j in range(0,9):
            grid[i][j].color = SOLVED_COLOR
    draw_all_field(grid)

def draw_all_gui(gui_objects, screen):
    for object in gui_objects:
        gui_objects[object].draw(screen)

def draw_grid():
    grid = []
    for i in range(0, 9):
        grid.append([])
        for j in range(0, 9):
            x_offset = 10* int(i/3)
            y_offset = 10* int(j/3)

            x_pos = 100 + i*60 + x_offset
            y_pos = 100 + j*60 + y_offset
            field = SudokuField(x_pos, y_pos, 50, 50, "", False)
            grid[i].append(field)
            field.draw(screen)
    return grid

def initialization():
    do_visualize = True
    percentage_filled = 0.5

    if(do_visualize):
        visualize_button_text = "Visualization enabled"
    else:
        visualize_button_text = "Visualization disabled"

    gui_objects = {}

    gui_objects["start_game"] = Button(700,100, 300,30, "Start Sudoku")
    gui_objects["visualize_button"] = Button(700,400, 300, 30, visualize_button_text)
    gui_objects["percentage_increase_button"] = Button(700,280, 100,30, "+")
    gui_objects["percentage_decrease_button"] = Button(820,280, 100, 30, "-")
    gui_objects["percentage_textbox"] = DisplayableField(700,250, 100, 30, str("Initialized filled tiles: " + str(percentage_filled)))

    draw_all_gui(gui_objects, screen)

    screen.fill((255,255,255))
    grid = draw_grid()

    game_started = False
    do_visualize = True

    while not game_started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu_active = False
                pygame.quit()
                return
            else:
                if gui_objects["visualize_button"].is_pressed(event) == 1:
                    do_visualize = not do_visualize
                    if do_visualize:
                        gui_objects["visualize_button"].change_text("Visualization enabled")
                    else:
                        gui_objects["visualize_button"].change_text("Visualization disabled")
                elif gui_objects["percentage_increase_button"].is_pressed(event) == 1:
                    if percentage_filled < 0.99:
                        percentage_filled += 0.01
                        gui_objects["percentage_textbox"].change_text("Initialized filled tiles: " + str(round(percentage_filled,2)))
                elif gui_objects["percentage_decrease_button"].is_pressed(event) == 1:
                    if percentage_filled > 0.01:
                        percentage_filled -= 0.01
                        gui_objects["percentage_textbox"].change_text("Initialized filled tiles: " + str(round(percentage_filled,2)))
                elif gui_objects["start_game"].is_pressed(event) == 1:
                    game_started = True
                    gui_objects["start_game"].change_text("Another round!")
        
        draw_all_gui(gui_objects, screen)
        draw_all_field(grid)
        pygame.display.flip()
    
    game(gui_objects, do_visualize, percentage_filled, grid)

def game(gui_objects, do_visualize, percentage_filled, grid = []):
    is_solved = False

    if(len(grid) == 0):             #In first game round, grid is passed from the initialization, in all subsequent rounds, grid is created here, because it needs to be cleared before each round
        screen.fill((255,255,255))
        grid = draw_grid()

    draw_all_gui(gui_objects, screen)
    draw_all_field(grid)
    pygame.display.flip()

    grid = fill_sudoku(grid, do_visualize)
    remove_some_numbers(grid, percentage_filled)
    game_active = True

    gui_objects["solve_button"] = Button(700,200, 300, 30, "Solve")

    while game_active:
        draw_all_gui(gui_objects, screen)
        draw_all_field(grid)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
                pygame.quit()
                return
            else:
                if gui_objects["visualize_button"].is_pressed(event) == 1:
                    do_visualize = not do_visualize
                    if do_visualize:
                        gui_objects["visualize_button"].change_text("Visualization enabled")
                    else:
                        gui_objects["visualize_button"].change_text("Visualization disabled")
                elif gui_objects["start_game"].is_pressed(event) == 1:
                    game(gui_objects, do_visualize, percentage_filled)
                    return
                elif gui_objects["percentage_increase_button"].is_pressed(event) == 1:
                    if percentage_filled < 0.99:
                        percentage_filled += 0.01
                        gui_objects["percentage_textbox"].change_text("Initialized filled tiles: " + str(round(percentage_filled,2)))
                elif gui_objects["percentage_decrease_button"].is_pressed(event) == 1:
                    if percentage_filled > 0.01:
                        percentage_filled -= 0.01
                        gui_objects["percentage_textbox"].change_text("Initialized filled tiles: " + str(round(percentage_filled,2)))
                elif gui_objects["solve_button"].is_pressed(event) == 1:
                    fill_sudoku(grid,do_visualize)
                    is_solved = True
                    on_solve(grid)
                else:
                    if(not is_solved):
                        if(handle_all_fields(grid, event) == 1):
                            if all_fields_filled(grid) == 1:
                                if(solved_correctly(grid)):
                                    on_solve(grid)
                                    is_solved = True


if __name__ == '__main__':
    initialization()