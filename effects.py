import pygame
import random
import math


class Particle:
    def __init__(self, x, y, color, velocity_x=None, velocity_y=None):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.lifetime = random.randint(20, 40)
        self.max_lifetime = self.lifetime
        self.velocity_x = velocity_x if velocity_x else random.uniform(-2, 2)
        self.velocity_y = velocity_y if velocity_y else random.uniform(-2, 2)
        self.alpha = 255
    
    def update(self):
        """Actualiza la posición y vida de la particula"""
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.lifetime -= 1
        self.alpha = int(255 * (self.lifetime / self.max_lifetime))
        return self.lifetime > 0
    
    def draw(self, screen):
        """Dibuja la particula con transparencia"""
        if self.alpha > 0:
            # Crear superficie temporal con alpha
            surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            color_with_alpha = (*self.color, self.alpha)
            pygame.draw.circle(surf, color_with_alpha, (self.size, self.size), self.size)
            screen.blit(surf, (int(self.x - self.size), int(self.y - self.size)))


class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def emit(self, x, y, color, count=5, direction=None):
        """
        Emite particulas desde una posicion
        """
        for _ in range(count):
            if direction == 'left':
                vx = random.uniform(-3, -1)
                vy = random.uniform(-1, 1)
            elif direction == 'right':
                vx = random.uniform(1, 3)
                vy = random.uniform(-1, 1)
            elif direction == 'up':
                vx = random.uniform(-1, 1)
                vy = random.uniform(-3, -1)
            elif direction == 'down':
                vx = random.uniform(-1, 1)
                vy = random.uniform(1, 3)
            else:
                vx = None
                vy = None
            
            particle = Particle(x, y, color, vx, vy)
            self.particles.append(particle)
    
    def update(self):
        """Actualiza todas las partículas y elimina las muertas"""
        self.particles = [p for p in self.particles if p.update()]
    
    def draw(self, screen):
        """Dibuja todas las partículas"""
        for particle in self.particles:
            particle.draw(screen)
    
    def clear(self):
        """Elimina todas las partículas"""
        self.particles.clear()


class ScreenShake:
    def __init__(self):
        self.shake_amount = 0
        self.shake_duration = 0
        self.offset_x = 0
        self.offset_y = 0
    
    def start(self, intensity=10, duration=10):
        """
        Inicia el efecto de screen shake
        """
        self.shake_amount = intensity
        self.shake_duration = duration
    
    def update(self):
        """Actualiza el offset del screen shake"""
        if self.shake_duration > 0:
            self.offset_x = random.randint(-self.shake_amount, self.shake_amount)
            self.offset_y = random.randint(-self.shake_amount, self.shake_amount)
            self.shake_duration -= 1
        else:
            self.offset_x = 0
            self.offset_y = 0
    
    def get_offset(self):
        """Retorna el offset actual (x, y)"""
        return (self.offset_x, self.offset_y)
    
    def is_shaking(self):
        """Verifica si está activo el shake"""
        return self.shake_duration > 0


class ColorManager:
    def __init__(self):
        self.danger_level = 0  # 0.0 a 1.0
        self.base_bg_color = (10, 10, 20)  # Azul oscuro
        self.danger_bg_color = (80, 10, 10)  # Rojo oscuro
    
    def set_danger_level(self, level):
        """
        Establece el nivel de peligro (0.0 = seguro, 1.0 = máximo peligro)
        """
        self.danger_level = max(0.0, min(1.0, level))
    
    def get_background_color(self):
        """
        Retorna el color de fondo interpolado según el nivel de peligro
        """
        r = int(self.base_bg_color[0] + (self.danger_bg_color[0] - self.base_bg_color[0]) * self.danger_level)
        g = int(self.base_bg_color[1] + (self.danger_bg_color[1] - self.base_bg_color[1]) * self.danger_level)
        b = int(self.base_bg_color[2] + (self.danger_bg_color[2] - self.base_bg_color[2]) * self.danger_level)
        return (r, g, b)
    
    def get_wall_color(self):
        """
        Retorna el color de las paredes segun el peligro (COLORES MUY SUAVES)
        """
        if self.danger_level < 0.3:
            return (0, 120, 120)  # Cyan muy suave
        elif self.danger_level < 0.6:
            return (140, 140, 0)  # Amarillo muy suave
        else:
            return (140, 0, 140)  # Magenta muy suave
    
    def get_player_color(self):
        """
        Retorna el color del jugador con efecto de pulso
        """
        pulse = abs(math.sin(pygame.time.get_ticks() / 200))
        base = 100 + int(30 * pulse)  # Muy reducido
        return (base, base, 150)  # Azul muy suave


def draw_glow_rect(surface, color, rect, glow_size=5):
    """
    Dibuja un rectangulo con efecto de brillo suave
    """
    if isinstance(rect, tuple):
        rect = pygame.Rect(rect)
    
    # Dibujar capas de brillo con transparencia decreciente (MÍNIMO)
    for i in range(glow_size, 0, -1):
        alpha = int(20 * (i / glow_size))  # Reducido a 20 para efecto mínimo
        glow_surf = pygame.Surface((rect.width + i*2, rect.height + i*2), pygame.SRCALPHA)
        glow_color = (*color, alpha)
        pygame.draw.rect(glow_surf, glow_color, glow_surf.get_rect(), border_radius=5)
        surface.blit(glow_surf, (rect.x - i, rect.y - i))
    
    # Dibujar rectángulo sólido
    pygame.draw.rect(surface, color, rect, border_radius=3)


def draw_glow_text(surface, font, text, pos, color, glow_size=3):
    """
    Dibuja texto con efecto de brillo SUAVE
    """
    # Renderizar texto con antialiasing
    text_surface = font.render(text, True, color)  # True = antialiasing
    text_rect = text_surface.get_rect(center=pos)
    
    # Dibujar capas de brillo MÍNIMAS
    for i in range(glow_size, 0, -1):
        alpha = int(25 * (i / glow_size))  # Reducido a 25 para efecto mínimo
        glow_surf = font.render(text, True, (*color, alpha) if len(color) == 3 else color)
        glow_rect = glow_surf.get_rect(center=(pos[0], pos[1]))
        
        # Dibujar en múltiples posiciones para efecto de brillo
        for dx in [-i, 0, i]:
            for dy in [-i, 0, i]:
                if dx != 0 or dy != 0:
                    surface.blit(glow_surf, (glow_rect.x + dx, glow_rect.y + dy))
    
    # Dibujar texto principal
    surface.blit(text_surface, text_rect)
    return text_rect
