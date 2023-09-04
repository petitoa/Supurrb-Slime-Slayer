"""

    Supurrb Slime Slayer: Supurrb Slime Slayer is a 2D pixel-style game built with Python and Pygame. The goal of the game is to survive as long as possible while fending off spawning slimes and collecting orbs. 
    You control the cat character and can shoot projectiles to eliminate enemies.
    Copyright (C) 2023 petitoa

    This file is part of Supurrb Slime Slayer.

    Supurrb Slime Slayer is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

    Supurrb Slime Slayer is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with Supurrb Slime Slayer. If not, see <https://www.gnu.org/licenses/>.

"""
import pygame
from constants import *
from pygame.locals import *


class Cat(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("cat.png"), (70, 70))
        self.rect = self.image.get_rect()
        screen_center = pygame.display.get_surface().get_rect().center
        self.rect.center = screen_center
        self.speed = 5
        self.health = 100
        self.score = 0

    def move_cat(self, keys, game_map):
        temp_cat = pygame.sprite.Sprite()
        temp_cat.rect = self.rect.copy()  # Make a copy of the cat's rectangle to use for collision detection

        if keys[pygame.K_w]:
            temp_cat.rect.y -= self.speed
        if keys[pygame.K_a]:
            temp_cat.rect.x -= self.speed
        if keys[pygame.K_s]:
            temp_cat.rect.y += self.speed
        if keys[pygame.K_d]:
            temp_cat.rect.x += self.speed

        # Check for collision with walls
        if not game_map.check_collision(temp_cat):
            self.rect = temp_cat.rect  # Update cat's position if no collision


class Bullet(pygame.sprite.Sprite):
    def __init__(self, cat_rect, direction):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=cat_rect.center)
        self.speed = 7
        self.direction = direction

    def update(self):
        if self.direction == pygame.K_UP:
            self.rect.y -= self.speed
        elif self.direction == pygame.K_DOWN:
            self.rect.y += self.speed
        elif self.direction == pygame.K_LEFT:
            self.rect.x -= self.speed
        elif self.direction == pygame.K_RIGHT:
            self.rect.x += self.speed

        if self.rect.x >= SCREEN_WIDTH and self.rect.y >= SCREEN_HEIGHT:
            self.kill()
