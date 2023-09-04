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
from cat import Cat, Bullet
from constants import *
from map import Map
from orb import Orb
from pygame.locals import *
from slime import Slime

ADD_SLIME_EVENT = pygame.USEREVENT + 1
ADD_ORB_EVENT = pygame.USEREVENT + 2


def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Supurrb Slime Slayer")

    game_map = Map()
    cat = Cat()

    cat_sprites = pygame.sprite.Group(cat)
    slime_sprites = pygame.sprite.Group()
    orb_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()

    pygame.time.set_timer(ADD_SLIME_EVENT, 2000)
    pygame.time.set_timer(ADD_ORB_EVENT, 7000)

    # Event loop
    previous_projectile_time = pygame.time.get_ticks()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == ADD_SLIME_EVENT:
                slime = Slime(game_map.matrix)
                # Check for collisions with walls
                while pygame.sprite.spritecollide(slime, game_map.wall_group, False):
                    # If a collision is detected, reposition the slime until it's in a valid spot
                    slime = Slime(game_map.matrix)
                slime_sprites.add(slime)
            if event.type == ADD_ORB_EVENT:
                orb = Orb(game_map.matrix)
                # Check for collisions with walls
                while pygame.sprite.spritecollide(orb, game_map.wall_group, False):
                    # If a collision is detected, reposition the slime until it's in a valid spot
                    orb = Orb(game_map.matrix)
                orb_sprites.add(orb)
            # Handle bullet fire rate and key press
            projectile_time = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                if projectile_time - previous_projectile_time > BULLET_FIRE_RATE:
                    previous_projectile_time = projectile_time
                    bullet = Bullet(cat.rect, pygame.K_UP)
                    bullet_sprites.add(bullet)
            elif keys[pygame.K_DOWN]:
                if projectile_time - previous_projectile_time > BULLET_FIRE_RATE:
                    previous_projectile_time = projectile_time
                    bullet = Bullet(cat.rect, pygame.K_DOWN)
                    bullet_sprites.add(bullet)
            elif keys[pygame.K_LEFT]:
                if projectile_time - previous_projectile_time > BULLET_FIRE_RATE:
                    previous_projectile_time = projectile_time
                    bullet = Bullet(cat.rect, pygame.K_LEFT)
                    bullet_sprites.add(bullet)
            elif keys[pygame.K_RIGHT]:
                if projectile_time - previous_projectile_time > BULLET_FIRE_RATE:
                    previous_projectile_time = projectile_time
                    bullet = Bullet(cat.rect, pygame.K_RIGHT)
                    bullet_sprites.add(bullet)

        bullet_sprites.update()

        # If cat health is zero
        if cat.health <= 0:
            cat.score = 0  # Reset the score
            cat.health = 100  # Reset cat's health

            # Clear all sprites except cat
            slime_sprites.empty()
            orb_sprites.empty()
            bullet_sprites.empty()

        # Check for collisions between the cat and slime
        cat_slime_collisions = pygame.sprite.spritecollide(cat, slime_sprites,
                                                           True)  # True removes the slime on collision
        if cat_slime_collisions:
            cat.health -= 10

        bullet_slime_collisions = pygame.sprite.groupcollide(bullet_sprites, slime_sprites, True, True)
        if bullet_slime_collisions:
            cat.score += 100

        orb_cat_collisions = pygame.sprite.spritecollide(cat, orb_sprites, True)
        if orb_cat_collisions:
            cat.score += 250

        pygame.sprite.groupcollide(bullet_sprites, game_map.wall_group, True, False)

        cat.move_cat(keys, game_map)

        # Slimes movement
        for slime in slime_sprites.sprites():
            slime.move_slimes(game_map)

        screen.fill(SOFT_BLUE)

        cat_sprites.draw(screen)  # Draw all sprites including the cat
        bullet_sprites.draw(screen)
        slime_sprites.draw(screen)
        orb_sprites.draw(screen)

        # Draw the map
        game_map.draw(screen)

        # Display score and health
        GAME_FONT = pygame.font.SysFont("Arial", 18, 1, 1)
        score_text = GAME_FONT.render("Score: " + str(cat.score), False, pygame.Color(YELLOW))
        health_text = GAME_FONT.render("Health: " + str(cat.health), False, pygame.Color(YELLOW))

        # Create a black background rectangle behind both texts
        background_rect = pygame.Rect(10, 10, max(score_text.get_width(), health_text.get_width()),
                                      2 * score_text.get_height())
        pygame.draw.rect(screen, pygame.Color(BLACK), background_rect)

        # Blit the text on top of the black background
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 10 + score_text.get_height()))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()