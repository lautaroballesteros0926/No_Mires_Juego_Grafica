# walls.py
"""
Lógica de las paredes que se cierran
"""

import pygame
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WALL_WIDTH, WALL_SPEED,
    WALL_START_LEFT, WALL_START_RIGHT, WHITE
)


class Wall:
    def __init__(self, x, side):
        """
        side: 'left' o 'right'
        """
        self.x = x
        self.side = side
        self.width = WALL_WIDTH
        self.height = WINDOW_HEIGHT
        self.color = WHITE
        self.rect = pygame.Rect(self.x, 0, self.width, self.height)
        self.initial_x = x
    
    def move(self):
        """
        Mueve la pared hacia el centro
        """
        if self.side == 'left':
            self.x += WALL_SPEED
        else:  # right
            self.x -= WALL_SPEED
        
        self.rect.x = self.x
    
    def draw(self, screen):
        """
        Dibuja la pared
        """
        pygame.draw.rect(screen, self.color, self.rect)
    
    def reset(self):
        """
        Reinicia la posición de la pared
        """
        self.x = self.initial_x
        self.rect.x = self.x


class WallManager:
    def __init__(self):
        self.left_wall = Wall(WALL_START_LEFT, 'left')
        self.right_wall = Wall(WALL_START_RIGHT, 'right')
        self.moving = False
    
    def start_moving(self):
        """
        Inicia el movimiento de las paredes
        """
        self.moving = True
    
    def stop_moving(self):
        """
        Detiene el movimiento de las paredes
        """
        self.moving = False
    
    def update(self):
        """
        Actualiza las paredes si están en movimiento
        """
        if self.moving:
            self.left_wall.move()
            self.right_wall.move()
    
    def draw(self, screen):
        """
        Dibuja ambas paredes
        """
        self.left_wall.draw(screen)
        self.right_wall.draw(screen)
    
    def get_walls(self):
        """
        Retorna ambas paredes para detección de colisiones
        """
        return [self.left_wall, self.right_wall]
    
    def reset(self):
        """
        Reinicia las paredes a su posición inicial
        """
        self.left_wall.reset()
        self.right_wall.reset()
        self.moving = False