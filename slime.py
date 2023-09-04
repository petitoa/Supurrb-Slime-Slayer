"""

    Supurrb Slime Slayer: Supurrb Slime Slayer is a 2D pixel-style game built with Python and Pygame. The goal of the game is to survive as long as possible while fending off spawning slimes and collecting orbs. 
    You control the cat character and can shoot projectiles to eliminate enemies.
    Copyright (C) 2023 petitoa

    This file is part of Supurrb Slime Slayer.

    Supurrb Slime Slayer is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

    Supurrb Slime Slayer is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with Supurrb Slime Slayer. If not, see <https://www.gnu.org/licenses/>.

"""
import random

import pygame
from constants import *
from map import *
from pygame.locals import *


class Slime(pygame.sprite.Sprite):
    def __init__(self, matrix):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("slimes.png"), (70, 70))
        self.rect = self.image.get_rect()
        self.speed = 2
        self.path = []
        self.matrix = matrix
        self.spawn_slime()
        self.direction = random.choice(['right', 'left', 'down', 'up'])

    def find_empty_spawn_point(self, matrix):
        while True:
            row = random.randint(1, len(matrix) - 1)
            col = random.randint(1, len(matrix[row]) - 1)
            if matrix[row][col] == 0:
                return row, col

    def spawn_slime(self):
        row, col = self.find_empty_spawn_point(self.matrix)
        self.row = row
        self.col = col
        self.rect.x = col * CELL_SIZE
        self.rect.y = row * CELL_SIZE

    def move_slimes(self, game_map):
        # Check for collisions with walls first
        collisions = pygame.sprite.spritecollide(self, game_map.wall_group, False)
        if collisions:
            # If the slime hits a wall, change its speed direction
            self.speed *= -1

        new_rect = self.rect.copy()

        if self.direction == 'right':
            new_rect.x += self.speed
        elif self.direction == 'left':
            new_rect.x -= self.speed
        elif self.direction == 'down':
            new_rect.y += self.speed
        elif self.direction == 'up':
            new_rect.y -= self.speed

        # Apply the movement
        self.rect = new_rect
