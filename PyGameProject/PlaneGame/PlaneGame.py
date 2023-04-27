import pygame
import random
import math
import sys

# 初始化界面
pygame.init()
# 设置窗口的大小
screen = pygame.display.set_mode((800, 600))
# 设置窗口的显示名称
pygame.display.set_caption("打飞机")
# 加载图片
icon = pygame.image.load("ufo.png")
bgimg = pygame.image.load("bg.png")
player = pygame.image.load("player.png")
enemyImg = pygame.image.load("enemy.png")
# 添加背景音效
pygame.mixer.music.load("bg.wav")
# 背景音乐单曲循环
pygame.mixer.music.play(-1)
# 添加射中音效
bao_sound = pygame.mixer.Sound("exp.wav")
# 定义飞机的起始位置的坐标
playerX = 400
playerY = 500
playerStep = 0

# 添加分数
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)


def show_score():
    text = f"Score:{score}"
    score_render = font.render(text, True, (0, 255, 0))
    screen.blit(score_render, (10, 10))


# 游戏结束
is_over = False
over_font = pygame.font.Font('freesansbold.ttf', 64)


def check_is_over():
    if is_over:
        text = "Game Over"
        render = over_font.render(text, True, (255, 0, 0))
        screen.blit(render, (200, 250))


class enemy():
    def __init__(self):
        self.img = pygame.image.load("enemy.png")
        self.x = random.randint(200, 600)
        self.y = random.randint(50, 250)
        self.step = random.randint(2, 6)

    def reset(self):
        self.x = random.randint(200, 600)
        self.y = random.randint(50, 200)


enemies = []
for i in range(5):
    enemies.append(enemy())


class bullet():
    def __init__(self):
        self.img = pygame.image.load("bullet.png")
        self.x = playerX + 16
        self.y = playerY + 10
        self.step = 5

    def hit(self):
        global score
        for e in enemies:
            if distance(self.x, self.y, e.x, e.y) < 30:
                bao_sound.play()
                score += 1
                bullets.remove(self)
                e.reset()


bullets = []
# 设置左上角的游戏图标
pygame.display.set_icon(icon)

is_over = False


# 显示敌人
def showEnemy():
    global is_over
    for e in enemies:
        screen.blit(e.img, (e.x, e.y))
        e.x += e.step
        if e.x > 736 or e.x < 0:
            e.step *= -1
            e.y += 8
            if e.y > 450:
                is_over = True
                enemies.clear()


def movePlayer():
    # 使用global关键字就可以修改全局变量的啦
    global playerX
    playerX = playerX + playerStep
    # 对小飞机进行边界控制
    if playerX > 736:
        playerX = 736
    if playerX < 0:
        playerX = 0


def showBullets():
    for i in bullets:
        screen.blit(i.img, (i.x, i.y))
        i.hit()
        i.y -= i.step
        if i.y < 0:
            bullets.remove(i)


# 俩个点之间的距离
def distance(x1, y1, x2, y2):
    a = x2 - x1
    b = y2 - y1
    return math.sqrt(a * a + b * b)


# 游戏主循环
running = True

while running:
    # 将背景图添加到窗口中
    screen.blit(bgimg, (0, 0))
    # 将飞机图添加到窗口中
    screen.blit(player, (playerX, playerY))
    show_score()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # 通过键盘事件控制飞机的移动
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerStep = 2
            if event.key == pygame.K_LEFT:
                playerStep = -2
            if event.key == pygame.K_SPACE:
                bullets.append(bullet())

                print("发射子弹啦")
        if event.type == pygame.KEYUP:
            playerStep = 0
    movePlayer()
    showEnemy()
    showBullets()
    check_is_over()
    # 更新整个窗口
    pygame.display.update()
