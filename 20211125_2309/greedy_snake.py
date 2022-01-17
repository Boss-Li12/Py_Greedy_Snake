from tkinter import *
import tkinter as tk
import random
import os

'''
@Row Number of units in the vertical direction
@Column Number of units in the transverse direction
@Unit_size Side length of a single unit
@Height Overall height
@Width Overall length
'''
global Row, Column
Row = 20
Column = 20

# you can set the height and width of the window here
Height = 700
Width = 700

Unit_height_size = Height / Row
Unit_width_size = Width / Column


# the initial direction of the snake
global Direction
Direction = 2

# the speed parameter
global FPS
FPS = 150

# the state of the food
global Have_food
Have_food = 0

# the position of the food
global Food_coord
Food_coord = [0, 0]

# the score
global Score
Score = 0

# the body of the snake
global snake_list
snake_list = [[11, 10], [10, 10], [9, 10]]

#global game_map
#game_map = []




# Dire is a global variable represents forward direction, -1, 1, -2, 2 represents up, down, left, right
def draw_a_unit(canvas, col, row, unit_color="green"):
    # Draw a square of (x1, y1) with reference to the upper left corner
    x1 = col * Unit_width_size
    y1 = row * Unit_height_size
    x2 = (col + 1) * Unit_width_size
    y2 = (row + 1) * Unit_height_size
    # Draw a rectangle formed by diagonal lines from (x0, Y0) to (x1, Y1) with the components in the canvas object
    # outline represents the color of the lines
    canvas.create_rectangle(x1, y1, x2, y2, fill=unit_color, outline="white")


def put_a_backgroud(canvas, color='silver'):
    # Build pixel grid on canvas
    for x in range(Column):
        for y in range(Row):
            draw_a_unit(canvas, x, y, unit_color=color)
            #game_map.append([x, y])


def draw_the_snake(canvas, snake_list, color='green'):
    '''
    @description: Draw snake
    @param {type} snake_list is an integer list, and the default element is list [x, y]
    @return: None
    '''
    for i in snake_list:
        draw_a_unit(canvas, i[0], i[1], unit_color=color)


def snake_move(snake_list, dire):
    # Change the direction through the external binding event
    # Or call the implementation in the default direction
    # return new snake_list
    global Row, Column
    global Have_food
    global Food_coord
    global Score

    new_coord = [0, 0]
    if dire % 2 == 1:
        # if the snake goes up or down
        new_coord[0] = snake_list[0][0]
        new_coord[1] = snake_list[0][1] + dire
    else:
        # if the snake goes left or right
        new_coord[0] = snake_list[0][0] + (int)(dire / 2)
        new_coord[1] = snake_list[0][1]
    # insert the new position into snake_list
    snake_list.insert(0, new_coord)
    '''
    # Conduct a mold taking process to form the effect of crossing the boundary
    for coord in snake_list:
        if coord[0] not in range(Column):
            coord[0] %= Column
            break
        elif coord[1] not in range(Row):
            coord[1] %= Row
            break
    '''
    # if the snake get the food
    if snake_list[0] == Food_coord:
        # Snake length increased by 1
        draw_a_unit(canvas, snake_list[0][0], snake_list[0][1], )
        Have_food = 0
        Score += 10
        str_score.set('Score:' + str(Score))
    else:
        # the snake moves one unit
        draw_a_unit(canvas, snake_list[-1][0], snake_list[-1][1], unit_color="silver")
        draw_a_unit(canvas, snake_list[0][0], snake_list[0][1], )
        snake_list.pop()
    return snake_list


# Ensure that the snake head cannot move in the direction of the original Snake
# and event is the bound keyboard event
def callback(event):
    # make sure the direction is correct
    global Direction
    ch = event.keysym
    if ch == 'Up':
        if snake_list[0][0] != snake_list[1][0]:
            Direction = -1
    elif ch == 'Down':
        if snake_list[0][0] != snake_list[1][0]:
            Direction = 1
    elif ch == 'Left':
        if snake_list[0][1] != snake_list[1][1]:
            Direction = -2
    elif ch == 'Right':
        if snake_list[0][1] != snake_list[1][1]:
            Direction = 2
    return


# Judge whether the snake hit itself or the boundary in the current state
def snake_death_judge(snake_list):
    # return 0 represents alive
    # return 1 represents dead
    # check the head of the snake
    set_list = snake_list[1:]
    if snake_list[0] in set_list:
        return 1
    elif snake_list[0][0] < 0 or snake_list[0][0] >= 20:
        return 1
    elif snake_list[0][1] < 0 or snake_list[0][1] >= 20:
        return 1
    else:
        return 0


def food(canvas, snake_list):
    # create position (x1, y1) randomly
    global Column, Row, Have_food, Food_coord
    #global game_map
    # if food still exist
    if Have_food:
        return
    # if food is eaten by snake, then create new food
    Food_coord[0] = random.choice(range(Column))
    Food_coord[1] = random.choice(range(Row))
    # make sure that new food is not in the body of snake
    while Food_coord in snake_list:
        Food_coord[0] = random.choice(range(Column))
        Food_coord[1] = random.choice(range(Row))
    # create the new food
    draw_a_unit(canvas, Food_coord[0], Food_coord[1], unit_color='red')
    Have_food = 1


move_able = True


def game_loop():
    global FPS
    global snake_list

    win.update()
    food(canvas, snake_list)

    if move_able:
        snake_list = snake_move(snake_list, Direction)

    flag = snake_death_judge(snake_list)
    # Interface for setting the end of the game
    if flag:
        root = Tk()
        root.title('Leave your name')
        #over_lavel = tk.Label(win, text='game over', font=('楷体', 25), width=15, height=1)
        # the gameover_photo should load in the format of gif

        over_lavel = tk.Label(win, image=gameover_photo)
        over_lavel.place(x=0, y=5 * Unit_height_size, bg=None)

        # Get the player's name through the input box
        Label(root, text="Please enter y"
                         "our name：").grid(row=0)
        #v = StringVar()
        # Entry for input
        e = Entry(root)
        e.grid(row=0, column=1, padx=10, pady=5)

        # show the score the rank
        def show1():

            leader_board = Tk()
            Label(leader_board, text="Leader Board").grid(row=0, column=1, padx=10, pady=5)
            Label(leader_board, text="Rank").grid(row=1, column=0, padx=10, pady=5)
            Label(leader_board, text="Name").grid(row=1, column=1, padx=10, pady=5)
            Label(leader_board, text="Score").grid(row=1, column=2, padx=10, pady=5)
            # open rank.txt and display the leader board
            with open('rank.txt', 'r') as f:
                lines = f.readlines()

            currow = 2
            for line in lines:
                curcol = 0
                for s in line.split():
                    Label(leader_board, text=str(s)).grid(row=currow, column=curcol, padx=10, pady=5)
                    curcol += 1
                currow += 1
            # destroy the input window
            root.destroy()

        # show the update rank and store it
        def show2():
            curname = e.get()

            # open rank.txt and display the leader board
            with open('rank.txt', 'r') as f:
                lines = f.readlines()

            # gather the rank data
            ranklist = []
            for line in lines:
                count = 0
                name = ""
                score = -1
                for s in line.split():
                    if count == 1:
                        name = s
                    elif count == 2:
                        score = int(s)
                    count += 1
                if score != -1:
                    ranklist.append((name, score))
            # append the new (name,score)
            ranklist.append((curname, Score))
            ranklist.sort(key=lambda k: k[1], reverse=True)

            # update the rank.txt
            f = open("rank.txt", 'w')
            for i in range(len(ranklist)):
                if i < 5:
                    new_context = str(i + 1) + " " + ranklist[i][0] + " " + str(ranklist[i][1]) + '\n'
                    f.write(new_context)
            f.close()

            # get the updated txt and show it
            with open('rank.txt', 'r') as f:
                lines = f.readlines()

            leader_board = Tk()
            Label(leader_board, text="Leader Board").grid(row=0, column=1, padx=10, pady=5)
            Label(leader_board, text="Rank").grid(row=1, column=0, padx=10, pady=5)
            Label(leader_board, text="Name").grid(row=1, column=1, padx=10, pady=5)
            Label(leader_board, text="Score").grid(row=1, column=2, padx=10, pady=5)

            currow = 2
            for line in lines:
                curcol = 0
                for s in line.split():
                    Label(leader_board, text=str(s)).grid(row=currow, column=curcol, padx=10, pady=5)
                    curcol += 1
                currow += 1
            # destroy the input window
            root.destroy()




        # add two buttons
        Button(root, text="just leave", width=10, command=show1) \
            .grid(row=2, column=0, sticky=W, padx=10, pady=5)
        Button(root, text="confirm my score", width=15, command=show2) \
            .grid(row=2, column=1, sticky=E, padx=10, pady=5)



        return

    win.after(FPS, game_loop)


from time import sleep
stop = False
hide = False

# Set pause and cheating functions
def stop_and_cheat_and_boss(event):
    global stop
    global move_able

    if event.keycode == 27:     # ESC: pause
        move_able = False
        stop = True
        def start(event):
            global move_able
            global stop
            #print(f"INPUT:{event.char},ASCII:{event.keycode}")

            if event.keycode == 27 and stop:
                stop = False
                move_able = True
                #print("start")

        canvas.bind("<Key>", start)

        while stop:
            #print(stop)
            sleep(0.05)
            win.update()

    elif event.keycode == 67:  # c: cheat
        global snake_list
        # cut 3 units from the body of the snake
        # make sure the length of the snake is no less than 3 units
        if len(snake_list) > 5:
            for i in range(3):
                draw_a_unit(canvas, snake_list[-1][0], snake_list[-1][1], unit_color="silver")
                snake_list.pop()

    elif event.keycode == 66:  #b: hide
        global hide
        global hide_canvas

        if hide is False:
            hide_canvas = Canvas(win, width=Width, height=Height + 2 * Unit_height_size)
            hide_canvas.create_image(0, 0, image = code_photo, anchor = 'nw')
            hide_canvas.place(x=0, y=0)
            win.title("python code")
            # stop the snake
            move_able = False
            hide = True
        else:
            hide_canvas.destroy()
            win.title('Greedy Snake')
            # free the snake
            move_able = True
            hide = False







# press Enter to begin
def check_begin():
    global begin

    def start(event):
        global begin
        if event.keycode == 13: # press Enter to begin
            begin = True

    canvas.bind("<Key>", start)
    while begin is False:
        sleep(0.05)
        win.update()

# the introduction button
def introduction():
    intro = Tk()
    intro.title("Introduction")
    Label(intro, text="Press 'Enter' to begin").grid(row=0, column=0, padx=10, pady=5)
    Label(intro, text="Pause/uppause: Press 'ESC'").grid(row=1, column=0, padx=10, pady=5)
    Label(intro, text="Boss: Press 'b' to show/hide the python code").grid(row=2, column=0, padx=10, pady=5)
    Label(intro, text="Cheat: Press 'c' to decrease the length of the snake and  the body is at least three squares long").grid(row=3, column=0, padx=10, pady=5)
    Label(intro, text="There is a save/Load button in the upper left corner, you can pause the game and choose to save.\nThen you can choose to load the saved game or press the 'Enter' to begin a new game next time.").grid(row=4, column=0, padx=10, pady=5)

# callback func for save
def save():
    # update the state.txt
    f = open("state.txt", 'w')

    new_context = str(Score) + '\n'
    f.write(new_context)

    for pos in snake_list:
        new_context = str(pos[0]) + ' ' + str(pos[1]) + '\n'
        f.write(new_context)

    f.close()


# callback func for load
def load():
    global begin
    global Score
    global snake_list
    global temp
    #load the state.txt
    f = open("state.txt", 'r')
    lines = f.readlines()
    f.close()

    state_snake_list = []
    for i in range(len(lines)):
        line = lines[i].split()
        if i == 0:
            Score = int(line[0])
        else:
            state_snake_list.append([int(line[0]), int(line[1])])

    snake_list = state_snake_list
    put_a_backgroud(canvas)
    draw_the_snake(canvas, snake_list)
    str_score.set('score:' + str(Score))
    score_label.place(x=Width / 3, y=Height)




# initialize the canvas
win = tk.Tk()
win.minsize(Width, int(Height + 4 * Unit_height_size))
win.maxsize(Width, int(Height + 4 * Unit_height_size))
win.title('Greedy Snake')
# 2 more units for height to display the score
canvas = tk.Canvas(win, width=Width, height=Height + 2 * Unit_height_size)
canvas.pack()
# boss-key canvas
global hide_canvas
# display the score
str_score = tk.StringVar()
score_label = tk.Label(win, textvariable=str_score, font=('Times New Roman', 20), width=15, height=1)

# load the pictures
global gameover_photo
# https://pixabay.com/zh/photos/game-over-game-over-computer-2720584/
gameover_photo = PhotoImage(file="gameover.gif")

global code_photo
code_photo = PhotoImage(file="code.gif")


# display the current score
# initialization
str_score.set('score:' + str(Score))
score_label.place(x= Width / 3, y=Height)
put_a_backgroud(canvas)
draw_the_snake(canvas, snake_list)

# add a introduction button
Button(win, text="introduction", width=10, command=introduction) \
    .place(x= 0, y=Height)


# create a menu
menubar = tk.Menu(win)
mymenu = tk.Menu(menubar, tearoff=False)
mymenu.add_command(label="save", command=save)
mymenu.add_command(label="load", command=load)
menubar.add_cascade(label="Please select:", menu=mymenu)
win.config(menu=menubar)


# bind the keyPress event and callback function
canvas.focus_set()
canvas.bind("<KeyPress-Left>", callback)
canvas.bind("<KeyPress-Right>", callback)
canvas.bind("<KeyPress-Up>", callback)
canvas.bind("<KeyPress-Down>", callback)
# canvas.bind("<Key>", do_stop)

# start the game
begin = False
check_begin()
game_loop()


while True:
    if not stop:
        win.update()
        canvas.bind("<Key>", stop_and_cheat_and_boss)
    else:
        sleep(0.02)

