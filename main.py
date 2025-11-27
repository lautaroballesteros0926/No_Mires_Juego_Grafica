# main.py
"""
Programa principal del juego de mecanografía con detección de ojos
"""

import pygame
import sys
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, BLACK,
    TOLERANCE_TIME
)
from camera import Camera
from player import Player
from walls import WallManager
from phrase_manager import PhraseManager
from ui import UI


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Juego de Mecanografía - No Mires")
        self.clock = pygame.time.Clock()
        
        # Componentes del juego
        self.camera = Camera()
        self.player = Player()
        self.walls = WallManager()
        self.phrase_manager = PhraseManager()
        self.ui = UI(self.screen)
        
        # Estados del juego
        self.game_state = "MEMORIZING"  # MEMORIZING, PLAYING, GAME_OVER, VICTORY
        self.tolerance_timer = TOLERANCE_TIME
        self.start_ticks = pygame.time.get_ticks()
        
        # Generar primera frase
        self.current_phrase = self.phrase_manager.get_random_phrase()
        
        self.running = True
    
    def handle_events(self):
        """
        Maneja los eventos de Pygame
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                # Reiniciar con ESPACIO en estados finales
                if event.key == pygame.K_SPACE and self.game_state in ["GAME_OVER", "VICTORY"]:
                    self.reset_game()
                
                # Durante el juego, capturar entrada de texto
                elif self.game_state == "PLAYING":
                    if event.key == pygame.K_RETURN:
                        # Verificar la frase
                        if self.phrase_manager.check_phrase():
                            self.game_state = "VICTORY"
                    
                    elif event.key == pygame.K_BACKSPACE:
                        # Borrar último carácter
                        self.phrase_manager.remove_character()
                    
                    else:
                        # Añadir carácter si es válido
                        if event.unicode.isprintable():
                            self.phrase_manager.add_character(event.unicode)
    
    def update(self):
        """
        Actualiza la lógica del juego
        """
        # Detectar estado de los ojos
        eyes_open = self.camera.detect_eyes()
        
        if self.game_state == "MEMORIZING":
            # Cuenta regresiva de tolerancia
            seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
            self.tolerance_timer = TOLERANCE_TIME - seconds
            
            if self.tolerance_timer <= 0:
                self.game_state = "PLAYING"
                self.tolerance_timer = 0
        
        elif self.game_state == "PLAYING":
            # Si los ojos están abiertos, mover las paredes
            if eyes_open:
                self.walls.start_moving()
            else:
                self.walls.stop_moving()
            
            # Actualizar paredes
            self.walls.update()
            
            # Verificar colisiones
            if self.player.check_collision(self.walls.get_walls()):
                self.game_state = "GAME_OVER"
                self.walls.stop_moving()
    
    def draw(self):
        """
        Dibuja todos los elementos del juego
        """
        # Fondo negro
        self.screen.fill(BLACK)
        
        # Dibujar elementos del juego
        self.walls.draw(self.screen)
        self.player.draw(self.screen)
        
        # Dibujar feed de la webcam
        frame = self.camera.get_frame()
        self.ui.draw_webcam_feed(frame)
        
        if self.game_state == "MEMORIZING":
            # Mostrar frase y cuenta regresiva
            self.ui.draw_phrase(self.current_phrase, show=True)
            self.ui.draw_countdown(self.tolerance_timer)
            self.ui.draw_instructions()
        
        elif self.game_state == "PLAYING":
            # Mostrar frase y input del usuario
            self.ui.draw_phrase(self.current_phrase, show=True)
            self.ui.draw_user_input(self.phrase_manager.get_user_input())
        
        elif self.game_state == "GAME_OVER":
            self.ui.draw_game_over()
        
        elif self.game_state == "VICTORY":
            self.ui.draw_victory()
        
        pygame.display.flip()
    
    def reset_game(self):
        """
        Reinicia el juego para una nueva ronda
        """
        self.player.reset()
        self.walls.reset()
        self.current_phrase = self.phrase_manager.get_random_phrase()
        self.game_state = "MEMORIZING"
        self.tolerance_timer = TOLERANCE_TIME
        self.start_ticks = pygame.time.get_ticks()
    
    def run(self):
        """
        Bucle principal del juego
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        # Limpieza
        self.camera.release()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()