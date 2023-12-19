import random
from threading import Thread
import pygame
from kaspersmicrobit import KaspersMicrobit
from kaspersmicrobit.services.accelerometer import AccelerometerData

MICROBIT_BLUETOOTH_NIEUW = 'E3:7E:99:0D:C1:BA'


class Aanvallen:
    def __init__(self):
        self.run = False
        self.image_rect = None
        self.image = None
        self.vijand = None
        self.position = None
        self.aanvallen = []
        self.gebotst = []

    def wijzer(self, vijand, position):
        angle = random.randint(0, 360)
        self.run = True
        uitrekken = True
        image_size = (20, 10)
        self.position = position
        while self.run:
            self.aanvallen = []
            self.image = pygame.image.load('wijzer.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, image_size)

            if uitrekken:
                image_size = (image_size[0], image_size[1] + 10)
            else:
                image_size = (image_size[0], image_size[1] - 10)
            if image_size[1] >= 800:
                uitrekken = False
            elif image_size[1] <= 10:
                uitrekken = True
                angle = random.randint(0, 360)

            cursor_rect = self.image.get_rect(center=self.position)

            # rotated image surface
            self.image = pygame.transform.rotate(self.image, angle)
            self.image_rect = self.image.get_rect(center=cursor_rect.center)
            self.aanvallen.append((self.image, self.image_rect))
            clock.tick(50)
        self.image_rect = None
        self.image = None
        self.vijand = None
        self.position = None
        self.aanvallen = []
        self.gebotst = []

    def borden(self, vijand, position):
        self.run = True
        self.position = position
        self.image = pygame.image.load('vuilbord.png').convert_alpha()
        aantal = 0
        while self.run:
            aantal += 1
            for x in range(len(self.aanvallen)):
                cursor_rect = self.image.get_rect(
                    center=pygame.Vector2(random.randint(self.position.x - 50, self.position.x + 170),
                                          random.randint(self.position.y - 50, self.position.y + 170)))
                self.image_rect = self.image.get_rect(center=cursor_rect.center)
                self.aanvallen[x] = (self.image, self.image_rect)
            if aantal == 16:
                cursor_rect = self.image.get_rect(
                    center=pygame.Vector2(random.randint(self.position.x - 50, self.position.x + 170),
                                          random.randint(self.position.y - 50, self.position.y + 170)))
                self.image_rect = self.image.get_rect(center=cursor_rect.center)
                self.aanvallen.append((self.image, self.image_rect))
                aantal = 0
            pygame.time.wait(125)
        self.image_rect = None
        self.image = None
        self.vijand = None
        self.position = None
        self.aanvallen = []
        self.gebotst = []

    def stront(self, vijand, position):
        self.run = True
        self.position = position
        self.image = pygame.image.load('stont.png').convert_alpha()
        while self.run:
            if len(self.gebotst):
                for x in self.gebotst:
                    if x in self.aanvallen:
                        self.aanvallen.remove(x)
                self.gebotst = []
            cursor_rect = self.image.get_rect(center=self.position)
            self.image_rect = self.image.get_rect(center=cursor_rect.center)
            self.aanvallen.append((self.image, self.image_rect))
            pygame.time.wait(2000)
        self.image_rect = None
        self.image = None
        self.vijand = None
        self.position = None
        self.aanvallen = []
        self.gebotst = []

    def geluid(self, vijand, position):
        self.run = True
        self.position = position
        self.image = pygame.image.load('gluid.png').convert_alpha()
        while self.run:
            self.aanvallen = []
            cursor_rect = self.image.get_rect(center=pygame.Vector2(self.position.x, self.position.y))
            self.image_rect = self.image.get_rect(center=cursor_rect.center)
            self.aanvallen.append((self.image, self.image_rect))
            clock.tick(60)
        self.image_rect = None
        self.image = None
        self.vijand = None
        self.position = None
        self.aanvallen = []
        self.gebotst = []


class Pinguin:
    def __init__(self):
        self.monster = None
        self.image = pygame.image.load("pinguin.png").convert_alpha()
        self.direction = pygame.Vector2()
        self.position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.leven = 1000
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = self.font.render('1000', True, (0, 0, 0))
        self.geraakt = False
        self.schiet = False

    def add_monster(self, monster):
        self.monster = monster

    def move(self):
        self.text = self.font.render(str(self.leven), True, (0, 0, 0))
        new_position = self.position + self.direction
        self.position.x = pygame.math.clamp(new_position.x, 8, screen.get_width() - 8)
        self.position.y = pygame.math.clamp(new_position.y, 8, screen.get_height() - 8)
        screen.blit(self.image, self.position)
        screen.blit(self.text, (self.position.x, self.position.y-20))
        if self.schiet:
            pygame.draw.line(screen, (0, 0, 255),
                             [self.position.x + 15, self.position.y + 23],
                             [self.monster.position.x + 60, self.monster.position.y + 60], 5)
        for x in self.monster.aanvallen:
            if self.raak_ik_monster(x):
                self.geraakt = True

    def raak_ik_monster(self, aanval_pos):
        aanval_pos = (aanval_pos[0].x, aanval_pos[0].y, aanval_pos[1].x, aanval_pos[1].y)
        pos = (self.position.x, self.position.y, self.position.x+31, self.position.y+46)
        if aanval_pos[0] <= pos[2] <= aanval_pos[2]\
                or (aanval_pos[0] <= pos[0] <= aanval_pos[2]):
            if (aanval_pos[1] <= pos[3] <= aanval_pos[3]) \
                    or (aanval_pos[1] <= pos[1] <= aanval_pos[3]):
                return True
        return False

    def aanval(self, sender):
        self.schiet = True
        self.monster.leven -= 1


class Monster:
    def __init__(self, pinguin):
        self.thread = None
        self.aanvallen = []
        self.image_add = 0
        self.tijd = 0
        self.monster = 0
        self.aanvallen_monsters = Aanvallen()
        self.monsters = [{"images": [pygame.image.load("corona.png"), pygame.image.load("corona2.png")],
                                    "leven": 10, "aanval": None, "naam": "corona", "snelheid": 1},
                         {"images": [pygame.image.load("klok.png"), pygame.image.load("klok.png")],
                          "leven": 10, "aanval": self.aanvallen_monsters.wijzer, "naam": "klok", "snelheid": 2},
                         {"images": [pygame.image.load("afwasmonster.png"), pygame.image.load("afwasmonster.png")],
                            "leven": 10, "aanval": self.aanvallen_monsters.borden, "naam": "afwas", "snelheid": 1},
                         {"images": [pygame.image.load("box.png"), pygame.image.load("box.png")],
                          "leven": 10, "aanval": self.aanvallen_monsters.geluid, "naam": "box", "snelheid": 1.5},
                         {"images": [pygame.image.load("hond_en_man.png"), pygame.image.load("hond_en_man.png")],
                          "leven": 10, "aanval": self.aanvallen_monsters.stront, "naam": "hond", "snelheid": 1}
                         ]
        self.position = pygame.Vector2(600, 640)
        self.position2 = pygame.Vector2(600+self.monsters[0]["images"][0].get_width(), 640+self.monsters[0]["images"][0].get_width())
        self.pinguin = pinguin
        self.leven = 10
        self.aanvallen.append((self.position, self.position2))
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = self.font.render('100', True, (0, 0, 0))

    def move(self):
        snelheid = self.monsters[self.monster]["snelheid"]
        self.text = self.font.render(str(self.leven), True, (0, 0, 0))
        self.tijd += 1
        if self.tijd == 20:
            self.tijd = 0
            self.image_add += 1
            if self.image_add == 2:
                self.image_add = 0
        if (self.pinguin.position.x - self.position.x) < 0:
            self.position.x -= snelheid
        else:
            self.position.x += snelheid
        if (self.pinguin.position.y - self.position.y) < 0:
            self.position.y -= snelheid
        else:
            self.position.y += snelheid
        self.position2.x = self.position.x + self.monsters[self.monster]["images"][self.image_add].get_width()
        self.position2.y = self.position.y+ self.monsters[self.monster]["images"][self.image_add].get_height()
        self.aanvallen = []
        self.aanvallen.append((self.position, self.position2))
        screen.blit(self.monsters[self.monster]["images"][self.image_add].convert_alpha(), (self.position.x, self.position.y))
        screen.blit(self.text, (self.position.x, self.position.y - 20))
        self.aanvallen_monsters.position = pygame.Vector2(self.position.x+(self.monsters[self.monster]["images"][self.image_add].get_width()/2),
                                                    self.position.y+(self.monsters[self.monster]["images"][self.image_add].get_height()/2))
        if len(self.aanvallen_monsters.aanvallen):
            for aanval in self.aanvallen_monsters.aanvallen:
                self.aanvallen.append((pygame.Vector2(aanval[1].topleft), pygame.Vector2(aanval[1].bottomright)))
                screen.blit(aanval[0], aanval[1].topleft)
                if self.raakt_aanval(aanval):
                    self.aanvallen_monsters.gebotst.append(aanval)
        if self.leven <= 0:
            self.position = pygame.Vector2(600, 640)
            self.aanvallen_monsters.run = False
            if self.thread:
                self.thread.join()
            if len(self.monsters) > self.monster+1:
                self.monster+=1
            self.leven = self.monsters[self.monster]["leven"]
            if self.monsters[self.monster]["aanval"]:
                self.thread = Thread(target=self.monsters[self.monster]["aanval"], args=(pinguin.position,
                                                        pygame.Vector2(self.position.x+(self.monsters[self.monster]["images"][self.image_add].get_width()/2),
                                                        self.position.y+(self.monsters[self.monster]["images"][self.image_add].get_height()/2))))
                self.thread.start()

    def raakt_aanval(self, aanval_pos):
        aanval_pos = (aanval_pos[1].topleft[0], aanval_pos[1].topleft[1], aanval_pos[1].bottomright[0], aanval_pos[1].bottomright[1])
        pos = (self.pinguin.position.x, self.pinguin.position.y, self.pinguin.position.x + 31, self.pinguin.position.y + 46)
        if aanval_pos[0] <= pos[2] <= aanval_pos[2] \
                or (aanval_pos[0] <= pos[0] <= aanval_pos[2]):
            if (aanval_pos[1] <= pos[3] <= aanval_pos[3]) \
                    or (aanval_pos[1] <= pos[1] <= aanval_pos[3]):
                return True
        return False


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

pinguin = Pinguin()
monster = Monster(pinguin)
pinguin.add_monster(monster)
achtergrond = pygame.image.load("achtergrond.png").convert_alpha()

def thread():
    while pinguin.leven > 0:
        if pinguin.geraakt:
            pinguin.leven -= 10
            pinguin.geraakt = False
        pinguin.schiet = False
        pygame.time.wait(500)


def accelerometer_data(data: AccelerometerData):
    pinguin.direction.x = data.x / 100
    pinguin.direction.y = data.y / 100


with KaspersMicrobit(MICROBIT_BLUETOOTH_NIEUW) as microbit:
    microbit.accelerometer.notify(accelerometer_data)
    microbit.buttons.on_button_a(press=pinguin.aanval)
    microbit.buttons.on_button_b(press=pinguin.aanval)
    Thread(target=thread).start()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(achtergrond, (0, 0))

        monster.move()
        pinguin.move()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
