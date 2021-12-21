import math
import random
import webbrowser

from song_list import SONGS, ALARM
import pygame
from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
pygame.init()
check_mark = ''
BREAK_COUNTS = ''
PINK = "#e2979c"
RED = "#FADBD8"
DARK_RED = "#ff0000"
GREEN = "#9bdeac"
background_colour = "#000"
DARK_YELLOW = "#BCA136"
DARK_GREEN = "#007500"
FONT_NAME = "Arial"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
rep = 0
play = True
pos = 0
paused = False
timer = None


# ---------------------------- PLAY MUSIC -------------------------------- #
# Stop playing the current song
def music_stop():
    global pos
    pygame.mixer.music.stop()
    pos = -2


def music_on():
    global pos
    pos = 0
    if pos == 0:
        pygame.mixer.music.load(random.choice(SONGS))
        pygame.mixer.music.play(loops=0)
        check_if_finished()


def check_if_finished():
    global pos, paused
    if pos != -2:
        if not pygame.mixer.music.get_busy() and paused == False:
            window.after(ms=1, func=music_on)
        window.after(ms=1, func=check_if_finished)


# Pause and unpause the current song
def music_pause():
    global paused
    # pause
    if not paused:
        pygame.mixer.music.pause()
        paused = True
    # unpause
    else:
        pygame.mixer.music.unpause()
        paused = False


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global rep
    window.after_cancel(timer)
    text.config(text="Timer")
    rep = 0
    current_image.config(file=coffee_image)
    canvas.itemconfig(canvas_text, text="00:00")
    check_tick.config(text="")
    start_button.config(state=NORMAL)
    restart_button.config(state=DISABLED)
    # action()


def alarm():
    global pos
    pygame.mixer.init()
    pygame.mixer.music.load(ALARM)
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play()
    pos = -2


# ---------------------------- TIMER MECHANISM ------------------------------- #


def action():
    global rep, CHECKMARK, check_mark
    rep += 1
    if rep != 1:
        alarm()
    if rep == 8:
        check()
        check_mark = ""
        count_down(LONG_BREAK_MIN * 50)
        text.config(text="LONG BREAK", fg=DARK_YELLOW)
        current_image.config(file=coffee_image)
        rep = 0
    elif rep % 2 == 0:
        count_down(SHORT_BREAK_MIN * 60)
        text.config(text="BREAK", fg=DARK_GREEN)
        current_image.config(file=listen_music)
        check()
    else:
        count_down(WORK_MIN * 60)
        text.config(text="STUDY", fg="#fff")
        current_image.config(file=computer)

    restart_button.config(state=NORMAL)
    start_button.config(state=DISABLED)
    window.attributes('-topmost', 0)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def count_down(count):
    global check_mark
    remain_min = math.floor(count / 60)
    remain_sec = count % 60
    if remain_sec < 10:
        remain_sec = f"0{remain_sec}"
    canvas.itemconfig(canvas_text, text=f"{remain_min}:{remain_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    elif count == 0:
        action()


def check():
    global check_mark
    check_mark += " ✔ "
    check_tick.config(text=check_mark)


def help_():
    # add absolute path of the html file in the template folder
    webbrowser.open('C:/Users/chami/OneDrive/Desktop/POMOmusic/templates/help.html')


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
menu_bar = Menu(window)
window.title("POMOmusic")
window.config(padx=20, pady=20, bg=background_colour)
window.resizable(width=False, height=False)

coffee_image = "images/love coffee-modified.png"
listen_music = "images/music.png"
computer = "images/computer-removebg-modified.png"
# Creating the canvas and the time
canvas = Canvas(width=300, height=350, bg=background_colour, highlightthickness=0)
current_image = PhotoImage(file=coffee_image)
canvas.create_image(150, 110, image=current_image)
canvas.grid(row=1, column=1)
canvas_text = canvas.create_text(150, 250, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))

# Labels
text = Label(text="Timer", font=(FONT_NAME, 35, "bold"), fg=PINK, bg=background_colour, highlightthickness=0)
text.grid(row=0, column=1)

check_tick = Label(text=check_mark, font=(FONT_NAME, 16, "bold"), fg=GREEN, bg=background_colour, highlightthickness=0)
check_tick.grid(row=3, column=1)

# creating player control button images
play_icon = PhotoImage(file="images/play50.png")
pause_icon = PhotoImage(file="images/pause50.png")
stop_icon = PhotoImage(file="images/stop50.png")
info_icon = PhotoImage(file="images/info50.png")
# Buttons
start_button = Button(text="Start Timer", font=(FONT_NAME, 12, "bold"), highlightthickness=0, command=action,
                      borderwidth=0)
start_button.grid(row=2, column=0)
restart_button = Button(text="Restart Timer", font=(FONT_NAME, 12, "bold"), highlightthickness=0, command=reset_timer,
                        borderwidth=0, state=DISABLED)
restart_button.grid(row=2, column=2)

stop_button = Button(image=stop_icon, bg=background_colour, borderwidth=0, command=music_stop)
stop_button.place(x=290, y=350)
play_button = Button(image=play_icon, bg=background_colour, borderwidth=0, command=music_on)
play_button.place(x=205, y=350)
pause_button = Button(image=pause_icon, bg=background_colour, borderwidth=0, command=music_pause)
pause_button.place(x=115, y=350)

# ------------------------------ Top Bar (Menu Section)-------------------- #


file = Menu(menu_bar, tearoff=False)
# File section in the top bar menu
menu_bar.add_cascade(label='File', menu=file)
file.add_command(label='Exit', command=window.quit)
help_me = Menu(menu_bar, tearoff=0)
# Help section in the top bar menu
menu_bar.add_cascade(label='Info', menu=help_me)
# About Us
help_me.add_command(label='About', command=help_)
window.config(menu=menu_bar)

window.mainloop()
