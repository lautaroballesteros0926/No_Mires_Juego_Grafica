# ui.py
"""
Gestión de la interfaz de usuario y renderizado de texto
"""

import pygame
import cv2
import numpy as np
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, GREEN, RED, GRAY,
    FONT_SIZE, PHRASE_FONT_SIZE, INPUT_FONT_SIZE,
    WEBCAM_X, WEBCAM_Y, WEBCAM_WIDTH, WEBCAM_HEIGHT
)


class UI:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.phrase_font = pygame.font.Font(None, PHRASE_FONT_SIZE)
        self.input_font = pygame.font.Font(None, INPUT_FONT_SIZE)
    
    def draw_text(self, text, x, y, color=WHITE, font=None):
        """
        Dibuja texto en la pantalla
        """
        if font is None:
            font = self.font
        
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
    
    def draw_phrase(self, phrase, show=True):
        """
        Dibuja la frase objetivo en la parte superior
        """
        if show:
            self.draw_text(
                f'Frase: "{phrase}"',
                WINDOW_WIDTH // 2,
                80,
                WHITE,
                self.phrase_font
            )
    
    def draw_user_input(self, user_input):
        """
        Dibuja el input del usuario en el centro-inferior
        """
        self.draw_text(
            f'Tu texto: {user_input}',
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT - 100,
            GREEN,
            self.input_font
        )
    
    def draw_countdown(self, time_left):
        """
        Dibuja la cuenta regresiva durante el tiempo de tolerancia
        """
        self.draw_text(
            f'Memoriza la frase: {int(time_left)}s',
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2 - 100,
            WHITE,
            self.phrase_font
        )
    
    def draw_game_over(self):
        """
        Dibuja la pantalla de Game Over
        """
        self.draw_text(
            '¡PERDISTE!',
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2 - 50,
            RED,
            self.phrase_font
        )
        self.draw_text(
            'Presiona ESPACIO para reintentar',
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2 + 20,
            WHITE,
            self.font
        )
    
    def draw_victory(self):
        """
        Dibuja la pantalla de victoria
        """
        self.draw_text(
            '¡CORRECTO!',
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2 - 50,
            GREEN,
            self.phrase_font
        )
        self.draw_text(
            'Presiona ESPACIO para continuar',
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2 + 20,
            WHITE,
            self.font
        )
    
    def draw_webcam_feed(self, frame):
        """
        Dibuja el feed de la webcam en la esquina superior izquierda
        """
        if frame is not None:
            # Convertir de BGR (OpenCV) a RGB (Pygame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Redimensionar si es necesario
            frame = cv2.resize(frame, (WEBCAM_WIDTH, WEBCAM_HEIGHT))
            
            # Rotar para Pygame (OpenCV usa (height, width, channels))
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            
            # Dibujar en la esquina superior izquierda
            self.screen.blit(frame, (WEBCAM_X, WEBCAM_Y))
            
            # Dibujar borde alrededor de la webcam
            pygame.draw.rect(
                self.screen,
                WHITE,
                (WEBCAM_X, WEBCAM_Y, WEBCAM_WIDTH, WEBCAM_HEIGHT),
                2
            )
    
    def draw_instructions(self):
        """
        Dibuja las instrucciones durante la fase de memorización
        """
        self.draw_text(
            '¡Memoriza la frase sin mirar el teclado!',
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2 + 50,
            GRAY,
            self.font
        )