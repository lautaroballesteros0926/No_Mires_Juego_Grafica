import pygame
import math
from config import (
    PLAYER_SIZE, PLAYER_START_X, PLAYER_START_Y,
    WHITE, RED, CYAN, WINDOW_WIDTH
)
from effects import draw_glow_rect


class Player:
    def __init__(self):
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.size = PLAYER_SIZE
        self.color = CYAN
        self.is_alive = True
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.danger_level = 0.0
    
    def update_danger_level(self, walls):
        """
        Calcula el nivel de peligro basado en la proximidad de las paredes
        """
        left_wall, right_wall = walls
        
        # Distancia a cada pared
        dist_left = self.rect.left - left_wall.rect.right
        dist_right = right_wall.rect.left - self.rect.right
        
        # Distancia mínima
        min_dist = min(dist_left, dist_right)
        max_safe_dist = WINDOW_WIDTH // 4
        
        # Calcular nivel de peligro (0.0 = seguro, 1.0 = muy peligroso)
        if min_dist <= 0:
            self.danger_level = 1.0
        else:
            self.danger_level = max(0.0, 1.0 - (min_dist / max_safe_dist))
    
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
        Dibuja el cuadrado del jugador con efecto de brillo
        """
        if not self.is_alive:
            # Dibujar sin brillo si está muerto
            pygame.draw.rect(screen, RED, self.rect)
        else:
            # Efecto de pulso basado en el tiempo
            pulse = abs(math.sin(pygame.time.get_ticks() / 300))
            
            # Color base con pulso
            r = int(CYAN[0] + (255 - CYAN[0]) * pulse * 0.3)
            g = int(CYAN[1] + (255 - CYAN[1]) * pulse * 0.3)
            b = int(CYAN[2])
            color = (r, g, b)
            
            # Tamaño del brillo aumenta con el peligro
            glow_size = int(5 + self.danger_level * 10)
            
            # Dibujar con efecto de brillo
            draw_glow_rect(screen, color, self.rect, glow_size)
    
    def reset(self):
        """
        Reinicia el estado del jugador
        """
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.color = CYAN
        self.is_alive = True
        self.danger_level = 0.0
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)