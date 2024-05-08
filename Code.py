#ping-pong
import pygame
import random
import os

# Устанавливаем размер окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Инициализация Pygame
pygame.init()

# Создаем окно
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ping Pong")

# Загружаем изображения
racket_img = pygame.image.load("racket.png")
racket_img = pygame.transform.scale(racket_img, (100, 20))  # Изменяем размер ракетки

ball_img = pygame.image.load("tennis_ball.png")
ball_img = pygame.transform.scale(ball_img, (20, 20))  # Изменяем размер мяча

# Определяем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Определяем скорости мяча по оси X и Y
BALL_SPEED_X = 7 * random.choice((1, -1))
BALL_SPEED_Y = 7 * random.choice((1, -1))

# Определяем класс для ракетки
class Racket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = racket_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)

    def update(self):
        # Перемещение ракетки влево или вправо
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        
        # Ограничиваем движение ракетки по экрану
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

# Определяем класс для мяча
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ball_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Отражение мяча от стен
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y

# Создаем спрайт группы для ракетки и мяча
all_sprites = pygame.sprite.Group()
racket = Racket()
ball = Ball()
all_sprites.add(racket, ball)

# Создаем основной цикл игры
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # Проверка на столкновение мяча с ракеткой
    if pygame.sprite.collide_rect(ball, racket):
        ball.speed_y = -BALL_SPEED_Y

    # Проверка на победу (мяч достиг нижней границы)
    if ball.rect.bottom >= SCREEN_HEIGHT:
        running = False  # Игра завершается

    # Отрисовка
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
