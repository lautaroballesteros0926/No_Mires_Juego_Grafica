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
        
        # Sistema de animación
        self.sprite_sheets = {}
        self.animations = {}
        self.current_animation = 'idle'
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.15  # Velocidad de animación
        
        # Cargar sprites
        self._load_sprites()
    
    def _load_sprites(self):
        """
        Carga los sprite sheets y extrae frames individuales
        """
        # Definir configuración de cada sprite sheet
        sprite_config = {
            'idle': {'path': 'assets/pj/Idle.png', 'frames': 8},
            'walk': {'path': 'assets/pj/Walk.png', 'frames': 8},
            'run': {'path': 'assets/pj/Run.png', 'frames': 7},
            'dead': {'path': 'assets/pj/Dead.png', 'frames': 5}
        }
        
        # Cargar cada sprite sheet
        for anim_name, config in sprite_config.items():
            try:
                # Cargar imagen completa
                sheet = pygame.image.load(config['path']).convert_alpha()
                
                # Extraer frames individuales
                frames = []
                frame_width = sheet.get_width() // config['frames']
                frame_height = sheet.get_height()
                
                for i in range(config['frames']):
                    # Extraer frame
                    frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
                    frame = sheet.subsurface(frame_rect)
                    
                    # Escalar al tamaño del jugador
                    scaled_frame = pygame.transform.scale(frame, (self.size, self.size))
                    frames.append(scaled_frame)
                
                self.animations[anim_name] = frames
                print(f"[OK] Cargado sprite '{anim_name}' con {len(frames)} frames")
                
            except Exception as e:
                print(f"[ERROR] Error cargando sprite {anim_name}: {e}")
                # Crear un sprite de respaldo (cuadrado de color)
                fallback_surface = pygame.Surface((self.size, self.size))
                fallback_surface.fill(CYAN if anim_name != 'dead' else RED)
                self.animations[anim_name] = [fallback_surface]
    
    def update_danger_level(self, walls):
        """
        Calcula el nivel de peligro basado en la proximidad de las paredes
        También ajusta la posición del jugador para que no se salga de las paredes
        """
        left_wall, right_wall = walls
        
        # Mantener al jugador dentro de los límites de las paredes
        # Limitar por la izquierda
        if self.rect.left < left_wall.rect.right:
            self.x = left_wall.rect.right
            self.rect.x = self.x
        
        # Limitar por la derecha
        if self.rect.right > right_wall.rect.left:
            self.x = right_wall.rect.left - self.size
            self.rect.x = self.x
        
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
    
    def update_animation(self, game_state, is_typing):
        """
        Actualiza la animación según el estado del juego
        
        Args:
            game_state: Estado actual del juego
            is_typing: Si el jugador está escribiendo
        """
        # Verificar que las animaciones estén cargadas
        if not self.animations:
            return
        
        # Determinar qué animación usar
        previous_animation = self.current_animation
        
        if not self.is_alive:
            self.current_animation = 'dead'
        elif self.danger_level > 0.6:
            # Peligro alto: correr
            self.current_animation = 'run'
        elif is_typing or game_state == "PLAYING":
            # Escribiendo: caminar
            self.current_animation = 'walk'
        else:
            # Inactivo: idle
            self.current_animation = 'idle'
        
        # Verificar que la animación existe
        if self.current_animation not in self.animations:
            self.current_animation = 'idle'
        
        # Si cambió la animación, reiniciar el índice
        if previous_animation != self.current_animation:
            self.frame_index = 0
            self.animation_timer = 0
        
        # Avanzar frame de animación
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            # Ciclar al siguiente frame
            if self.current_animation in self.animations and len(self.animations[self.current_animation]) > 0:
                num_frames = len(self.animations[self.current_animation])
                self.frame_index = (self.frame_index + 1) % num_frames
    
    def draw(self, screen):
        """
        Dibuja el sprite animado del jugador
        """
        # Obtener frame actual
        if self.current_animation in self.animations and len(self.animations[self.current_animation]) > 0:
            current_frame = self.animations[self.current_animation][self.frame_index]
            
            # Dibujar sprite
            screen.blit(current_frame, (self.x, self.y))
            
            # Opcional: añadir efecto de brillo sutil cuando hay peligro
            if self.is_alive and self.danger_level > 0.5:
                # Crear superficie semi-transparente para el brillo
                glow_size = int(self.danger_level * 10)
                if glow_size > 0:
                    glow_rect = pygame.Rect(
                        self.x - glow_size,
                        self.y - glow_size,
                        self.size + glow_size * 2,
                        self.size + glow_size * 2
                    )
                    # Dibujar brillo rojo sutil
                    glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                    alpha = int(self.danger_level * 100)
                    pygame.draw.rect(glow_surface, (255, 0, 0, alpha), glow_surface.get_rect(), border_radius=5)
                    screen.blit(glow_surface, (glow_rect.x, glow_rect.y))
        else:
            # Fallback: dibujar cuadrado
            pygame.draw.rect(screen, self.color, self.rect)
    
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
        self.current_animation = 'idle'
        self.frame_index = 0
        self.animation_timer = 0