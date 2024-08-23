import pygame as pg

pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550

ICON_SIZE = 80
PADDING = 5

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60

DOG_WIDTH = 310
DOG_HEIGHT = 500

MENU_NAV_XPAD = 90
MENU_NAV_YPAD = 130

font = pg.font.Font(None, 40)
mini_font = pg.font.Font(None, 15)

def text_render(text):
    return font.render(str(text), True, "black")

class Dog:
    def __init__(self):
        self.kart = load_immage("images/dog.png", DOG_WIDTH, DOG_HEIGHT)
        self.rect = self.kart.get_rect()
        self.rect.topleft = (400, 200)

    def otris(self, screen):
        screen.blit(self.kart, self.rect)

def load_immage(file, width, height):
    immage = pg.image.load(file).convert_alpha()
    immage = pg.transform.scale(immage, (width, height))
    return immage

class Item:
    def __init__(self, name, price, file):
        self.name = name
        self.price = price
        self.is_using = False
        self.is_bought = False

        self.image = load_immage(file, DOG_WIDTH // 1.7, DOG_HEIGHT // 1.7)
        self.full_image = load_immage(file, DOG_WIDTH, DOG_HEIGHT)

class ClothesMeny:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_immage("images/menu/menu_page.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = load_immage("images/menu/bottom_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_immage("images/menu/bottom_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_immage("images/menu/top_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_immage("images/menu/top_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items = [Item("Синяя футболка", 10, "images/items/blue t-shirt.png"),
                      Item("Ботинки", 50, "images/items/boots.png"),
                      Item("Шляпа", 50, "images/items/hat.png")]
        
        self.current_item = 0

        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.next_button = Button("Вперёд", SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH, SCREEN_HEIGHT - MENU_NAV_YPAD,
                                  width=int(BUTTON_WIDTH // 1.2), heigt=int(BUTTON_HEIGHT // 1.2),
                                  funk=self.to_next)
        
    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1

    def update(self):
        self.next_button.update()

    def is_clicked(self, event):
        self.next_button.is_clicked(event)

    def draw (self, screen):
        screen.blit(self.menu_page, (0, 0))

        screen.blit(self.items[self.current_item].image, self.item_rect)

        if self.items[self.current_item].is_bought:
            screen.blit(self.bottom_label_on, (0, 0))
        else:
            screen.blit(self.bottom_label_off, (0, 0))
        if self.items[self.current_item].is_using:
            screen.blit(self.top_label_on, (0, 0))
        else:
            screen.blit(self.top_label_off, (0, 0))

        self.next_button.draw(screen)

class Button:
    def __init__(self, text, x, y, width=BUTTON_WIDTH, heigt=BUTTON_HEIGHT, text_font=font, funk=None):
        self.funk = funk
        self.idle_image = load_immage("images/button.png", width, heigt)
        self.pressed_image = load_immage("images/button_clicked.png", width, heigt)
        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.text_font = text_font
        self.text = self.text_font.render(str(text), True, "black")
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

        self.is_pressed = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.is_pressed:
                self.image = self.pressed_image
            else :
                self.image = self.idle_image

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                self.funk()
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.is_pressed = False


class Game:
    def __init__(self):

        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Виртуальный питомец")

        self.happiness = 100
        self.satiety = 100
        self.health = 100

        self.money = 100
        self.coins_per_second = 1

        self.costs_of_upgrade = {100: False, 1000: False, 5000: False, 10000: False}

        self.mode = "Main"

        self.background = load_immage("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        
        self.happiness_image = load_immage("images/happiness.png", ICON_SIZE, ICON_SIZE)

        self.satiety_image = load_immage("images/satiety.png", ICON_SIZE, ICON_SIZE)

        self.health_image = load_immage("images/health.png", ICON_SIZE, ICON_SIZE)

        self.money_image = load_immage("images/money.png", ICON_SIZE, ICON_SIZE)

        button_x = SCREEN_WIDTH - BUTTON_WIDTH - PADDING

        self.eat_button = Button("Еда", button_x, PADDING + ICON_SIZE)
        self.clothes_button = Button("Одежда", button_x, PADDING + ICON_SIZE * 2,
                                     funk=self.clothes_menu_on)
        self.play_button = Button("Игры", button_x, PADDING + ICON_SIZE * 3)

        self.upgrade_button = Button("Улучшить", SCREEN_WIDTH - ICON_SIZE, 0,
                                     width=BUTTON_WIDTH // 3, heigt=BUTTON_HEIGHT // 3,
                                     text_font=mini_font, funk=self.increase_money)

        self.buttons = [self.eat_button, self.clothes_button, self.play_button, self.upgrade_button]

        self.clothes_menu = ClothesMeny(self)

        self.INCREASE_COINS = pg.USEREVENT + 1
        pg.time.set_timer(self.INCREASE_COINS, 1000)

        NEW_DAY = pg.USEREVENT + 2
        pg.time.set_timer(NEW_DAY, 86400000)

        self.dog = Dog()

        self.run()

    def clothes_menu_on(self):
        self.mode = "Clothes menu"

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()

    def increase_money(self):
        for ceni in self.costs_of_upgrade:
            kuplino = self.costs_of_upgrade[ceni]
            if kuplino is False and self.money >= ceni:
                self.coins_per_second += 1
                self.money -= ceni
                self.costs_of_upgrade[ceni] = True
                break

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.mode = "Main"

            if event.type == self.INCREASE_COINS:
                self.money += self.coins_per_second

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.money += self.coins_per_second

            for knopka in self.buttons:
                knopka.is_clicked(event)
            self.clothes_menu.is_clicked(event)

    def update(self):
        for knopka in self.buttons:
            knopka.update()

        self.clothes_menu.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.happiness_image, (PADDING, PADDING))
        self.screen.blit(text_render(self.happiness), (PADDING + ICON_SIZE, PADDING * 6))
        
        self.screen.blit(self.satiety_image, (PADDING, PADDING + ICON_SIZE))
        self.screen.blit(text_render(self.satiety), (PADDING + ICON_SIZE, PADDING * 6 + ICON_SIZE))

        self.screen.blit(self.health_image, (PADDING, PADDING + ICON_SIZE * 2))
        self.screen.blit(text_render(self.health), (PADDING + ICON_SIZE, PADDING * 6 + ICON_SIZE * 2))

        self.screen.blit(self.money_image, (SCREEN_WIDTH - PADDING - ICON_SIZE, PADDING))
        self.screen.blit(text_render(self.money), (SCREEN_WIDTH - PADDING - ICON_SIZE - 40, PADDING * 6))

        for knopka in self.buttons:
            knopka.draw(self.screen)

        self.dog.otris(self.screen)

        if self.mode == "Clothes menu":
            self.clothes_menu.draw(self.screen)

        pg.display.flip()

if __name__ == "__main__":
    Game()