import pygame as pg

pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550

ICON_SIZE = 80
PADDING = 5

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60

font = pg.font.Font(None, 40)
mini_font = pg.font.Font(None, 15)

def load_immage(file, width, height):
    immage = pg.image.load(file).convert_alpha()
    immage = pg.transform.scale(immage, (width, height))
    return immage

def text_render(text):
    return font.render(str(text), True, "black")

class Dog:
    def __init__(self):
        self.kart = load_immage("images/dog.png", 290, 400)
        self.rect = self.kart.get_rect()
        self.rect.topleft = (400, 200)

    def otris(self, screen):
        screen.blit(self.kart, self.rect)

class Button:
    def __init__(self, text, x, y, width=BUTTON_WIDTH, heigt=BUTTON_HEIGHT, text_font=font, func=None):
        self.func = func
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
                self.func()
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.is_pressed = False

class Game:
    def __init__(self):
        self.money = 10
        self.coins_per_second = 1
        self.costs_of_upgrade = {100: False, 1000: False, 5000: False, 10000: False}
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Виртуальный питомец")

        self.happiness = 100
        self.satiety = 100
        self.health = 100

        self.money = 100

        self.backgroun = load_immage("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.happiness_image = load_immage("images/happiness.png", ICON_SIZE, ICON_SIZE)

        self.satiety_image = load_immage("images/satiety.png", ICON_SIZE, ICON_SIZE)

        self.health_image = load_immage("images/health.png", ICON_SIZE, ICON_SIZE)

        self.money_image = load_immage("images/money.png", ICON_SIZE, ICON_SIZE)

        button_x = SCREEN_WIDTH - BUTTON_WIDTH - PADDING

        self.eat_button = Button("Еда", button_x, PADDING + ICON_SIZE)
        self.clothes_button = Button("Одежда", button_x, PADDING + ICON_SIZE * 2)
        self.play_button = Button("Игры", button_x, PADDING + ICON_SIZE * 3)

        self.upgrade_button = Button("Улучшить", SCREEN_WIDTH - ICON_SIZE, 0, width=BUTTON_WIDTH // 3, heigt=BUTTON_HEIGHT // 3, text_font=mini_font, 
func=self.increase_money)

        self.dog = Dog()

        self.buttons = [self.eat_button, self.clothes_button, self.play_button, self.upgrade_button]

        self.INCREASE_COINS = pg.USEREVENT + 1
        pg.time.set_timer(self.INCREASE_COINS, 1000)

        NEW_DAY = pg.USEREVENT + 1
        pg.time.set_timer(NEW_DAY, 86400000)

        self.run()

    def increase_money(self):
        ...

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == self.INCREASE_COINS:
                self.money += 1
     
            if event.type == self.INCREASE_COINS:
                self.money += self.coins_per_second
     
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.money += self.coins_per_second
    
            for button in self.buttons:
                button.is_clicked(event)

            self.eat_button.is_clicked(event)
            self.clothes_button.is_clicked(event)
            self.play_button.is_clicked(event)

    def update(self):
        self.eat_button.update()
        self.clothes_button.update()
        self.play_button.update()
        pass

    def draw(self):
        self.screen.blit(self.backgroun, (0, 0))

        self.screen.blit(self.happiness_image, (PADDING, PADDING))
        self.screen.blit(text_render(self.happiness), (PADDING + ICON_SIZE, PADDING * 6))

        self.screen.blit(self.satiety_image, (PADDING, PADDING + ICON_SIZE))
        self.screen.blit(text_render(self.satiety), (PADDING + ICON_SIZE, PADDING * 6 + ICON_SIZE))

        self.screen.blit(self.health_image, (PADDING, PADDING + ICON_SIZE * 2))
        self.screen.blit(text_render(self.health), (PADDING + ICON_SIZE, PADDING * 6 + ICON_SIZE * 2))

        self.screen.blit(self.money_image, (SCREEN_WIDTH - PADDING - ICON_SIZE, PADDING))
        self.screen.blit(text_render(self.money), (SCREEN_WIDTH - PADDING - ICON_SIZE - 40, PADDING * 6))

        self.eat_button.draw(self.screen)
        self.clothes_button.draw(self.screen)
        self.play_button.draw(self.screen)

        self.dog.otris(self.screen)
        
        pg.display.flip()


if __name__ == "__main__":
    Game()