import random
import pygame
from load_image import screen
from constants import *
from sprites import Shoot, BossShoot, Background, Boss, Player, Meteor, Heart, Boom, Fire, MeteorBoom
from load_image import load_image

pygame.init()


class GameView:
    def __init__(self):
        self.player = None
        self.heart = None
        self.player_image = load_image("ship1.png")
        self.hearts = PLAYER_HEARTS

        self.score = {"meteors": 0, "boss_hearts": 0}

        self.boss = None
        self.boss_hearts = BOSS_HEARTS

        self.first_background = None
        self.second_background = None
        self.third_background = None
        self.meteor = None
        self.boom = None
        self.fire = None
        self.meteor_boom = None

        self.boss_attacks = pygame.sprite.Group()
        self.player_attacks = pygame.sprite.Group()
        self.all_backgrounds = pygame.sprite.Group()
        self.all_meteors = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_hearts = pygame.sprite.Group()
        self.all_boom = pygame.sprite.Group()
        self.all_boss_damage = pygame.sprite.Group()

        self.pressed_keys = []

    def menu(self):
        clock = pygame.time.Clock()
        running = True

        timer_animation = pygame.USEREVENT
        pygame.time.set_timer(timer_animation, 70)

        all_sprites = pygame.sprite.Group()

        frames = ['Menu/space-1.tiff', 'Menu/space-2.tiff', 'Menu/space-3.tiff', 'Menu/space-4.tiff',
                  'Menu/space-5.tiff', 'Menu/space-6.tiff', 'Menu/space-7.tiff', 'Menu/space-8.tiff',
                  'Menu/space-9.tiff', 'Menu/space-10.tiff', 'Menu/space-11.tiff', 'Menu/space-12.tiff',
                  'Menu/space-13.tiff', 'Menu/space-14.tiff', 'Menu/space-15.tiff', 'Menu/space-16.tiff',
                  'Menu/space-17.tiff', 'Menu/space-18.tiff', 'Menu/space-19.tiff', 'Menu/space-20.tiff',
                  'Menu/space-21.tiff', 'Menu/space-22.tiff', 'Menu/space-23.tiff', 'Menu/space-24.tiff']

        cur_frame = 0

        background = pygame.sprite.Sprite()
        background.image = load_image(frames[cur_frame])
        background.image = pygame.transform.scale(background.image, (1400, 700))
        background.rect = background.image.get_rect()
        background.rect.x = 0
        background.rect.y = 0
        all_sprites.add(background)

        play = pygame.sprite.Sprite()
        play.image = load_image('Buttons/play.png')
        play.rect = play.image.get_rect()
        play.rect.x = 100
        play.rect.y = 250
        all_sprites.add(play)

        levels = pygame.sprite.Sprite()
        levels.image = load_image('Buttons/Levels.png')
        levels.rect = levels.image.get_rect()
        levels.rect.x = 100
        levels.rect.y = 350
        all_sprites.add(levels)

        quit_button = pygame.sprite.Sprite()
        quit_button.image = load_image('Buttons/Quit.png')
        quit_button.rect = quit_button.image.get_rect()
        quit_button.rect.x = 100
        quit_button.rect.y = 450
        all_sprites.add(quit_button)

        title = pygame.image.load('Data/Buttons/Outer space.png')
        title = pygame.transform.scale(title, (604, 98)).convert_alpha()

        while running:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.rect.collidepoint(event.pos):
                        running = False

                    if play.rect.collidepoint(event.pos):
                        self.setup()
                        player_result = self.game_life()
                        if player_result:
                            self.game_over(type_over='win')
                        elif not player_result:
                            self.game_over()

                    if levels.rect.collidepoint(event.pos):
                        self.levels_menu()

                if event.type == timer_animation:
                    cur_frame = (cur_frame + 1) % len(frames)
                    background.image = load_image(frames[cur_frame])
                    background.image = pygame.transform.scale(background.image, (1400, 700))

            all_sprites.draw(screen)
            all_sprites.update()

            screen.blit(title, (100, 70))

            clock.tick(FPS)
            pygame.display.flip()

    def levels_menu(self):
        clock = pygame.time.Clock()
        running = True

        timer_animation = pygame.USEREVENT
        pygame.time.set_timer(timer_animation, 70)

        all_sprites = pygame.sprite.Group()

        frames = ['Menu/space-1.tiff', 'Menu/space-2.tiff', 'Menu/space-3.tiff', 'Menu/space-4.tiff',
                  'Menu/space-5.tiff', 'Menu/space-6.tiff', 'Menu/space-7.tiff', 'Menu/space-8.tiff',
                  'Menu/space-9.tiff', 'Menu/space-10.tiff', 'Menu/space-11.tiff', 'Menu/space-12.tiff',
                  'Menu/space-13.tiff', 'Menu/space-14.tiff', 'Menu/space-15.tiff', 'Menu/space-16.tiff',
                  'Menu/space-17.tiff', 'Menu/space-18.tiff', 'Menu/space-19.tiff', 'Menu/space-20.tiff',
                  'Menu/space-21.tiff', 'Menu/space-22.tiff', 'Menu/space-23.tiff', 'Menu/space-24.tiff']

        cur_frame = 0

        background = pygame.sprite.Sprite()
        background.image = load_image(frames[cur_frame])
        background.image = pygame.transform.scale(background.image, (1400, 700))
        background.rect = background.image.get_rect()
        background.rect.x = 0
        background.rect.y = 0
        all_sprites.add(background)

        infinity = pygame.sprite.Sprite()
        infinity.image = load_image('Buttons/infinity.png')
        infinity.rect = infinity.image.get_rect()
        infinity.rect.centerx = SCREEN_WIDTH / 2
        infinity.rect.top = 200
        all_sprites.add(infinity)

        story = pygame.sprite.Sprite()
        story.image = load_image('Buttons/story.png')
        story.rect = story.image.get_rect()
        story.rect.right = infinity.rect.left - 50
        story.rect.top = 200
        all_sprites.add(story)

        hard = pygame.sprite.Sprite()
        hard.image = load_image('Buttons/hard.png')
        hard.rect = hard.image.get_rect()
        hard.rect.left = infinity.rect.right + 50
        hard.rect.top = 200
        all_sprites.add(hard)

        back = pygame.sprite.Sprite()
        back.image = load_image('Buttons/back.png')
        back.image = pygame.transform.scale(back.image, (75, 75))
        back.rect = back.image.get_rect()
        back.rect.right = story.rect.left - 50
        back.rect.centery = story.rect.centery
        all_sprites.add(back)

        title = pygame.image.load('Data/Buttons/Outer space.png')
        title = pygame.transform.scale(title, (604, 98)).convert_alpha()

        while running:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back.rect.collidepoint(event.pos):
                        running = False

                    if story.rect.collidepoint(event.pos):
                        self.setup()
                        player_result = self.game_life()
                        if player_result:
                            self.game_over(type_over='win')
                        elif not player_result:
                            self.game_over()

                    if infinity.rect.collidepoint(event.pos):
                        self.setup()
                        player_result = self.game_life(game_type='infinity')
                        if player_result:
                            self.game_over(type_over='win')
                        elif not player_result:
                            self.game_over()

                    if hard.rect.collidepoint(event.pos):
                        self.setup()
                        player_result = self.game_life(game_type='hard')
                        if player_result:
                            self.game_over(type_over='win', game_type='hard')
                        elif not player_result:
                            self.game_over(game_type='hard')

                if event.type == timer_animation:
                    cur_frame = (cur_frame + 1) % len(frames)
                    background.image = load_image(frames[cur_frame])
                    background.image = pygame.transform.scale(background.image, (1400, 700))

            all_sprites.draw(screen)
            all_sprites.update()

            screen.blit(title, (100, 70))

            clock.tick(FPS)
            pygame.display.flip()

    def game_over(self, type_over='lose', game_type=None):
        clock = pygame.time.Clock()

        if game_type == 'hard':
            score = (BOSS_HEARTS + 300 - self.boss_hearts) / BOSS_HEARTS * 100
        else:
            score = (BOSS_HEARTS - self.boss_hearts) / BOSS_HEARTS * 100
        score = round(score, 2)

        font = pygame.font.Font(None, 35)

        if score > 100:
            score_text = font.render(str(score)[:4] + '%', True, (255, 255, 255))
        else:
            score_text = font.render(str(score) + '%', True, (255, 255, 255))

        running = True

        if type_over == 'win':
            title = pygame.image.load('Data/Buttons/YOU WIN.png').convert_alpha()
        else:
            title = pygame.image.load('Data/Buttons/Game over.png').convert_alpha()

        all_sprites = pygame.sprite.Group()

        score_background = pygame.image.load('Data/Buttons/score.png').convert_alpha()
        best_score = pygame.image.load('Data/Buttons/Best score.png').convert_alpha()

        best_score_text = None

        f = open("best_score.txt", 'r')
        data = f.read()

        if data != '':
            if float(data) < score:
                f = open('best_score.txt', 'w')
                f.write(str(score))
                best_score_text = font.render(str(score) + '%', True, (255, 255, 255))
            else:
                best_score_text = font.render(str(data) + '%', True, (255, 255, 255))
        else:
            f = open('best_score.txt', 'w')
            f.write(str(score))

        f.close()

        quit_button = pygame.sprite.Sprite()
        quit_button.image = load_image('Buttons/back.png')
        quit_button.rect = quit_button.image.get_rect()
        quit_button.rect.centerx = SCREEN_WIDTH / 2
        quit_button.rect.bottom = SCREEN_HEIGHT - 90
        all_sprites.add(quit_button)

        while running:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.rect.collidepoint(event.pos):
                        running = False

            if type_over == 'win':
                screen.blit(title, (402, 110))
            else:
                screen.blit(title, (296, 110))

            screen.blit(score_background, (534, 333))
            screen.blit(score_text, (765, 389))

            if best_score_text:
                screen.blit(best_score, (1000, 600))
                screen.blit(best_score_text, (1200, 600))

            all_sprites.draw(screen)
            all_sprites.update()

            clock.tick(FPS)
            pygame.display.flip()

    def setup(self):
        self.boss_attacks = pygame.sprite.Group()
        self.player_attacks = pygame.sprite.Group()
        self.all_backgrounds = pygame.sprite.Group()
        self.all_meteors = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_hearts = pygame.sprite.Group()
        self.all_boom = pygame.sprite.Group()
        self.all_boss_damage = pygame.sprite.Group()

        self.first_background = Background()

        self.first_background.rect.left = 0
        self.first_background.rect.top = 0

        self.all_backgrounds.add(self.first_background)

        self.second_background = Background(orientation=True)

        self.second_background.rect.left = self.first_background.rect.right
        self.second_background.rect.top = 0

        self.all_backgrounds.add(self.second_background)

        self.third_background = Background()

        self.third_background.rect.left = self.second_background.rect.right
        self.third_background.rect.top = 0

        self.all_backgrounds.add(self.third_background)

        self.player = Player()

        self.boss = Boss(SCREEN_WIDTH, SCREEN_HEIGHT / 2)

        self.all_sprites.add(self.first_background)
        self.all_sprites.add(self.second_background)
        self.all_sprites.add(self.third_background)
        self.all_sprites.add(self.boss)
        self.all_sprites.add(self.player)

        self.hearts = PLAYER_HEARTS
        self.boss_hearts = BOSS_HEARTS

        self.pressed_keys = []

    def game_life(self, game_type='story'):
        if game_type == 'hard':
            self.hearts = 3
            self.boss_hearts = BOSS_HEARTS + 300

        for i in range(self.hearts):
            self.heart = Heart(i)
            self.all_sprites.add(self.heart)
            self.all_hearts.add(self.heart)

        clock = pygame.time.Clock()
        running = True

        timer_player_shoot = pygame.USEREVENT + 1
        pygame.time.set_timer(timer_player_shoot, 300)

        timer_player_shoot_second = pygame.USEREVENT + 2
        pygame.time.set_timer(timer_player_shoot_second, 100)

        if game_type == 'hard':
            timer_boss_shoot = pygame.USEREVENT + 3
            pygame.time.set_timer(timer_boss_shoot, 150)
        else:
            timer_boss_shoot = pygame.USEREVENT + 3
            pygame.time.set_timer(timer_boss_shoot, 300)

        timer_background = pygame.USEREVENT + 4
        pygame.time.set_timer(timer_background, 300)

        timer_animation = pygame.USEREVENT + 5
        pygame.time.set_timer(timer_animation, 70)

        timer_heart_animation = pygame.USEREVENT + 6
        pygame.time.set_timer(timer_heart_animation, 200)

        timer_meteor = pygame.USEREVENT + 7
        pygame.time.set_timer(timer_meteor, 1000)

        boss_died = pygame.USEREVENT + 8
        pygame.time.set_timer(boss_died, 8000)

        while running:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    self.pressed_keys.append(event.key)

                if pygame.K_x in self.pressed_keys and event.type == timer_player_shoot:
                    shoot = Shoot(self.player.rect.right, self.player.rect.top, shoot_type='big')
                    self.player_attacks.add(shoot)
                    self.all_sprites.add(shoot)

                if pygame.K_SPACE in self.pressed_keys and event.type == timer_player_shoot_second:
                    shoot = Shoot(self.player.rect.right, self.player.rect.top + 0.7 * self.player.rect.height)
                    self.player_attacks.add(shoot)
                    self.all_sprites.add(shoot)

                if self.boss_hearts <= 0 and event.type == timer_player_shoot_second and game_type != 'infinity':
                    x = random.randrange(self.boss.rect.left, self.boss.rect.right)
                    y = random.randrange(self.boss.rect.top, self.boss.rect.bottom)

                    boom = Boom(x, y)
                    self.all_sprites.add(boom)
                    self.all_boom.add(boom)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        if event.key in self.pressed_keys:
                            self.pressed_keys.remove(event.key)

                    if event.key == pygame.K_DOWN:
                        if event.key in self.pressed_keys:
                            self.pressed_keys.remove(event.key)

                    if event.key == pygame.K_LEFT:
                        if event.key in self.pressed_keys:
                            self.pressed_keys.remove(event.key)

                    if event.key == pygame.K_RIGHT:
                        if event.key in self.pressed_keys:
                            self.pressed_keys.remove(event.key)

                    if event.key == pygame.K_SPACE:
                        if event.key in self.pressed_keys:
                            self.pressed_keys.remove(event.key)

                    if event.key == pygame.K_x:
                        if event.key in self.pressed_keys:
                            self.pressed_keys.remove(event.key)

                if event.type == timer_boss_shoot and (self.boss_hearts > 0 or game_type == 'infinity'):
                    boss_shoot = BossShoot(self.boss.rect.left, self.boss.rect.bottom - 0.38 * self.boss.rect.height,
                                           self.player.rect.centerx, self.player.rect.centery)
                    self.boss_attacks.add(boss_shoot)
                    self.all_sprites.add(boss_shoot)

                if event.type == timer_background:
                    if self.first_background.rect.right <= 0:
                        self.first_background.rect.left = self.third_background.rect.right

                    if self.second_background.rect.right <= 0:
                        self.second_background.rect.left = self.first_background.rect.right

                    if self.third_background.rect.right <= 0:
                        self.third_background.rect.left = self.second_background.rect.right

                    self.all_backgrounds.update()

                if event.type == timer_animation:
                    self.boss.update_animation()
                    self.player.update_animation()

                    for i in self.all_boom:
                        i.update_animation()

                    for i in self.all_boss_damage:
                        i.update_animation()

                    for i in self.player_attacks:
                        i.update_animation()

                if event.type == timer_heart_animation:
                    for i in self.all_hearts:
                        i.update_animation()

                if event.type == timer_meteor:
                    self.meteor = Meteor()
                    self.all_meteors.add(self.meteor)
                    self.all_sprites.add(self.meteor)

                if event.type == boss_died and self.boss_hearts <= 0 and game_type != 'infinity':
                    return True

            if len(self.pressed_keys) != 0:
                if pygame.K_UP in self.pressed_keys:
                    self.player.rect.centery -= v / FPS

                if pygame.K_DOWN in self.pressed_keys:
                    self.player.rect.centery += v / FPS

                if pygame.K_LEFT in self.pressed_keys:
                    self.player.rect.x -= v / FPS

                if pygame.K_RIGHT in self.pressed_keys:
                    self.player.rect.x += v / FPS

            for i in self.boss_attacks:
                if i.collision_check(self.player) and (self.boss_hearts > 0 or game_type == 'infinity')\
                        and self.hearts > 0:
                    self.hearts -= 1
                    self.heart = self.all_hearts.sprites()[-1]
                    self.heart.kill()

                for j in self.player_attacks:
                    if i.collision_check(j):
                        i.kill()
                    if j.collision_check(self.boss):
                        self.boss_hearts -= 1
                        if self.boss_hearts % 100 == 0 and game_type != 'infinity':
                            self.boom = Boom(*j.rect.center)
                            if len(self.all_boss_damage) + 1 <= 5:
                                self.fire = Fire(self.boss.rect, len(self.all_boss_damage) + 1)

                            self.all_boss_damage.add(self.fire)
                            self.all_boom.add(self.boom)

                            self.all_sprites.add(self.fire)
                            self.all_sprites.add(self.boom)

                    for k in self.all_meteors:
                        if j.collision_check(k):
                            self.meteor_boom = MeteorBoom(*k.rect.center)

                            self.all_boom.add(self.meteor_boom)
                            self.all_sprites.add(self.meteor_boom)

                            k.kill()

            for i in self.all_meteors:
                if i.collision_check(self.player) and (self.boss_hearts > 0 or game_type == 'infinity')\
                        and self.hearts > 0:
                    self.hearts -= 1
                    self.heart = self.all_hearts.sprites()[-1]
                    self.heart.kill()

            self.all_sprites.draw(screen)
            self.all_sprites.update()

            if self.player.rect.bottom > SCREEN_HEIGHT - 100:
                self.player.rect.bottom = SCREEN_HEIGHT - 100
            if self.player.rect.right > self.boss.rect.left:
                self.player.rect.right = self.boss.rect.left
            if self.player.rect.top < 0:
                self.player.rect.top = 0
            if self.player.rect.left < 0:
                self.player.rect.left = 0

            clock.tick(FPS)
            pygame.display.flip()

            if self.hearts == 0 and (self.boss_hearts > 0 or game_type == 'infinity'):
                return False

            if self.boss_hearts == 0 and game_type != 'infinity':
                x = random.randrange(self.boss.rect.left, self.boss.rect.right)
                y = random.randrange(self.boss.rect.top, self.boss.rect.bottom)

                boom = Boom(x, y)
                self.all_sprites.add(boom)
                self.all_boom.add(boom)
