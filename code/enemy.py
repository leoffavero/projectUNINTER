#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import pygame

from code.Const import ENTITY_SPEED, WIN_WIDTH, WIN_HEIGHT
from code.entity import Entity


class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.direction = -1  # os inimigos começam indo para a esquerda

    def move(self):
        self.rect.x += self.direction * ENTITY_SPEED[self.name]

        # se sair da tela, reposiciona do outro lado
        if self.rect.right < 0:
            self.rect.x = WIN_WIDTH
            self.rect.y = random.randint(40, WIN_HEIGHT - 40)

# #!/usr/bin/python
# # -*- coding: utf-8 -*-
# from code.Const import ENTITY_SPEED, ENTITY_SHOT_DELAY
# from code.EnemyShot import EnemyShot
# from code.Entity import Entity
#
#
# class Enemy(Entity):
#     def __init__(self, name: str, position: tuple):
#         super().__init__(name, position)
#         self.shot_delay = ENTITY_SHOT_DELAY[self.name]
#
#     def move(self):
#         self.rect.centerx -= ENTITY_SPEED[self.name]
#
#     def shoot(self):
#         self.shot_delay -= 1
#         if self.shot_delay == 0:
#             self.shot_delay = ENTITY_SHOT_DELAY[self.name]
#             return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))
