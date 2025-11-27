import pygame
import cv2
import numpy as np
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, GREEN, RED, GRAY,
    CYAN, MAGENTA, YELLOW, PURPLE,
    WEBCAM_X, WEBCAM_Y, WEBCAM_WIDTH, WEBCAM_HEIGHT,
    FONT_SIZE, PHRASE_FONT_SIZE, INPUT_FONT_SIZE, TITLE_FONT_SIZE, HUD_FONT_SIZE
)
from effects import draw_glow_text


class UI:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        # Usar Consolas para mejor legibilidad (monospace)
        self.font = pygame.font.SysFont('consolas', FONT_SIZE, bold=False)
        self.phrase_font = pygame.font.SysFont('consolas', PHRASE_FONT_SIZE, bold=True)
        self.input_font = pygame.font.SysFont('consolas', INPUT_FONT_SIZE, bold=False)
        self.title_font = pygame.font.SysFont('consolas', TITLE_FONT_SIZE, bold=True)
        self.hud_font = pygame.font.SysFont('consolas', HUD_FONT_SIZE, bold=False)
    
    def draw_hud(self, level_number, score, combo, wpm):
        """
        Dibuja el HUD con informacion del juego - todo en la parte superior
        """
        # Nivel en esquina superior izquierda
        level_text = f"NIVEL {level_number}"
        draw_glow_text(self.screen, self.hud_font, level_text, (20, 20), WHITE, glow_size=1)
        
        # Score en la parte superior centro-izquierda
        score_text = f"SCORE: {score}"
        draw_glow_text(self.screen, self.hud_font, score_text, (250, 20), WHITE, glow_size=1)
        
        # WPM en la parte superior centro-derecha
        wpm_text = f"WPM: {wpm}"
        draw_glow_text(self.screen, self.hud_font, wpm_text, (500, 20), WHITE, glow_size=1)
        
        # Combo en la esquina superior derecha (solo si hay combo)
        if combo > 0:
            combo_text = f"COMBO x{combo}"
            draw_glow_text(self.screen, self.hud_font, combo_text, (WINDOW_WIDTH - 150, 20), WHITE, glow_size=1)
    
    def draw_phrase(self, phrase, show=True):
        """
        Dibuja la frase objetivo centrada verticalmente
        """
        if show:
            draw_glow_text(
                self.screen,
                self.phrase_font,
                f'{phrase}',
                (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3),
                WHITE,
                glow_size=1  # Reducido de 4 a 1
            )
    
    def draw_user_input_with_feedback(self, phrase_manager):
        """
        Dibuja el input del usuario con feedback visual caracter por caracter
        """
        comparison = phrase_manager.get_character_comparison()
        user_input = phrase_manager.get_user_input()
        
        if not user_input:
            # Mostrar placeholder
            draw_glow_text(
                self.screen,
                self.input_font,
                "Escribe aquí...",
                (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100),
                GRAY,
                glow_size=0  # Sin brillo
            )
            return
        
        # Calcular posición inicial para centrar el texto
        total_width = len(user_input) * 25  # Ajustado para Consolas
        start_x = (WINDOW_WIDTH - total_width) // 2
        y = WINDOW_HEIGHT - 100
        
        # Dibujar cada carácter con su color (blanco correcto, gris incorrecto)
        x_offset = start_x
        for char, is_correct in comparison:
            color = WHITE if is_correct else GRAY
            char_surface = self.input_font.render(char, True, color)
            char_rect = char_surface.get_rect(center=(x_offset, y))
            
            # Efecto de brillo reducido (solo 1 capa suave)
            if is_correct:
                glow_surf = self.input_font.render(char, True, color)
                glow_rect = glow_surf.get_rect(center=(x_offset, y))
                # Brillo muy sutil
                # self.screen.blit(glow_surf, (glow_rect.x - 1, glow_rect.y))
                # self.screen.blit(glow_surf, (glow_rect.x + 1, glow_rect.y))
            
            self.screen.blit(char_surface, char_rect)
            x_offset += char_rect.width + 2
    
    def draw_countdown(self, time_left):
        """
        Dibuja la cuenta regresiva durante el tiempo de tolerancia
        """
        seconds = int(time_left)
        color = WHITE
        
        # Número más abajo y con menos brillo
        draw_glow_text(
            self.screen,
            self.title_font,
            f'{seconds}',
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2),  # Bajado 100px
            color,
            glow_size=2  # Reducido de 8 a 2
        )
        
        # Texto más abajo y con menos brillo
        draw_glow_text(
            self.screen,
            self.phrase_font,
            '¡Memoriza la frase!',
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80),  # Bajado 80px
            WHITE,
            glow_size=1  # Reducido de 4 a 1
        )
    
    def draw_game_over(self):
        """
        Dibuja la pantalla de Game Over
        """
        draw_glow_text(
            self.screen,
            self.title_font,
            '¡PERDISTE!',
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50),
            WHITE,
            glow_size=2  # Reducido de 10 a 2
        )
        draw_glow_text(
            self.screen,
            self.font,
            'Presiona ESPACIO para reintentar',
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50),
            GRAY,
            glow_size=1  # Reducido de 3 a 1
        )
    
    def draw_victory(self):
        """
        Dibuja la pantalla de victoria
        """
        draw_glow_text(
            self.screen,
            self.title_font,
            '¡CORRECTO!',
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50),
            WHITE,
            glow_size=2  # Reducido de 10 a 2
        )
        draw_glow_text(
            self.screen,
            self.font,
            'Presiona ESPACIO para continuar',
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50),
            GRAY,
            glow_size=1  # Reducido de 3 a 1
        )
    
    def draw_level_complete(self, level_number, score_breakdown):
        """
        Dibuja la pantalla de nivel completado con desglose de puntuación
        """
        draw_glow_text(
            self.screen,
            self.title_font,
            f'NIVEL {level_number} COMPLETADO',
            (WINDOW_WIDTH // 2, 150),
            WHITE,
            glow_size=8
        )
        
        # Desglose de puntuación
        y_offset = 250
        line_height = 100
        
        stats = [
            (f"WPM: {score_breakdown['wpm']}", WHITE),
            (f"Precision: {score_breakdown['accuracy']}%", WHITE),
            (f"Combo Maximo: {score_breakdown['combo']}", WHITE),
            (f"Tiempo Ojos Cerrados: {score_breakdown['eyes_closed_time']}s", WHITE),
            (f"Puntos del Nivel: {score_breakdown['level_score']}", WHITE),
            (f"Puntuación Total: {score_breakdown['total_score']}", WHITE),
        ]
        
        for text, color in stats:
            draw_glow_text(
                self.screen,
                self.phrase_font,
                text,
                (WINDOW_WIDTH // 2, y_offset),
                color,
                glow_size=3
            )
            y_offset += line_height
        
        # Instrucción
        draw_glow_text(
            self.screen,
            self.font,
            'Presiona ESPACIO para continuar',
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100),
            GRAY,
            glow_size=3
        )
    
    def draw_game_complete(self, total_score):
        """
        Dibuja la pantalla de juego completado (todos los niveles)
        """
        draw_glow_text(
            self.screen,
            self.title_font,
            '¡JUEGO COMPLETADO!',
            (WINDOW_WIDTH // 2, 200),
            WHITE,
            glow_size=10
        )
        
        draw_glow_text(
            self.screen,
            self.phrase_font,
            f'Puntuación Final: {total_score}',
            (WINDOW_WIDTH // 2, 300),
            WHITE,
            glow_size=5
        )
        
        draw_glow_text(
            self.screen,
            self.font,
            'Presiona ESPACIO para jugar de nuevo',
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100),
            GRAY,
            glow_size=3
        )
    
    def draw_webcam_feed(self, frame):
        """
        Dibuja el feed de la webcam en la esquina superior izquierda
        """
        if frame is not None:
            try:
                # Convertir de BGR (OpenCV) a RGB (Pygame)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Redimensionar si es necesario
                frame_resized = cv2.resize(frame_rgb, (WEBCAM_WIDTH, WEBCAM_HEIGHT))
                
                # Rotar para Pygame (OpenCV usa (height, width, channels))
                frame_rotated = np.rot90(frame_resized)
                frame_surface = pygame.surfarray.make_surface(frame_rotated)
                
                # Dibujar en la esquina superior izquierda
                self.screen.blit(frame_surface, (WEBCAM_X, WEBCAM_Y))
                
                # Dibujar solo el borde blanco
                border_rect = pygame.Rect(WEBCAM_X, WEBCAM_Y, WEBCAM_WIDTH, WEBCAM_HEIGHT)
                pygame.draw.rect(self.screen, WHITE, border_rect, 3)
            except Exception as e:
                # Si hay error, simplemente no mostrar la webcam
                pass
    
    def draw_danger_indicator(self, danger_level):
        """
        Dibuja un indicador de peligro pulsante cuando las paredes estan cerca
        """
        if danger_level > 0.5:
            # Efecto de pulso
            import math
            pulse = abs(math.sin(pygame.time.get_ticks() / 100))
            alpha = int(150 * pulse * danger_level)
            
            # Crear overlay blanco
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, alpha))
            self.screen.blit(overlay, (0, 0))
            
            # Texto de advertencia
            if danger_level > 0.7:
                draw_glow_text(
                    self.screen,
                    self.title_font,
                    '¡PELIGRO!',
                    (WINDOW_WIDTH // 2, 50),
                    WHITE,
                    glow_size=8
                )
    
    def draw_instructions(self):
        """
        Dibuja las instrucciones durante la fase de memorizacion
        """
        draw_glow_text(
            self.screen,
            self.font,
            '¡Memoriza la frase sin mirar el teclado!',
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50),
            GRAY,
            glow_size=2
        )
    
    def draw_loading(self, progress=0):
        """
        Dibuja pantalla de carga con instrucciones mientras se inicializa el juego
        """
        # Título de carga
        draw_glow_text(
            self.screen,
            self.title_font,
            'CARGANDO...',
            (WINDOW_WIDTH // 2, 100),
            WHITE,
            glow_size=2
        )
        
        # Barra de progreso
        bar_width = 400
        bar_height = 30
        bar_x = (WINDOW_WIDTH - bar_width) // 2
        bar_y = 160
        
        # Fondo de la barra
        pygame.draw.rect(self.screen, GRAY, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Progreso
        if progress > 0:
            fill_width = int(bar_width * (progress / 100))
            pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, fill_width, bar_height))
        
        # Instrucciones mientras carga
        instructions = [
            "INSTRUCCIONES:",
            "",
            "1. Memoriza la frase que aparece",
            "",
            "2. Cierra los ojos para escribir",
            "",
            "3. Las paredes se mueven lento con ojos cerrados",
            "",
            "4. Completa la frase correctamente para avanzar",
        ]
        
        y_offset = 250
        for i, instruction in enumerate(instructions):
            if i == 0:
                color = WHITE
                font = self.phrase_font
                glow = 1  # Reducido de 4 a 1 para mejor legibilidad
            else:
                color = GRAY
                font = self.font
                glow = 0  # Reducido de 2 a 0 para texto limpio
            
            draw_glow_text(
                self.screen,
                font,
                instruction,
                (WINDOW_WIDTH // 2, y_offset),
                color,
                glow_size=glow
            )
            y_offset += 45  # Espaciado aumentado
    
    def draw_menu(self):
        """
        Dibuja la pantalla de inicio - solo instrucciones
        """
        # Solo instrucciones centradas
        instructions = [
            "INSTRUCCIONES:",
            "",
            "1. Memoriza la frase que aparece",
            "",
            "2. Cierra los ojos para escribir",
            "",
            "3. Las paredes se mueven lento con ojos cerrados",
            "",
            "4. Completa la frase correctamente para avanzar",
            "",
            "",
            "Presiona ESPACIO para comenzar",
        ]
        
        # Centrar verticalmente
        total_height = len(instructions) * 40
        start_y = (WINDOW_HEIGHT - total_height) // 2
        
        for i, instruction in enumerate(instructions):
            # Título en blanco, instrucciones en gris, mensaje final en blanco
            if i == 0 or i == len(instructions) - 1:
                color = WHITE
                font = self.phrase_font
                glow = 5
            else:
                color = GRAY
                font = self.font
                glow = 2
            
            draw_glow_text(
                self.screen,
                font,
                instruction,
                (WINDOW_WIDTH // 2, start_y + i * 40),
                color,
                glow_size=glow
            )
