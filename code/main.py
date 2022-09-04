from calendar import c
from dis import dis
from multiprocessing.spawn import is_forking
from re import S
from turtle import window_height
import pygame
from sys import displayhook, exit
import random


pygame.init()
clock = pygame.time.Clock()

#параметры окна
win_height = 720
win_width = 1280

#скорость движения заднего фона
moving_speed = 3

#стартовая точка паука
spider_start_pos = (100,250)


#создание игрового окна
window = pygame.display.set_mode((win_width,win_height))

#загружаем задний фон
bg_img = pygame.transform.scale(pygame.image.load("./media/img/background.png"),(win_width,win_height))

#загружаем изображения паука
spider_img = [pygame.image.load("./media/img/hero/1.png"),
            pygame.image.load("./media/img/hero/2.png"),
            pygame.image.load("./media/img/hero/3.png")]

#загружаем изображения(кадры)дома
scrap_top = pygame.transform.scale(pygame.image.load("./media/img/skyscraper/fire.png"),(135,600))
scrap_bot = pygame.transform.scale(pygame.image.load("./media/img/skyscraper/scape_bot.png"),(135,600))

#изображения кнопок
start_btn_img = pygame.transform.scale(pygame.image.load("./media/img/buttons/start_btn.png"),(150,100))




game_paused = False


#класс кнопки

class Button:
    def __init__(self,img,pos):
        self.img = img
        self.x, self.y = pos
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
    def show(self):
        window.blit(self.img,(self.rect.x,self.rect.y))

    def click(self,event):
        global game_paused
        x,y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x,y):
                    game_paused = False




#класс для заднего фона
class Moving_bg(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bg_img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
    def update(self):
        self.rect.x -= moving_speed
        if self.rect.x <= -win_width:
            self.kill()

#класс главного персонажа
class Spider(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = spider_img[0]
       self.rect = self.image.get_rect()
       self.rect.center = spider_start_pos
       self.vel = 0
    

    def update(self,user_input):
        global game_paused
        self.vel += 0.5

        self.rect.y += self.vel

        if user_input[pygame.K_SPACE] and self.rect.y > 35:
            self.vel = -7
        if user_input[pygame.K_ESCAPE]:
            game_paused = True

 
class Scraper(pygame.sprite.Sprite):
    def __init__(self,x,y,image):
       pygame.sprite.Sprite.__init__(self)
       self.image = image
       self.rect = self.image.get_rect()
       self.rect.x, self.rect.y = x, y
    def update(self):
        self.rect.x -= moving_speed
        if self.rect.x <= -win_width:
            self.kill()


#функция перевірки дотику спрайтів
def collide_check(spider,skyscrap):
    global game_paused
    if pygame.sprite.groupcollide(spider,skyscrap,0,1):
        game_paused = True



#функция выхода
def exit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        start_btn.click(event)

#функция Меню
def menu():
    window.fill((0,0,0))
    start_btn.show()
    pygame.display.update()


    

 
start_btn = Button(start_btn_img,(580,300))

#главная функция запуска игры с игровым циклом
def main():
    bg_x, bg_y = 0,0
    bg_group = pygame.sprite.Group()
    bg_group.add(Moving_bg(bg_x,bg_y))

    spider = pygame.sprite.GroupSingle()
    spider.add(Spider())

    skyscrap = pygame.sprite.Group()

    skyscrap_spawner = 0

    run = True
    while run:
        exit_game()
        if game_paused:
            menu()
        else:
        
            collide_check(spider,skyscrap)

            user_input = pygame.key.get_pressed()

            if len(bg_group) <= 2:
                bg_group.add(Moving_bg(win_width,bg_y))

            bg_group.draw(window)
            spider.draw(window)
            skyscrap.draw(window)


            if skyscrap_spawner >=180:
                x_top_scrap, x_bottom_scrap = 1280,1280
                y_top_scrap = random.randint(-500,-200)
                y_bottom_scrap = y_top_scrap+230+600
                skyscrap.add(Scraper(x_top_scrap,y_top_scrap,scrap_top))
                skyscrap.add(Scraper(x_bottom_scrap,y_bottom_scrap,scrap_bot))
                skyscrap_spawner = 0

            skyscrap_spawner += 1

            skyscrap.update()
            bg_group.update()
            spider.update(user_input)

            

            clock.tick(60)
            pygame.display.update()

main()