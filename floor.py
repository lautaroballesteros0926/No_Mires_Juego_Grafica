import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT

class Floor:
    def __init__(self):
        try:
            # Cargar la imagen del suelo
            self.tile_image = pygame.image.load('assets/land/tile_0196.png').convert_alpha()
            # Escalar si es necesario (opcional, por ahora usamos tamaño original)
            self.tile_width = self.tile_image.get_width()
            self.tile_height = self.tile_image.get_height()
            
            # Calcular cuántos tiles necesitamos para cubrir el ancho
            self.tiles_x = (WINDOW_WIDTH // self.tile_width) + 1
            
            # Posición Y del suelo (parte inferior de la pantalla)
            # Asumimos que queremos una fila de tiles en la parte inferior
            self.y_pos = WINDOW_HEIGHT - self.tile_height
            
        except Exception as e:
            print(f"Error cargando assets del suelo: {e}")
            self.tile_image = None

    def draw(self, screen):
        if self.tile_image:
            for i in range(self.tiles_x):
                screen.blit(self.tile_image, (i * self.tile_width, self.y_pos))
        else:
            # Fallback si no hay imagen: dibujar una línea gris
            pygame.draw.rect(screen, (50, 50, 50), (0, WINDOW_HEIGHT - 20, WINDOW_WIDTH, 20))
