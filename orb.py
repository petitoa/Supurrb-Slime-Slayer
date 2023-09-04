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


class Orb(pygame.sprite.Sprite):
    def __init__(self, matrix):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("orb.png"), (50, 50))
        self.rect = self.image.get_rect()
        self.matrix = matrix
        self.spawn_orb()

    def find_empty_spawn_point(self, matrix):
        while True:
            row = random.randint(1, len(matrix) - 1)
            col = random.randint(1, len(matrix[row]) - 1)
            if matrix[row][col] == 0:
                return row, col

    def spawn_orb(self):
        row, col = self.find_empty_spawn_point(self.matrix)
        self.row = row
        self.col = col
        self.rect.x = col * CELL_SIZE
        self.rect.y = row * CELL_SIZE
