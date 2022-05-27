import random

from classes.action import Action
from classes.animation_set import AnimationSet
from classes.animation import Animation
from classes.timer import Timer
from settings import Settings
import pygame, os


class Character(pygame.sprite.Sprite):
    def __init__(self, game, options, size, pos):
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
        self.walking_offset = 0
        self.walking_speed = 0
        self.old_pos = (0, 0)
        self.movement_timer = Timer(random.randint(1000, 2000))
        self.direction = random.choice(Settings.npc_directions)
        self.random_animation_timer = Timer(1000)

    def update_sprite(self, surface):
        self.old_pos = self.pos
        super().update_sprite(surface)
        self.set_position(*self.old_pos)

    def calculate_movement(self, ignore_direction=None):
        if ignore_direction:
            if ignore_direction == "up":
                self.direction = "down"
            elif ignore_direction == "down":
                self.direction = "up"

            if ignore_direction == "right":
                self.direction = "left"
            elif ignore_direction == "left":
                self.direction = "right"

        else:
            self.direction = random.choice(Settings.npc_directions)  # Random walking direction choice

        print(ignore_direction, self.direction)

        self.walking_speed = random.randint(*Settings.npc_speed_range)  # Random Walking speed

        if not ignore_direction:
            # For diagonal walking offset
            self.walking_offset = random.randrange(*Settings.npc_offset_range)

            # Random Character actions
            if sum([abs(self.walking_speed), abs(self.walking_offset)]) == 0:
                self.action_handler.force_change_action(random.choice(['IDLE', 'DIG', 'AXE', 'HAMMERING', 'DOING']))
                print(self.action_handler.current_action)

            elif sum([abs(self.walking_speed), abs(self.walking_offset)]) == 1:
                self.action_handler.force_change_action('WALKING')
                print(self.action_handler.current_action)

            elif sum([abs(self.walking_speed), abs(self.walking_offset)]) == 2:
                self.action_handler.force_change_action('RUN')
                print(self.action_handler.current_action)

    def movement(self):
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
            if speed_x + self.walking_offset > 0:
                self.flip = False
            else:
                self.flip = True

            if speed_x != 0:
                self.rect.move_ip(speed_x, sum([speed_y, self.walking_offset]))
            else:
                self.rect.move_ip(sum([speed_x, self.walking_offset]), speed_y)
            self.pos = (self.rect.x, self.rect.y)
            self.set_position(*self.pos)

    def check_collision(self):
        if pygame.sprite.collide_mask(self, self.game.collision_layer):
            return True
        return False

    def update(self):
        super().update()
        self.movement()
        if self.check_collision():
            self.calculate_movement(self.direction)
            self.set_position(*self.old_pos)
