import random

from classes.action import Action
from classes.animation_set import AnimationSet
from classes.animation import Animation
from classes.timer import Timer
from settings import Settings
import pygame, os


class Character(pygame.sprite.Sprite):
    def __init__(self, game, options, size, pos):
        super().__init__()
        self.surface = pygame.Surface(size)
        self.game = game
        self.options = options
        self.size = size
        self.pos = pos
        self.flip = False

        animation_path = os.path.join(Settings.path_image, 'sprites', 'character')
        animations = [
            Animation('WALKING', animation_path, self.options, (64, 64), 16, 50),
            Animation('DIG', animation_path, self.options, (64, 64), 16, 50),
            Animation('CAUGHT', animation_path, self.options, (64, 64), 16, 50),
            Animation('REELING', animation_path, self.options, (64, 64), 16, 50),
            Animation('WAITING', animation_path, self.options, (64, 64), 16, 50),
            Animation('CASTING', animation_path, self.options, (64, 64), 16, 50),
            Animation('HAMMERING', animation_path, self.options, (64, 64), 16, 50),
            Animation('SWIMMING', animation_path, self.options, (64, 64), 16, 50),
            Animation('MINING', animation_path, self.options, (64, 64), 16, 50),
            Animation('AXE', animation_path, self.options, (64, 64), 16, 50),
            Animation('ROLL', animation_path, self.options, (64, 64), 16, 50),
            Animation('JUMP', animation_path, self.options, (64, 64), 16, 50),
            Animation('RUN', animation_path, self.options, (64, 64), 16, 50),
            Animation('DOING', animation_path, self.options, (64, 64), 16, 50),
            Animation('DEATH', animation_path, self.options, (64, 64), 16, 50),
            Animation('HURT', animation_path, self.options, (64, 64), 16, 50),
            Animation('WATERING', animation_path, self.options, (64, 64), 16, 50),
            Animation('CARRY', animation_path, self.options, (64, 64), 16, 50),
            Animation('IDLE', animation_path, self.options, (64, 64), 16, 50),
            Animation('ATTACK', animation_path, self.options, (64, 64), 16, 50)
        ]

        self.animation_set = AnimationSet('character', animations)
        self.action_handler = Action({'name': 'WALKING', 'loop': True})

        self.update_sprite(self.surface)
        self.set_position(*self.pos)

    def update_sprite(self, surface):
        self.image = pygame.transform.scale(surface, self.size)
        if self.flip:
            self.image = pygame.transform.flip(self.image, self.flip, False)
        self.rect = self.image.get_rect()

    def set_position(self, x, y):
        self.rect.x, self.rect.y = x, y

    def update(self):
        frame = self.animation_set.process_animation(self.action_handler.current_action['name'])
        if frame:
            self.update_sprite(frame)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class WalkingNPC(Character):
    def __init__(self, game, options, size, pos):
        super().__init__(game, options, size, pos)
        self.block_animations = False
        self.walking_speed = 0
        self.old_animation_pos = (0, 0)
        self.old_walking_pos = (0, 0)
        self.movement_timer = Timer(random.randint(1000, 2000))
        self.direction = random.choice(Settings.npc_directions)
        self.random_animation_timer = Timer(1000)

    def update_sprite(self, surface):
        self.old_animation_pos = self.pos
        super().update_sprite(surface)
        self.set_position(*self.old_animation_pos)

    def calculate_movement(self, ignore_direction=None):
        if ignore_direction:
            if ignore_direction == "up":
                self.direction = "down"
            elif ignore_direction == "down":
                self.direction = "up"
            elif ignore_direction == "left":
                self.direction = "right"
            elif ignore_direction == "right":
                self.direction = "left"

        else:
            self.direction = random.choice(Settings.npc_directions)     # Random walking direction choice
        self.walking_speed = random.randint(*Settings.npc_speed_range)  # Random Walking speed

        # Random Character actions
        if abs(self.walking_speed) == 0:
            if not self.block_animations:
                self.action_handler.force_change_action(random.choice(['IDLE', 'WATERING', 'DOING']))

        elif self.walking_speed == 1:
            self.action_handler.force_change_action('WALKING')

        elif self.walking_speed == 2:
            self.action_handler.force_change_action('RUN')

    def movement(self, is_collided=False):
        if self.movement_timer.is_next_stop_reached():
            self.calculate_movement()

        else:
            speed_y, speed_x = 0, 0
            if self.direction == "up":
                speed_y = -self.walking_speed
            elif self.direction == "down":
                speed_y = self.walking_speed
            if self.direction == "left":
                speed_x = -self.walking_speed
            elif self.direction == "right":
                speed_x = self.walking_speed

            # Calculating if character needs to flip
            if speed_x > 0:
                self.flip = False
            else:
                self.flip = True

            if not is_collided:
                self.old_walking_pos = self.pos
                self.rect.move_ip(speed_x, speed_y)
                self.pos = (self.rect.x, self.rect.y)

    def check_collision(self):
        hitlist = pygame.sprite.spritecollide(self, self.game.map_manager.border_tiles, False)
        if len(hitlist) > 0:
            for hit in hitlist:
                if pygame.sprite.collide_mask(self, hit):
                    return hitlist
        else:
            return False

    def fix_position(self):
        if self.direction != "up" or self.direction != "down":
            self.flip = not self.flip

        self.calculate_movement(self.direction)
        self.set_position(*self.old_walking_pos)
        self.pos = (self.rect.x, self.rect.y)
        self.block_animations = True

    def update(self):
        super().update()
        if self.check_collision():
            self.fix_position()
        else:
            self.movement()
            self.block_animations = False
