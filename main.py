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
from floor import Floor


class Game:
    def __init__(self):
        # Inicializar Pygame primero
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("No Mires - Typing Game")
        self.clock = pygame.time.Clock()
        
        # Crear UI temporal para mostrar pantalla de carga
        self.ui = UI(self.screen)
        
        # Mostrar pantalla de carga inicial
        self.screen.fill((0, 0, 0))
        self.ui.draw_loading(0)
        pygame.display.flip()
        
        # Cargar componentes con progreso
        # Cámara (30%)
        self.camera = Camera()
        self.screen.fill((0, 0, 0))
        self.ui.draw_loading(30)
        pygame.display.flip()
        
        # Jugador con sprites (50%)
        self.player = Player()
        self.screen.fill((0, 0, 0))
        self.ui.draw_loading(50)
        pygame.display.flip()
        
        # Paredes y suelo (70%)
        self.walls = WallManager()
        self.floor = Floor()
        self.screen.fill((0, 0, 0))
        self.ui.draw_loading(70)
        pygame.display.flip()
        
        # Managers (85%)
        self.phrase_manager = PhraseManager()
        self.level_manager = LevelManager()
        self.score_manager = ScoreManager()
        self.screen.fill((0, 0, 0))
        self.ui.draw_loading(85)
        pygame.display.flip()
        
        # Efectos (100%)
        self.particle_system = ParticleSystem()
        self.screen_shake = ScreenShake()
        self.color_manager = ColorManager()
        self.screen.fill((0, 0, 0))
        self.ui.draw_loading(100)
        pygame.display.flip()
        
        # Esperar un momento para que se vea el 100%
        pygame.time.wait(500)
        
        # Estados del juego
        self.game_state = "MENU"  # Iniciar en pantalla de inicio
        self.tolerance_timer = TOLERANCE_TIME
        self.start_ticks = pygame.time.get_ticks()
        self.wall_stop_timer = 0
        self.current_wall_speed = 0
        
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
            # Configurar velocidad de paredes según el nivel
            self.current_wall_speed = current_level.wall_speed
            self.walls.set_speed(self.current_wall_speed)
            
            
            # Configurar tiempo de tolerancia
            self.tolerance_timer = current_level.tolerance_time
            
            # Obtener nueva frase
            difficulty = current_level.phrase_difficulty
            # CORREGIDO: usar get_random_phrase y eliminar set_phrase
            self.current_phrase = self.phrase_manager.get_random_phrase(difficulty)
            
            # Resetear timer
            self.start_ticks = pygame.time.get_ticks()
            self.game_state = "MEMORIZING"
        else:
            self.game_state = "GAME_COMPLETE"

    def handle_events(self):
        """
        Maneja los eventos de entrada
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.camera.cap.release()
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.camera.cap.release()
                    pygame.quit()
                    sys.exit()
                
                # Pantalla de inicio
                if self.game_state == "MENU":
                    if event.key == pygame.K_SPACE:
                        self.start_new_level()
                
                # Reiniciar juego si terminó
                if self.game_state in ["GAME_OVER", "GAME_COMPLETE"]:
                    if event.key == pygame.K_SPACE:
                        self.level_manager.reset()
                        self.score_manager.reset_game()
                        self.start_new_level()
                
                # Continuar al siguiente nivel
                elif self.game_state == "LEVEL_COMPLETE":
                    if event.key == pygame.K_SPACE:
                        if self.level_manager.next_level():
                            self.start_new_level()
                        else:
                            self.game_state = "GAME_COMPLETE"
                
                # Input de escritura
                elif self.game_state == "PLAYING":
                    # Si los ojos están cerrados, detener movimiento de paredes temporalmente
                    # (esto ya se maneja en update, pero aquí manejamos el input)
                    
                    if event.key == pygame.K_BACKSPACE:
                        # Borrar ultimo carácter
                        self.phrase_manager.remove_character()
                    
                    else:
                        # Añadir caracter si es valido
                        if event.unicode.isprintable():
                            # Verificar si el caracter es correcto
                            current_input = self.phrase_manager.get_user_input()
                            expected_char = self.current_phrase[len(current_input)] if len(current_input) < len(self.current_phrase) else None
                            
                            self.phrase_manager.add_character(event.unicode)
                            
                            # Actualizar estadísticas
                            is_correct = (event.unicode == expected_char)
                            if is_correct:
                                self.score_manager.add_correct_character()
                            else:
                                self.score_manager.add_incorrect_character()
                                # Aumentar velocidad ligeramente por error
                                self.current_wall_speed += 0.3
                                self.walls.set_speed(self.current_wall_speed)
                            
                            # Verificar si completó la frase
                            if self.phrase_manager.check_phrase():
                                # Frase correcta: detener paredes por 2 segundos
                                self.wall_stop_timer = 2000  # WALL_STOP_DURATION
                                self.walls.stop_moving()
                            
                                self.score_manager.complete_level(self.level_manager.current_level)
                                self.game_state = "LEVEL_COMPLETE"
    
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
            # Cuenta regresiva
            current_time = pygame.time.get_ticks()
            elapsed = (current_time - self.start_ticks) / 1000
            self.tolerance_timer = max(0, TOLERANCE_TIME - elapsed)
            
            if self.tolerance_timer <= 0:
                self.game_state = "PLAYING"
                self.score_manager.start_typing()
        
        elif self.game_state == "PLAYING":
            # Actualizar timer de parada de paredes (después de completar frase)
            if self.wall_stop_timer > 0:
                self.wall_stop_timer -= 1000 / 60  # Restar ms por frame (asumiendo 60 FPS)
                self.walls.stop_moving()
            else:
                # Lógica de movimiento según ojos
                if eyes_open:
                    # Ojos abiertos: velocidad normal (o penalizada por errores)
                    self.walls.set_speed(self.current_wall_speed)
                    self.walls.start_moving()
                else:
                    # Ojos cerrados: velocidad MÍNIMA (muy lenta)
                    self.walls.set_speed(0.5)  # WALL_SPEED_MINIMAL
                    self.walls.start_moving()
            
            self.walls.update()
            
            # Verificar colisión
            if self.walls.check_collision(self.player):
                self.game_state = "GAME_OVER"
            
            # Actualizar nivel de peligro del jugador
            self.player.update_danger_level(self.walls.get_walls())
            
            # Actualizar color manager segun peligro
            self.color_manager.set_danger_level(self.player.danger_level)
            
            # Screen shake si hay mucho peligro
            if self.player.danger_level > 0.7 and eyes_open:
                self.screen_shake.start(intensity=5, duration=5)
        
        
        # Actualizar animación del jugador
        is_typing = len(self.phrase_manager.get_user_input()) > 0
        self.player.update_animation(self.game_state, is_typing)
        # Actualizar sistemas visuales
        self.particle_system.update()
        self.screen_shake.update()
        # self.color_manager.update()  # ELIMINADO: No existe este método
    
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
        
        # Dibujar suelo (antes que todo lo demás)
        self.floor.draw(game_surface)
        
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
        
        if self.game_state == "MENU":
            # Pantalla de inicio
            self.ui.draw_menu()
        
        elif self.game_state == "MEMORIZING":
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