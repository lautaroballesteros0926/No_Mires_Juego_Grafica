import pygame
import sys
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    TOLERANCE_TIME
)
from camera import Camera
from player import Player
from walls import WallManager
from phrase_manager import PhraseManager
from ui import UI
from level_manager import LevelManager
from score_manager import ScoreManager
from effects import ParticleSystem, ScreenShake, ColorManager


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("No Mires - Typing Game")
        self.clock = pygame.time.Clock()
        
        # Componentes del juego
        self.camera = Camera()
        self.player = Player()
        self.walls = WallManager()
        self.phrase_manager = PhraseManager()
        self.ui = UI(self.screen)
        
        # Nuevos sistemas
        self.level_manager = LevelManager()
        self.score_manager = ScoreManager()
        self.particle_system = ParticleSystem()
        self.screen_shake = ScreenShake()
        self.color_manager = ColorManager()
        
        # Estados del juego
        self.game_state = "MEMORIZING"  # MEMORIZING, PLAYING, LEVEL_COMPLETE, GAME_OVER, GAME_COMPLETE
        self.tolerance_timer = TOLERANCE_TIME
        self.start_ticks = pygame.time.get_ticks()
        
        # Iniciar primer nivel
        self.start_new_level()
        
        self.running = True
    
    def start_new_level(self):
        """
        Inicia un nuevo nivel
        """
        current_level = self.level_manager.get_current_level()
        if current_level:
            # Reiniciar componentes PRIMERO
            self.player.reset()
            self.walls.reset()
            self.score_manager.reset_level()
            self.particle_system.clear()
            
            # Configurar velocidad de paredes según el nivel
            self.walls.set_speed(current_level.wall_speed)
            
            # Configurar tiempo de tolerancia
            self.tolerance_timer = current_level.tolerance_time
            
            # Obtener frase según dificultad del nivel
            self.current_phrase = self.phrase_manager.get_random_phrase(current_level.phrase_difficulty)
            
            # Reiniciar estado
            self.game_state = "MEMORIZING"
            self.start_ticks = pygame.time.get_ticks()
    
    def handle_events(self):
        """
        Maneja los eventos de Pygame
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                # Reiniciar con ESPACIO en estados finales
                if event.key == pygame.K_SPACE:
                    if self.game_state == "GAME_OVER":
                        self.level_manager.reset()
                        self.score_manager.reset_game()
                        self.start_new_level()
                    
                    elif self.game_state == "LEVEL_COMPLETE":
                        # Avanzar al siguiente nivel
                        if self.level_manager.next_level():
                            self.start_new_level()
                        else:
                            self.game_state = "GAME_COMPLETE"
                    
                    elif self.game_state == "GAME_COMPLETE":
                        # Reiniciar todo el juego
                        self.level_manager.reset()
                        self.score_manager.reset_game()
                        self.start_new_level()
                
                # Durante el juego, capturar entrada de texto
                elif self.game_state == "PLAYING":
                    if event.key == pygame.K_RETURN:
                        # Verificar la frase
                        if self.phrase_manager.check_phrase():
                            # Calcular puntuación del nivel
                            level_score = self.score_manager.complete_level(
                                self.level_manager.get_level_number()
                            )
                            self.game_state = "LEVEL_COMPLETE"
                            self.walls.stop_moving()
                    
                    elif event.key == pygame.K_BACKSPACE:
                        # Borrar ultimo carácter
                        self.phrase_manager.remove_character()
                    
                    else:
                        # Añadir caracter si es valido
                        if event.unicode.isprintable():
                            # Verificar si el caracter es correcto
                            current_input = self.phrase_manager.get_user_input()
                            expected_char = self.current_phrase[len(current_input)] if len(current_input) < len(self.current_phrase) else None
                            
                            if event.unicode == expected_char:
                                self.score_manager.add_correct_character()
                            else:
                                self.score_manager.add_incorrect_character()
                            
                            self.phrase_manager.add_character(event.unicode)
    
    def update(self):
        """
        Actualiza la logica del juego
        """
        # Detectar estado de los ojos
        eyes_open = self.camera.detect_eyes()
        
        # Actualizar sistema de puntuacion de ojos cerrados
        if not eyes_open and self.game_state == "PLAYING":
            self.score_manager.start_eyes_closed()
        else:
            self.score_manager.stop_eyes_closed()
        
        if self.game_state == "MEMORIZING":
            # Cuenta regresiva de tolerancia
            seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
            self.tolerance_timer = self.level_manager.get_current_level().tolerance_time - seconds
            
            if self.tolerance_timer <= 0:
                self.game_state = "PLAYING"
                self.tolerance_timer = 0
                self.score_manager.start_typing()
        
        elif self.game_state == "PLAYING":
            # Si los ojos estan abiertos, mover las paredes
            if eyes_open:
                self.walls.start_moving()
            else:
                self.walls.stop_moving()
            
            # Actualizar paredes
            self.walls.update()
            
            # Actualizar nivel de peligro del jugador
            self.player.update_danger_level(self.walls.get_walls())
            
            # Actualizar color manager segun peligro
            self.color_manager.set_danger_level(self.player.danger_level)
            
            # Screen shake si hay mucho peligro
            if self.player.danger_level > 0.7 and not self.screen_shake.is_shaking():
                intensity = int(self.player.danger_level * 15)
                self.screen_shake.start(intensity, 8)
            
            # Verificar colisiones
            if self.player.check_collision(self.walls.get_walls()):
                self.game_state = "GAME_OVER"
                self.walls.stop_moving()
                self.screen_shake.start(20, 20)
        
        # Actualizar efectos visuales
        self.particle_system.update()
        self.screen_shake.update()
    
    def draw(self):
        """
        Dibuja todos los elementos del juego
        """
        # Obtener offset del screen shake
        shake_offset = self.screen_shake.get_offset()
        
        # Crear superficie temporal para aplicar shake
        game_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Fondo dinamico según peligro
        bg_color = self.color_manager.get_background_color()
        game_surface.fill(bg_color)
        
        # Dibujar elementos del juego
        wall_color = self.color_manager.get_wall_color()
        self.walls.draw(game_surface, wall_color, self.particle_system)
        self.player.draw(game_surface)
        
        # Dibujar particulas
        self.particle_system.draw(game_surface)
        
        # Aplicar screen shake
        self.screen.fill((0, 0, 0))
        self.screen.blit(game_surface, shake_offset)
        
        # Dibujar UI
        # Feed de la webcam
        frame = self.camera.get_frame()
        self.ui.draw_webcam_feed(frame)
        
        # HUD
        if self.game_state in ["PLAYING", "MEMORIZING"]:
            self.ui.draw_hud(
                self.level_manager.get_level_number(),
                self.score_manager.total_score,
                self.score_manager.combo,
                self.score_manager.calculate_wpm()
            )
        
        if self.game_state == "MEMORIZING":
            # Mostrar frase y cuenta regresiva
            self.ui.draw_phrase(self.current_phrase, show=True)
            self.ui.draw_countdown(self.tolerance_timer)
            self.ui.draw_instructions()
        
        elif self.game_state == "PLAYING":
            # Mostrar frase y input del usuario con feedback
            self.ui.draw_phrase(self.current_phrase, show=True)
            self.ui.draw_user_input_with_feedback(self.phrase_manager)
            
            # Indicador de peligro
            self.ui.draw_danger_indicator(self.player.danger_level)
        
        elif self.game_state == "LEVEL_COMPLETE":
            score_breakdown = self.score_manager.get_score_breakdown()
            self.ui.draw_level_complete(
                self.level_manager.get_level_number(),
                score_breakdown
            )
        
        elif self.game_state == "GAME_OVER":
            self.ui.draw_game_over()
        
        elif self.game_state == "GAME_COMPLETE":
            self.ui.draw_game_complete(self.score_manager.total_score)
        
        pygame.display.flip()
    
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