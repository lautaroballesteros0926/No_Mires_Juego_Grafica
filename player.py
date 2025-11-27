# player.py
"""
Lógica del cuadrado del jugador
"""

import pygame
from config import (
    PLAYER_SIZE, PLAYER_START_X, PLAYER_START_Y,
    WHITE, RED
)


class Player:
    def __init__(self):
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.size = PLAYER_SIZE
        self.color = WHITE
        self.is_alive = True
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
    
    def check_collision(self, walls):
        """
        Verifica si el jugador colisiona con alguna pared
        """
        left_wall, right_wall = walls
        
        if self.rect.colliderect(left_wall.rect) or self.rect.colliderect(right_wall.rect):
            self.is_alive = False
            self.color = RED
            return True
        
        return False
    
    def draw(self, screen):
        """
        Dibuja el cuadrado del jugador
        """
        pygame.draw.rect(screen, self.color, self.rect)
    
    def reset(self):
        """
        Reinicia el estado del jugador
        """
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.color = WHITE
        self.is_alive = True
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)