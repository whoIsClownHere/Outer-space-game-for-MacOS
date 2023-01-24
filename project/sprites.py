import pygame
from constants import *
from load_image import load_image
import random


class MovingSprite(pygame.sprite.Sprite):
    def update(self):
        super(MovingSprite, self).update()

        if self.rect.centerx < -100 or self.rect.centerx > SCREEN_HEIGHT + 1000:
            self.kill()

    def collision_check(self, rect):
        if pygame.sprite.collide_mask(self, rect):
            self.kill()
            return True
        return False


class Shoot(MovingSprite):
    image = load_image("laser.png")
    frames = ['Fireball/fireball-1.png', 'Fireball/fireball-2.png', 'Fireball/fireball-3.png',
              'Fireball/fireball-4.png', 'Fireball/fireball-5.png', 'Fireball/fireball-6.png']

    def __init__(self, x, y, shoot_type='small'):
        super(Shoot, self).__init__()
        self.shoot_type = shoot_type

        if self.shoot_type == 'small':
            self.image = Shoot.image
            self.image = pygame.transform.scale(self.image, (50, 11))
        else:
            self.cur_frame = 0
            self.image = load_image(self.frames[self.cur_frame])
            self.image = pygame.transform.scale(self.image, (75, 139))
            self.image = pygame.transform.rotate(self.image, 90)

        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        super(Shoot, self).update()
        if self.shoot_type == 'small':
            self.rect.x += v_attack / FPS
        else:
            self.rect.x += v_second_attack / FPS

    def update_animation(self):
        if self.shoot_type != 'small':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = load_image(self.frames[self.cur_frame])
            self.image = pygame.transform.scale(self.image, (75, 139))
            self.image = pygame.transform.rotate(self.image, 90)


class BossShoot(MovingSprite):
    image = load_image("fireball.png")

    def __init__(self, x, y, x_player, y_player):
        super(BossShoot, self).__init__()

        self.x = x
        self.y = y
        self.x_player = x_player
        self.y_player = y_player

        self.image = BossShoot.image
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

        self.k, self.b = self.make_moving_function()

        self.mask = pygame.mask.from_surface(self.image)

    def make_moving_function(self):
        if self.x - self.x_player != 0:
            k = (self.y - self.y_player) / (self.x - self.x_player)
            b = self.y - self.x * k
            return k, b

    def update(self):
        super(BossShoot, self).update()
        self.rect.centerx -= v_boss_attack / FPS
        self.rect.centery = self.k * self.rect.x + self.b


class Background(pygame.sprite.Sprite):
    image = load_image("background/space.png")

    def __init__(self, orientation=False):
        super(Background, self).__init__()

        self.image = Background.image
        if orientation:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x -= v_background


class Boss(pygame.sprite.Sprite):
    frames = ['Boss/ship_big-1.png', 'Boss/ship_big-2.png', 'Boss/ship_big-3.png', 'Boss/ship_big-4.png']

    def __init__(self, x, y):
        super(Boss, self).__init__()
        self.cur_frame = 0
        self.image = load_image(self.frames[self.cur_frame])
        self.image = pygame.transform.scale(self.image, (500, 375))
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.centery = y

        self.moving = 1

    def update_animation(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = load_image(self.frames[self.cur_frame])
        self.image = pygame.transform.scale(self.image, (500, 375))

    def update(self):
        if self.moving == 1:
            self.rect.centery += v_boss / FPS
            if self.rect.bottom > SCREEN_HEIGHT - 100:
                self.moving *= -1
        else:
            self.rect.centery += -v_boss / FPS
            if self.rect.top < 0:
                self.moving *= -1


class Player(pygame.sprite.Sprite):
    frames = ['Player/ship-1.tiff', 'Player/ship-2.tiff', 'Player/ship-4.tiff']

    def __init__(self):
        super(Player, self).__init__()
        self.cur_frame = 0
        self.image = load_image(self.frames[self.cur_frame])
        self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale(self.image, (200, 100))
        self.rect = self.image.get_rect()
        self.rect.right = 10
        self.rect.centery = SCREEN_HEIGHT / 2

        self.moving = 1

    def update_animation(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = load_image(self.frames[self.cur_frame])
        self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale(self.image, (200, 100))


class Meteor(MovingSprite):
    image = load_image("meteor.png")

    def __init__(self):
        super(Meteor, self).__init__()

        self.image = Meteor.image
        self.image = pygame.transform.scale(self.image, (75, 58.5))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH
        self.rect.centery = random.randrange(SCREEN_HEIGHT - 100)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        super(Meteor, self).update()
        self.rect.centerx -= v_meteor / FPS


class Heart(pygame.sprite.Sprite):
    frames = ['Heart/heart-1.png', 'Heart/heart-2.png']

    def __init__(self, i):
        super(Heart, self).__init__()
        self.cur_frame = 0
        self.image = load_image(self.frames[self.cur_frame])
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.left = 50 + i * 50 + i * 10
        self.rect.top = SCREEN_HEIGHT - 100

    def update_animation(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = load_image(self.frames[self.cur_frame])
        self.image = pygame.transform.scale(self.image, (50, 50))


class Boom(pygame.sprite.Sprite):
    frames = ['boom/boom-1.tiff', 'boom/boom-2.tiff', 'boom/boom-3.tiff', 'boom/boom-4.tiff', 'boom/boom-5.tiff',
              'boom/boom-6.tiff', 'boom/boom-7.tiff', 'boom/boom-8.tiff', 'boom/boom-9.tiff', 'boom/boom-10.tiff',
              'boom/boom-11.tiff', 'boom/boom-12.tiff']

    def __init__(self, x, y):
        super(Boom, self).__init__()
        self.cur_frame = 0
        self.image = load_image(self.frames[self.cur_frame])
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x

    def update_animation(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = load_image(self.frames[self.cur_frame])
        if self.cur_frame == 11:
            self.kill()


class Fire(pygame.sprite.Sprite):
    frames = ['fire/fire-1.tiff', 'fire/fire-2.tiff', 'fire/fire-3.tiff', 'fire/fire-4.tiff', 'fire/fire-5.tiff',
              'fire/fire-6.tiff', 'fire/fire-7.tiff', 'fire/fire-8.tiff', 'fire/fire-9.tiff', 'fire/fire-10.tiff',
              'fire/fire-11.tiff', 'fire/fire-12.tiff', 'fire/fire-13.tiff', 'fire/fire-14.tiff', 'fire/fire-15.tiff',
              'fire/fire-16.tiff', 'fire/fire-17.tiff', 'fire/fire-18.tiff', 'fire/fire-19.tiff', 'fire/fire-20.tiff',
              'fire/fire-21.tiff', 'fire/fire-22.tiff', 'fire/fire-23.tiff', 'fire/fire-24.tiff', 'fire/fire-25.tiff',
              'fire/fire-26.tiff', 'fire/fire-27.tiff', 'fire/fire-28.tiff', 'fire/fire-29.tiff', 'fire/fire-30.tiff',
              'fire/fire-31.tiff', 'fire/fire-32.tiff', 'fire/fire-33.tiff', 'fire/fire-34.tiff', 'fire/fire-35.tiff',
              'fire/fire-36.tiff', 'fire/fire-37.tiff', 'fire/fire-38.tiff']

    def __init__(self, rect, index):
        super(Fire, self).__init__()
        self.cur_frame = 0
        self.image = load_image(self.frames[self.cur_frame])
        self.rect = self.image.get_rect()

        if index == 1:
            self.count = 107
            self.rect.bottom = rect.centery + self.count
            self.rect.centerx = rect.centerx + 287
        elif index == 2:
            self.count = 100
            self.rect.bottom = rect.centery + self.count
            self.rect.centerx = rect.centerx + 400
        elif index == 3:
            self.count = 50
            self.rect.bottom = rect.centery + 500
            self.rect.centerx = rect.centerx + 350
        elif index == 4:
            self.count = 30
            self.rect.bottom = rect.centery + self.count
            self.rect.centerx = rect.centerx + 270
        elif index == 5:
            self.count = 160
            self.rect.bottom = rect.centery + self.count
            self.rect.centerx = rect.centerx + 300

        self.image = pygame.transform.scale(self.image, (200, 111))
        self.boss_rect = rect

    def update_animation(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = load_image(self.frames[self.cur_frame])
        self.image = pygame.transform.scale(self.image, (200, 111))

    def update(self):
        self.rect.centery = self.boss_rect.centery + self.count


class MeteorBoom(pygame.sprite.Sprite):
    frames = ['meteor_boom/meteor_boom-1.tiff', 'meteor_boom/meteor_boom-2.tiff', 'meteor_boom/meteor_boom-3.tiff',
              'meteor_boom/meteor_boom-4.tiff', 'meteor_boom/meteor_boom-5.tiff', 'meteor_boom/meteor_boom-6.tiff',
              'meteor_boom/meteor_boom-7.tiff', 'meteor_boom/meteor_boom-8.tiff', 'meteor_boom/meteor_boom-9.tiff']

    def __init__(self, x, y):
        super(MeteorBoom, self).__init__()
        self.cur_frame = 0
        self.image = load_image(self.frames[self.cur_frame])
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect.centery = y
        self.rect.centerx = x

    def update_animation(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = load_image(self.frames[self.cur_frame])
        self.image = pygame.transform.scale(self.image, (100, 100))
        if self.cur_frame == 8:
            self.kill()
