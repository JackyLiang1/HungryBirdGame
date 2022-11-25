import pygame, sys, time, random, colorsys, math
from pygame.locals import *
from player import Player
from background import Background
from button import Button
from pig import Pig
from utils import clamp
from utils import checkCollisions
def main():
    pygame.init()
    # 设置窗口
    DISPLAY=pygame.display.set_mode((640,480),0,32)
    pygame.display.set_caption('Hungry-Bird')
    pygame.display.set_icon(pygame.image.load('data/gfx/player.png'))
    # 获取字体
    font = pygame.font.Font('data/fonts/font.otf', 100)
    font_small = pygame.font.Font('data/fonts/font.otf', 32)
    font_20 = pygame.font.Font('data/fonts/font.otf', 20)
    # 获取图片
    shop = pygame.image.load('data/gfx/shop.png')
    shop_bg = pygame.image.load('data/gfx/shop_bg.png')
    retry_button = pygame.image.load('data/gfx/retry_button.png')
    logo = pygame.image.load('data/gfx/logo.png')
    title_bg = pygame.image.load('data/gfx/bg.png')
    title_bg.fill((255, 30.599999999999998, 0.0), special_flags=pygame.BLEND_ADD)
    # 获取声音
    flapfx = pygame.mixer.Sound("data/sfx/flap.wav")
    upgradefx = pygame.mixer.Sound("data/sfx/upgrade.wav")
    beanfx = pygame.mixer.Sound("data/sfx/pig.wav")
    deadfx = pygame.mixer.Sound("data/sfx/dead.wav")
    # 设置颜色
    WHITE=(255,255,255)
    # 设置鸟旋转的偏移量
    rotOffset = -5
    # 创建新的玩家对象
    player = Player()
    pigs = []
    buttons = []
    # 添加两个按钮
    for i in range(2): buttons.append(Button())
    # 设置初始价格
    buttons[0].typeIndicatorSprite = pygame.image.load('data/gfx/flap_indicator.png')
    buttons[0].price = 5   
    buttons[1].typeIndicatorSprite = pygame.image.load('data/gfx/speed_indicator.png')
    buttons[1].price = 5
    # 获取5个猪
    for i in range(5): pigs.append(Pig())
    # 通过猪列表循环
    for pig in pigs:
        pig.position.xy = random.randrange(0, DISPLAY.get_width() - pig.sprite.get_width()), pigs.index(pig)*-200 - player.position.y
    # 创建背景列表, 每个对象都有相应的索引
    bg = [Background(), Background(), Background()]
    # 一些必要的变量
    pigCount = 0
    startingHeight = player.position.y
    height = 0
    health = 100
    flapForce = 3
    dead = False
    # 需要的帧速率和时间
    framerate = 60
    last_time = time.time()
    splashScreenTimer = 0
    # 渲染屏幕
    # 播放声音
    pygame.mixer.Sound.play(flapfx)
    while splashScreenTimer < 100:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()

        splashScreenTimer += dt

        for event in pygame.event.get():
            # 如果玩家点击按钮
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

        DISPLAY.fill((231, 205, 183))
        # 初始页面
        startMessage = font_small.render("Liang Junhao's tiny game", True, (171, 145, 123))
        DISPLAY.blit(startMessage, (DISPLAY.get_width()/2 - startMessage.get_width()/2, DISPLAY.get_height()/2 - startMessage.get_height()/2))
            
        # 更新窗口
        pygame.display.update()
        # 等待片刻
        pygame.time.delay(10)
    
    titleScreen = True
    # 开始界面
    pygame.mixer.Sound.play(flapfx)
    while titleScreen:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
        # 获取鼠标坐标
        mouseX,mouseY = pygame.mouse.get_pos()  
        # 获取键盘点击
        clicked = False
        keys = pygame.key.get_pressed()
        # 检测项目
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            # 如果玩家退出
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        # 用户点击并且鼠标位置发生移动
        if (clicked and checkCollisions(mouseX, mouseY, 3, 3, DISPLAY.get_width()/2 - retry_button.get_width()/2, 288, retry_button.get_width(), retry_button.get_height())):
            clicked = False
            pygame.mixer.Sound.play(upgradefx)
            titleScreen = False

        DISPLAY.fill(WHITE)
        DISPLAY.blit(title_bg, (0,0))
        DISPLAY.blit(logo, (DISPLAY.get_width()/2 - logo.get_width()/2, DISPLAY.get_height()/2 - logo.get_height()/2 + math.sin(time.time()*5)*5 - 25)) 
        DISPLAY.blit(retry_button, (DISPLAY.get_width()/2 - retry_button.get_width()/2, 288))
        startMessage = font_small.render("START", True, (0, 0, 0))
        DISPLAY.blit(startMessage, (DISPLAY.get_width()/2 - startMessage.get_width()/2, 292))

        pygame.display.update()
        pygame.time.delay(10)

    # 主程序循环
    while True:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
        # 再次获取鼠标坐标
        mouseX,mouseY = pygame.mouse.get_pos()
        jump = False
        clicked = False
        keys = pygame.key.get_pressed()
        # 获取事件
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN and event.key==K_SPACE:
                jump = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            if clicked and mouseY < DISPLAY.get_height() - 90:
                jump = True
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        
        camOffset = -player.position.y + DISPLAY.get_height()/2 - player.currentSprite.get_size()[1]/2

        DISPLAY.fill(WHITE)
        for o in bg:
            o.setSprite(((player.position.y/50) % 100) / 100)
            DISPLAY.blit(o.sprite, (0, o.position))

        color = colorsys.hsv_to_rgb(((player.position.y/50) % 100) / 100,0.5,0.5)
        currentHeightMarker = font.render(str(height), True, (color[0]*255, color[1]*255, color[2]*255, 50 ))
        DISPLAY.blit(currentHeightMarker, (DISPLAY.get_width()/2 - currentHeightMarker.get_width()/2, camOffset + round((player.position.y - startingHeight)/DISPLAY.get_height())*DISPLAY.get_height() + player.currentSprite.get_height() - 40))


        for pig in pigs:
            DISPLAY.blit(pig.sprite, (pig.position.x, pig.position.y + camOffset))
        DISPLAY.blit(pygame.transform.rotate(player.currentSprite, clamp(player.velocity.y, -10, 5)*rotOffset), (player.position.x,player.position.y + camOffset))

        DISPLAY.blit(shop_bg, (0, 0))
        pygame.draw.rect(DISPLAY, (81, 48, 20), (21, 437, 150 * (health / 100), 25))
        DISPLAY.blit(shop, (0, 0))



        for button in buttons:
            DISPLAY.blit(button.sprite, (260 + (buttons.index(button)*200), 393))
            priceDisplay = font_small.render(str(button.price), True, (0,0,0))
            DISPLAY.blit(priceDisplay, (302 + (buttons.index(button)*200), 408))
            levelDisplay = font_20.render('Lvl. ' + str(button.level), True, (200,200,200))
            DISPLAY.blit(levelDisplay, (274 + (buttons.index(button)*200), 441))
            DISPLAY.blit(button.typeIndicatorSprite, (242 + (buttons.index(button)*200), 377))

        pigCountDisplay = font_small.render(str(pigCount).zfill(7), True, (0,0,0))
        DISPLAY.blit(pigCountDisplay, (72, 394))
        if dead:
            DISPLAY.blit(retry_button, (4, 4))
            deathMessage = font_small.render("RETRY", True, (0, 0, 0))
            DISPLAY.blit(deathMessage, (24, 8))
        
        height = round(-(player.position.y - startingHeight)/DISPLAY.get_height())
 
        player.position.x += player.velocity.x*dt
        if player.position.x + player.currentSprite.get_size()[0] > 640:
            player.velocity.x = -abs(player.velocity.x)
            player.currentSprite = player.leftSprite
            rotOffset = 5
        if player.position.x < 0:
            player.velocity.x = abs(player.velocity.x)
            player.currentSprite = player.rightSprite
            rotOffset = -5
        if jump and not dead:
            player.velocity.y = -flapForce
            pygame.mixer.Sound.play(flapfx)
        player.position.y += player.velocity.y*dt
        player.velocity.y = clamp(player.velocity.y + player.acceleration*dt, -99999999999, 50)


        health -= 0.2*(1+height/10)*dt
        if health <= 0 and not dead:
            dead = True
            pygame.mixer.Sound.play(deadfx)
            

        for pig in pigs:
            if pig.position.y + camOffset + 90 > DISPLAY.get_height():
                pig.position.y -= DISPLAY.get_height()*2
                pig.position.x = random.randrange(0, DISPLAY.get_width() - pig.sprite.get_width())
            if (checkCollisions(player.position.x, player.position.y, player.currentSprite.get_width(), player.currentSprite.get_height(), pig.position.x, pig.position.y, pig.sprite.get_width(), pig.sprite.get_height())):
                dead = False
                pygame.mixer.Sound.play(beanfx)
                pigCount += 1
                health = 100
                pig.position.y -= DISPLAY.get_height() - random.randrange(0, 200)
                pig.position.x = random.randrange(0, DISPLAY.get_width() - pig.sprite.get_width())

        for button in buttons:
            buttonX,buttonY = 220 + (buttons.index(button)*200), 393
            if clicked and not dead and checkCollisions(mouseX, mouseY, 3, 3, buttonX, buttonY, button.sprite.get_width(), button.sprite.get_height()):
                if (pigCount >= button.price):
                    pygame.mixer.Sound.play(upgradefx)
                    button.level += 1
                    pigCount -= button.price
                    button.price = round(button.price*2.5)
                    if (buttons.index(button) == 0):
                        flapForce *= 1.5
                    if (buttons.index(button) == 1):
                        player.velocity.x *= 1.5
        
        if dead and clicked and checkCollisions(mouseX, mouseY, 3, 3, 4, 4, retry_button.get_width(), retry_button.get_height()):
            health = 100
            player.velocity.xy = 3, 0
            player.position.xy = 295, 100
            player.currentSprite = player.rightSprite
            pigCount = 0
            height = 0
            flapForce = 3
            buttons = []
            for i in range(2): buttons.append(Button())
            buttons[0].typeIndicatorSprite = pygame.image.load('data/gfx/flap_indicator.png')
            buttons[0].price = 5   
            buttons[1].typeIndicatorSprite = pygame.image.load('data/gfx/speed_indicator.png')
            buttons[1].price = 5
            pigs = []
            for i in range(5): pigs.append(Pig())
            for pig in pigs:
                pig.position.xy = random.randrange(0, DISPLAY.get_width() - pig.sprite.get_width()), pigs.index(pig)*-200 - player.position.y
            pygame.mixer.Sound.play(upgradefx)
            dead = False         

        
        bg[0].position = camOffset + round(player.position.y/DISPLAY.get_height())*DISPLAY.get_height()
        bg[1].position = bg[0].position + DISPLAY.get_height() 
        bg[2].position = bg[0].position - DISPLAY.get_height()
        
        pygame.display.update()
        pygame.time.delay(10)


if __name__ == "__main__":
    main()
