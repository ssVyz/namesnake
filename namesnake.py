# fully handwritten, 07.05.26, dnz

import msvcrt
import sys
import time
import random


### Constants  ###

ARENA_HEIGHT = 10
ARENA_LENGTH = 30


### Game  ###

class App:

    def __init__(self, user_name):
        self.username = user_name
        self.direction = "left"

        self.food = Food(user_name, 10, 5)
        self.screen = Screen()
        self.snake = Snake()
        self.snake.snake_start(self.username[:1])

    def cycle(self, input):
        self.resolve_input_direction(input)
        self.snake.snake_move(self.direction, self.food)
        current_snake = self.snake.get_snake_pos()
        self.screen.refresh(self.get_food_coords(), current_snake)
        self.check_collission(current_snake)


    def get_food_coords(self):
        return (self.food.food_x, self.food.food_y, self.food.letter)
    

    def resolve_input_direction(self, input):
        if input in ["up", "down", "left", "right"]:
            self.direction = input

    def check_collission(self, current_snake):
        if self.snake.head.pos_x == 0 or self.snake.head.pos_x == ARENA_LENGTH or self.snake.head.pos_y == 0 or self.snake.head.pos_y == ARENA_HEIGHT:
            print("You ran into a wall")
            sys.exit(0)

        if self.snake.collides(current_snake) == True:
            print("Your snake just crashed")
            sys.exit(0)


class Screen:

    def __init__(self):
        self.current_screen = None

    def build_screen(self):
        screen_list = []

        screen_list.append("="*ARENA_LENGTH)
        for i in range(0, ARENA_HEIGHT-1):
            screen_list.append(("|" + "."*28 + "|"))
        screen_list.append("="*ARENA_LENGTH)
        return screen_list
    
    def insert_food(self, coords_x, coords_y, letter):
        old_line = self.current_screen[coords_y]
        self.current_screen[coords_y] = old_line[:coords_x] + letter + old_line[coords_x+1:]

    def insert_snake(self, snake_data):
        for part in snake_data:
            self.draw_snake_part(part[0], part[1], part[2])

    def draw_snake_part(self, coords_x, coords_y, letter):
        old_line = self.current_screen[coords_y]
        self.current_screen[coords_y] = old_line[:coords_x] + letter + old_line[coords_x+1:]

    def refresh(self, food_data, snake_data):
        self.clear_screen()
        self.current_screen = self.build_screen()
        self.insert_food(food_data[0], food_data[1], food_data[2])
        self.insert_snake(snake_data)
        self.print_screen(self.current_screen)

    def print_screen(self, screen_list):
        for i in range(0, len(screen_list)):
            print(screen_list[i])

    def clear_screen(self):
        for i in range(0, 10):
            print("")
        

class Snake:

    def __init__(self):
        self.last_x = None
        self.last_y = None
        self.last_bodypart = None

    def snake_start(self, first_letter):
        self.head = Bodypart(first_letter, 20, 5, None)
        self.last_x = self.head.pos_x
        self.last_y = self.head.pos_y

    def get_last_bodypart(self, bodypart):
        if bodypart.next == None:
            self.last_bodypart = bodypart
        else:
            self.get_last_bodypart(bodypart.next)

    def snake_move(self, direction, food):
        self.last_x = self.head.pos_x
        self.last_y = self.head.pos_y
        if direction == "up":
            self.head.pos_y -= 1
        if direction == "down":
            self.head.pos_y += 1
        if direction == "left":
            self.head.pos_x -= 1
        if direction == "right":
            self.head.pos_x += 1
        if self.head.next is not None:
            self.snake_increment(self.head.next)
        if self.head.pos_x == food.food_x and self.head.pos_y == food.food_y:
            self.snake_eat(food.letter)
            food.eat()

    def snake_increment(self, bodypart):
        buffer_x = bodypart.pos_x
        buffer_y = bodypart.pos_y
        bodypart.pos_x = self.last_x
        bodypart.pos_y = self.last_y
        self.last_x = buffer_x
        self.last_y = buffer_y
        if bodypart.next is not None:
            self.snake_increment(bodypart.next)

    def snake_eat(self, letter):
        new_body = Bodypart(letter, self.last_x, self.last_y, None)
        self.get_last_bodypart(self.head)
        self.last_bodypart.set_next(new_body)


    def get_snake_pos(self, bodypart=None):
        if bodypart == None:
            bodypart = self.head
        snake_list = []
        snake_list.append((bodypart.pos_x, bodypart.pos_y, bodypart.letter))
        if bodypart.next is not None:
            return_list = self.get_snake_pos(bodypart.next)
            snake_list.extend(return_list)
        return snake_list
    
    def collides(self, current_snake):
        head_coords_x = current_snake[0][0]
        head_coords_y = current_snake[0][1]
        if len(current_snake) < 3:
            return False
        del current_snake[0]
        del current_snake[0]
        for part in current_snake:
            if part[0] == head_coords_x and part[1] == head_coords_y:
                return True
        return False

    
class Bodypart:

    def __init__(self, letter, pos_x, pos_y, next):
        self.letter = letter
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.next = None

    def set_next(self, new_part):
        self.next = new_part


class Food:

    def __init__(self, user_name, food_x, food_y):
        self.user_name = user_name[1:]
        self.food_x = food_x
        self.food_y = food_y
        self.letter = self.user_name[:1]
        self.current_string = self.user_name[1:]

    def eat(self):
        self.letter = self.current_string[:1]
        self.current_string = self.current_string[1:]
        self.food_x = random.randint(1, ARENA_LENGTH-2)
        self.food_y = random.randint(1, ARENA_HEIGHT-2)


    def get_food_pos(self):
        return (self.food_x, self.food_y, self.letter)

        

### basic functions ###


### Returns the last key pressed (pressing b exits)
def last_key():
    keyhit_list = []
    while msvcrt.kbhit() == True:
        pressed = msvcrt.getch().decode("utf-8")
        if pressed == "b":
            sys.exit()
        keyhit_list.append(pressed)

    if keyhit_list == []:
        return None
    else:
        return keyhit_list[-1]

### Direction resolver
def resolve_direction(keypress):
    if keypress == "w":
        return "up"
    if keypress == "s":
        return "down"
    if keypress == "a":
        return "left"
    if keypress == "d":
        return "right"
    else:
        return None



########################
### entry point ###
########################

def main():

    user_name = input("Your name: ")
    app = App(user_name)


    while True:
        user_input = (resolve_direction(last_key()))
        app.cycle(user_input)
        time.sleep(0.5)


if __name__ == "__main__":
    main()