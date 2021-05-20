import pygame, sys

pygame.init()
win = pygame.display.set_mode((700,750))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 50)
score = 0

bg_img = pygame.image.load('bg1.png')
drive_right = pygame.image.load('car R.png')
drive_left = pygame.image.load('car L.png')
drive_straight = pygame.image.load('car.png')
drive_parked = pygame.image.load('car.png')
bot_right = pygame.image.load('bot R.png')
bot_left = pygame.image.load('bot L.png')
bot_straight = pygame.image.load('bot.png')
bot_parked = pygame.image.load('bot.png')
stop_img = pygame.image.load('stop sign.png')
car_crashed_str = pygame.image.load('car crashed straight.png')
car_crashed_left = pygame.image.load('car crashed left.png')
car_crashed_right = pygame.image.load('car crashed right.png')
smoke = pygame.image.load('smoke.png')


def txt_obj(text, font):
    txt_surface = font.render(text, True, (0,0,0))
    return txt_surface, txt_surface.get_rect()


class Car(object):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.vel = 0.7
        self.height = height
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.parked = True
        self.left = False
        self.right = False
        self.straight = False
        self.speeding = False
        self.back = False
        self.crashed = False

    def draw(self, win):
        if not(self.parked):
            if self.left:
                win.blit(drive_left, (self.x, self.y))
                self.hitbox = (self.x, self.y, self.width + 30, self.height)

            elif self.right:
                win.blit(drive_right, (self.x, self.y))
                self.hitbox = (self.x, self.y, self.width + 30, self.height)

            elif self.straight:
                win.blit(drive_straight, (self.x, self.y))
                self.hitbox = (self.x, self.y, self.width, self.height)
            
            elif self.back:
                win.blit(drive_straight, (self.x, self.y))
                self.hitbox = (self.x, self.y, self.width, self.height)

            elif self.speeding and self.right:
                win.blit(drive_right, (self.x, self.y))
                self.hitbox = (self.x, self.y, self.width, self.height)

        else:
            win.blit(drive_parked, (self.x, self.y))
            self.hitbox = (self.x, self.y, self.width, self.height)

    

        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


    def borders(self):
        if self.x >= 490:
            self.x = 490
        if self.x <= 218:
            self.x = 218

    def update(self):
        self.borders()


class Bot(object):
    def __init__(self, x, y, vel, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.parked = True
        self.left = False
        self.right = False
        self.straight = False
        self.speeding = False
        self.back = False

    def draw(self, win):
        if not(self.parked):
            if self.left:
                win.blit(bot_left, (self.x, self.y))
                self.hitbox = (self.x, self.y, self.width + 30, self.height)

            elif self.right:
                win.blit(bot_right, (self.x, self.y))
                self.hitbox = (self.x, self.y, self.width + 30, self.height)

            elif self.straight:
                win.blit(bot_straight, (self.x, self.y))
                self.hitbox = (self.x, self.y, self.width, self.height)
            
            elif self.back:
                win.blit(bot_straight, (self.x, self.y))
                self.hitbox = (self.x, self.y, self.width, self.height)

            elif self.speeding and self.right:
                win.blit(bot_right, (self.x, self.y))
                self.hitbox = (self.x, self.y, self.width, self.height)


        else:
            win.blit(bot_parked, (self.x, self.y))
            self.hitbox = (self.x, self.y, self.width, self.height)

        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


class StopSign(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        win.blit(stop_img, (self.x, self.y))

        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


class Background(object):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.vel = 0.7

    def draw(self, win):
        win.blit(bg_img, (self.x, self.y))

    def update(self):
        self.borders()

    def borders(self):
        if self.y <= -2880:
            self.y = -2880
        if self.y >= -1:
            self.y = -1


car = Car(300, 375, 55, 120)
bot1 = Bot(400, 375, 0, 66, 125)
bg = Background(-70, -2920)
#stop_sign1 = StopSign(bg.x+500,bg.y+3000, 60,60)

#bg.x+470,bg.y+500

def game():
    global score

    stop_sign1 = StopSign(bg.x+470,bg.y+2500, 60,60)
    stop_sign2 = StopSign(bg.x+548,bg.y+2000, 60,60)

    #objects
    bg.draw(win)
    car.draw(win)
    stop_sign1.draw(win)
    stop_sign2.draw(win)
    bot1.draw(win)
    score += 0.01

    score_surface = game_font.render(f'{int(score)}',True,(255,255,255))
    score_rect = score_surface.get_rect(center = (50,50))
    win.blit(score_surface, score_rect)

    bot_died_surface = game_font.render('BOT DIED!!',True,(255,255,255))
    bot_died_rect = bot_died_surface.get_rect(center = (350,200))

    bg.update()
    car.update()

    bot1.vel = 0.7
    bot1.y -= bot1.vel


    #bot collision movement
    if bot1.hitbox[0] + bot1.hitbox[2] > stop_sign1.hitbox[0] - 25 and bot1.hitbox[0] < stop_sign1.hitbox[0] + stop_sign1.hitbox[2] + 25:
        if bot1.hitbox[1] < stop_sign1.hitbox[1] + 170:
            if car.hitbox[0] > bot1.hitbox[0]:
                bot1.straight = False
                bot1.back = False
                bot1.left = True
                bot1.right = False
                bot1.parked = False
                bot1.speeding = False
                if bot1.left:
                    bot1.x -= bot1.vel

            elif car.hitbox[0] < bot1.hitbox[0]:            
                bot1.straight = False
                bot1.back = False
                bot1.left = False
                bot1.right = True
                bot1.parked = False
                bot1.speeding = False
                if bot1.right:
                    bot1.x += bot1.vel

                '''if bot1.hitbox[0] > 480:
                    bot1.straight = True
                    bot1.back = False
                    bot1.left = False
                    bot1.right = False
                    bot1.parked = False
                    bot1.speeding = False'''


    elif bot1.hitbox[1] + bot1.hitbox[3] < stop_sign1.hitbox[1]:
        bot1.straight = True
        bot1.back = False
        bot1.left = False
        bot1.right = False
        bot1.parked = False
        bot1.speeding = False
        bot1.y += bot1.vel

    if bot1.hitbox[0] + bot1.hitbox[2] > stop_sign2.hitbox[0] - 25 and bot1.hitbox[0] < stop_sign2.hitbox[0] + stop_sign2.hitbox[2] + 25:
        if bot1.hitbox[1] < stop_sign2.hitbox[1] + 170:
            if car.hitbox[0] > bot1.hitbox[0] + 6:
                bot1.straight = False
                bot1.back = False
                bot1.left = True
                bot1.right = False
                bot1.parked = False
                bot1.speeding = False
                bot1.x -= bot1.vel

            elif car.hitbox[0] < bot1.hitbox[0]: 
                if bot1.hitbox[0] - 100 > car.hitbox[0] + car.hitbox[2]:
                    bot1.straight = False
                    bot1.back = False
                    bot1.left = True
                    bot1.right = False
                    bot1.parked = False
                    bot1.speeding = False 
                    bot1.x -= bot1.vel

                else:
                    bot1.straight = True
                    bot1.back = False
                    bot1.left = False
                    bot1.right = False
                    bot1.parked = False
                    bot1.speeding = False


    else:
        bot1.straight = True
        bot1.back = False
        bot1.left = False
        bot1.right = False
        bot1.parked = False
        bot1.speeding = False


    #car collision
    if car.hitbox[1] < stop_sign1.hitbox[1] + stop_sign1.hitbox[3] and car.hitbox[1] + car.hitbox[3] > stop_sign1.hitbox[1]:
        if car.hitbox[0] + car.hitbox[2] > stop_sign1.hitbox[0] and car.hitbox[0] < stop_sign1.hitbox[0] + stop_sign1.hitbox[2]:
            game_over()


    if car.hitbox[1] < stop_sign2.hitbox[1] + stop_sign2.hitbox[3] and car.hitbox[1] + car.hitbox[3] > stop_sign2.hitbox[1]:
        if car.hitbox[0] + car.hitbox[2] > stop_sign2.hitbox[0] and car.hitbox[0] < stop_sign2.hitbox[0] + stop_sign2.hitbox[2]:
            game_over()
                


    #bot collision
    if bot1.hitbox[1] < stop_sign1.hitbox[1] + stop_sign1.hitbox[3] and bot1.hitbox[1] + bot1.hitbox[3] > stop_sign1.hitbox[1]:
        if bot1.hitbox[0] + bot1.hitbox[2] > stop_sign1.hitbox[0] and bot1.hitbox[0] < stop_sign1.hitbox[0] + stop_sign1.hitbox[2]:
            bot1.y += bg.vel
            win.blit(bot_died_surface, bot_died_rect)
    
    '''if bot1.hitbox[1] < stop_sign2.hitbox[1] + stop_sign2.hitbox[3] and bot1.hitbox[1] + bot1.hitbox[3] > stop_sign2.hitbox[1]:
        if bot1.hitbox[0] + bot1.hitbox[2] > stop_sign2.hitbox[0] and bot1.hitbox[0] < stop_sign2.hitbox[0] + stop_sign2.hitbox[2]:
            bot1.y += bg.vel
            win.blit(bot_died_surface, bot_died_rect)'''


    #print('Background: (', bg.x, ',', bg.y, ')')
    #print('Car: (', car.x, ',', car.y, ')')
    #print('Stop Sign: (', stop_sign1.x, ',', stop_sign1.y, ')')

    pygame.display.update()

def menu():

    pygame.display.set_caption('Menu')

    win.blit(bg_img, (-100,0))

    while True:

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()

        level1_btn = pygame.Rect(250, 325, 200, 100)
        level1_btn_text = pygame.font.Font('freesansbold.ttf', 30)
        txt_surf, txt_rect = txt_obj('Level 1', level1_btn_text)
        txt_rect.center = ((250+(200/2)), (325+(100/2)))

        pygame.draw.rect(win, (255, 255, 255), level1_btn)
        win.blit(txt_surf, txt_rect)

        if level1_btn.collidepoint((mx, my)):
            if click:
                level1()

        
        pygame.display.update()


def game_over():

    pygame.display.set_caption('Game Over :(')


    while True:

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if car.straight:
            win.blit(car_crashed_str, (car.x, car.y))
            win.blit(smoke, (car.x+25, car.y-30))

        elif car.left:
            win.blit(car_crashed_left, (car.x, car.y))
            win.blit(smoke, (car.x+25, car.y-20))

        elif car.right:
            win.blit(car_crashed_right, (car.x, car.y))
            win.blit(smoke, (car.x+55, car.y-20))


        mx, my = pygame.mouse.get_pos()

        menu_btn = pygame.Rect(200, 200, 300, 100)
        game_over_btn_text = pygame.font.Font('freesansbold.ttf', 30)
        txt_surf, txt_rect = txt_obj('Back To Menu', game_over_btn_text)
        txt_rect.center = ((200+(300/2)), (200+(100/2)))

        restart_btn = pygame.Rect(200, 350, 300, 100)
        game_over_btn_text = pygame.font.Font('freesansbold.ttf', 30)
        txt_surf1, txt_rect1 = txt_obj('Restart', game_over_btn_text)
        txt_rect1.center = ((200+(300/2)), (350+(100/2)))

        end_surface = game_font.render(':( YOU DIED! :(' ,True,(255,255,255))
        end_rect = end_surface.get_rect(center = (350,155))
        win.blit(end_surface, end_rect)

        pygame.draw.rect(win, (255, 255, 255), menu_btn)
        win.blit(txt_surf, txt_rect)

        #pygame.draw.rect(win, (255, 255, 255), restart_btn)
        #win.blit(txt_surf1, txt_rect1)

        if menu_btn.collidepoint((mx, my)):
            if click:
                menu()

        if restart_btn.collidepoint((mx, my)):
            if click:
                level1()

        
        pygame.display.update()


def level1():
    global score
    score = 0
    car.crashed = False

    bot1.straight = True
    bot1.back = False
    bot1.left = False
    bot1.right = False
    bot1.parked = False
    bot1.speeding = False

    car.x = 300
    bg.y = -2920

    bot1.x = 400
    bot1.y = 375

    pygame.display.set_caption('Level 1')


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()


        if keys[pygame.K_w]:
            bg.y += bg.vel
            bot1.y += bg.vel
            car.straight = True
            car.back = False
            car.left = False
            car.right = False
            car.parked = False
            car.speeding = False
            car.crashed = False

        if keys[pygame.K_a]:
            car.x -= car.vel
            car.straight = False
            car.back = False
            car.left = True
            car.right = False
            car.parked = False
            car.speeding = False
            car.crashed = False

        if keys[pygame.K_d]:
            car.x += car.vel
            car.straight = False
            car.back = False
            car.left = False
            car.right = True
            car.parked = False
            car.speeding = False
            car.crashed = False

        if keys[pygame.K_s]:
            bg.y -= bg.vel
            bot1.y -= bg.vel
            car.straight = False
            car.back = True
            car.left = False
            car.right = False
            car.parked = False
            car.speeding = False
            car.crashed = False

        if keys[pygame.K_LSHIFT]:
            bg.vel = 2
            car.speeding = True

        elif not(keys[pygame.K_LSHIFT]):
            bg.vel = 0.7
            car.speeding = True


        if not(keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]):
            car.straight = False
            car.back = False
            car.left = False
            car.right = False
            car.parked = True
            car.speeding = False
            car.crashed = False

        game()


menu()

pygame.quit()