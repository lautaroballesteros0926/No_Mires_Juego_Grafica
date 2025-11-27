import pygame
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WALL_WIDTH,
    WALL_START_LEFT, WALL_START_RIGHT, PARTICLE_COUNT
)
from effects import draw_glow_rect


class Wall:
    def __init__(self, x, side):
        """
        side: 'left' o 'right'
        """
        self.x = x
        self.side = side
        self.width = WALL_WIDTH
        self.height = WINDOW_HEIGHT
        self.rect = pygame.Rect(self.x, 0, self.width, self.height)
        self.initial_x = x
        self.speed = 0
        self.particle_timer = 0
    
    def set_speed(self, speed):
        """
        Establece la velocidad de la pared
        """
        self.speed = speed
    
    def move(self):
        """
        Mueve la pared hacia el centro
        """
        if self.side == 'left':
            self.x += self.speed
        else:  # right
            self.x -= self.speed
        
        self.rect.x = self.x
    
    def draw(self, screen, color, particle_system=None):
        """
        Dibuja la pared con efecto de brillo
        """
        # Dibujar con efecto de brillo
        draw_glow_rect(screen, color, self.rect, glow_size=8)
        
        # Emitir partículas si se esta moviendo
        if particle_system and self.speed > 0:
            self.particle_timer += 1
            if self.particle_timer >= 3:  # Emitir cada 3 frames
                self.particle_timer = 0
                
                # Posición de emision (borde interno de la pared)
                if self.side == 'left':
                    emit_x = self.rect.right
                    direction = 'right'
                else:
                    emit_x = self.rect.left
                    direction = 'left'
                
                # Emitir particulas a lo largo de la altura
                for i in range(PARTICLE_COUNT):
                    emit_y = self.rect.top + (self.rect.height * i // PARTICLE_COUNT)
                    particle_system.emit(emit_x, emit_y, color, count=2, direction=direction)
    
    def reset(self):
        """
        Reinicia la posicion de la pared
        """
        self.x = self.initial_x
        self.rect.x = self.x
        self.speed = 0
        self.particle_timer = 0


class WallManager:
    def __init__(self):
        self.left_wall = Wall(WALL_START_LEFT, 'left')
        self.right_wall = Wall(WALL_START_RIGHT, 'right')
        self.moving = False
        self.current_speed = 0
    
    def set_speed(self, speed):
        """
        Establece la velocidad de ambas paredes
        """
        self.current_speed = speed
        self.left_wall.set_speed(speed)
        self.right_wall.set_speed(speed)
    
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
        Actualiza las paredes si estan en movimiento
        """
        if self.moving:
            self.left_wall.move()
            self.right_wall.move()
    
    def draw(self, screen, color, particle_system=None):
        """
        Dibuja ambas paredes con efectos
        """
        self.left_wall.draw(screen, color, particle_system)
        self.right_wall.draw(screen, color, particle_system)
    
    def get_walls(self):
        """
        Retorna ambas paredes para detección de colisiones
        """
        return [self.left_wall, self.right_wall]
    
    def reset(self):
        """
        Reinicia las paredes a su posicion inicial
        """
        self.left_wall.reset()
        self.right_wall.reset()
        self.moving = False
        self.current_speed = 0