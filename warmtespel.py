from kaspersmicrobit import KaspersMicrobit
from tkinter import *
import random
import time

MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'


class Snow:
    def __init__(self, canvas):
        self.coordinates = None
        self.canvas = canvas
        self.snow = PhotoImage(file='sneeuw.gif')
        self.image = self.canvas.create_image(random.randint(1, 1000), random.randint(-1000, 0), image=self.snow, anchor='nw')

    def move(self):
        self.canvas.move(self.image, random.randint(-3, 3), 1)
        self.coordinates = canvas.coords(self.image)
        if self.coordinates[1] >= 1000:
            self.canvas.move(self.image, random.randint(-500, 500), -1000)


class Attaks:
    def __init__(self, canvas, fm, penguin):
        self.ijsbg = None
        self.lijn = None
        self.pinguin = None
        self.coordinates_f = None
        self.canvas = canvas
        self.penguin = penguin
        self.fm = fm

    def __del__(self):
        self.canvas.delete(self.lijn)
        
    def water(self):
        self.coordinates_f = list(self.canvas.coords(self.fm))
        self.pinguin = list(self.canvas.coords(self.penguin))
        if (abs(self.coordinates_f[0] - self.pinguin[0]) <= 50):
        #   or (abs(self.coordinates_f[1] - self.pinguin[1]) <= 50) \
        #   or (abs(self.coordinates_f[2] - self.pinguin[2]) <= 50) \
        #   or (abs(self.coordinates_f[3] - self.pinguin[3]) <= 50):
            self.lijn = self.canvas.create_line(self.coordinates_f, self.coordinates_f, self.pinguin, self.pinguin, fill='blue')
        else:
            self.lijn = self.canvas.create_text(400, 250, text='het floremonster is te ver weg', fill='red')

    def ijs(self):
        self.ijsbg = PhotoImage(file='ijs.gif')


class Pinguin:
    def __init__(self, canvas):
        self.x = 0
        self.y = 0
        self.canvas = canvas
        self.images = [
            PhotoImage(file='pinguingroot.gif'),
            PhotoImage(file='stappinguingroot.gif'),
            PhotoImage(file='stappinguin2groot.gif')
        ]
        self.image = canvas.create_image(500, 500, image=self.images[0], anchor='nw')
        self.image_add = 0

    def animate(self):
        if self.x != 0 or self.y != 0:
            self.image_add += 1
            self.canvas.itemconfig(self.image, image=self.images[self.image_add])
            if self.image_add >= len(self.images) - 1:
                self.image_add = 0
        else:
            self.canvas.itemconfig(self.image, image=self.images[0])
        self.canvas.move(self.image, self.x, self.y)

    def move(self):
        self.animate()
        self.canvas.move(self.image, self.x, self.y)

    def turn_left(self):
        self.x = -2

    def turn_right(self):
        self.x = 2

    def up(self):
        self.y = -2

    def down(self):
        self.y = 2


class Floormonster:
    def __init__(self, canvas):
        self.canvas = canvas
        self.images = [
                PhotoImage(file='floor-monstergroot.gif'),
                PhotoImage(file='floor-monster2groot.gif'),
            ]
        self.image = self.canvas.create_image(500, 800, image=self.images[0], anchor='nw')
        self.image_add = 0
        self.tijd = 0

    def animate(self):
        self.tijd += 1
        if self.tijd == 10:
            self.tijd = 0
            self.image_add += 1
            if self.image_add == 2:
                self.image_add = 0
            self.canvas.itemconfig(self.image, image=self.images[self.image_add])


def knop_A(event):
    pinguin.turn_left()


def knop_B(event):
    pinguin.turn_right()


def pinguin_up(event):
    pinguin.up()


def pinguin_down(event):
    pinguin.down()


def pinguin_keyup(event):
    pinguin.y = 0


def button_up(event):
    pinguin.x = 0


def dis():
    microbit1.disconnect()
    tk.destroy()


def water2(a):
    a.water()


def water(event):
    a = Attaks(canvas, f.image, pinguin.image)
    water2(a)
    # time.sleep(0.01)
    # del a


microbit1 = KaspersMicrobit('E3:7E:99:0D:C1:BA')
microbit1.connect()
microbit1.buttons.on_button_a(press=knop_A, release=button_up)
microbit1.buttons.on_button_b(press=knop_B, release=button_up)
temp = int(microbit1.temperature.read())
tk = Tk()
tk.title("spel")
tk.resizable(False, False)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=1000, height=1000, bd=0, highlightthickness=0)
if temp - 25 <= 0:
    bg = PhotoImage(file='donker.gif')
else:
    bg = PhotoImage(file='licht.gif')
canvas.create_image(0, 0, image=bg, anchor='nw')
canvas.pack()
tk.update()
pinguin = Pinguin(canvas)
f = Floormonster(canvas)


canvas.bind_all('<KeyPress-Up>', pinguin_up)
canvas.bind_all('<KeyPress-Down>', pinguin_down)
canvas.bind_all('<KeyPress-Left>', knop_A)
canvas.bind_all('<KeyPress-Right>', knop_B)
canvas.bind_all('<KeyRelease-Up>', pinguin_keyup)
canvas.bind_all('<KeyRelease-Down>', pinguin_keyup)
canvas.bind_all('<KeyRelease-Left>', button_up)
canvas.bind_all('<KeyRelease-Right>', button_up)
canvas.bind_all('<w>', water)
tk.protocol("WM_DELETE_WINDOW", dis)
snowflakes = []

if temp - 25 <= 0:
    for x in range(0, 1000):
        snow = Snow(canvas)
        snowflakes.append(snow)

delete = 0
while 1:
    delete += 1
    if temp - 25 <= 0 and len(snowflakes) == 0:
        for x in range(0, 1000):
            snow = Snow(canvas)
            snowflakes.append(snow)
    if temp - 25 <= 0:
        for x in snowflakes:
            x.move()
    pinguin.animate()
    f.animate()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
