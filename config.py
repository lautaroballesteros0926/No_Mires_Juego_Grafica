# config.py
"""
Configuración general del juego de mecanografía
"""

# Ventana
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)

# Jugador (cuadrado)
PLAYER_SIZE = 50
PLAYER_START_X = WINDOW_WIDTH // 2 - PLAYER_SIZE // 2
PLAYER_START_Y = WINDOW_HEIGHT // 2 - PLAYER_SIZE // 2

# Paredes
WALL_WIDTH = 50
WALL_SPEED = 2  # píxeles por frame cuando los ojos están abiertos
WALL_START_LEFT = 0
WALL_START_RIGHT = WINDOW_WIDTH - WALL_WIDTH

# Tiempo
TOLERANCE_TIME = 4  # segundos para memorizar la frase

# Webcam
WEBCAM_WIDTH = 320
WEBCAM_HEIGHT = 240
WEBCAM_X = 10
WEBCAM_Y = 10

# Mediapipe
EYE_ASPECT_RATIO_THRESHOLD = 0.2  # umbral para detectar ojos cerrados

# Fuentes
FONT_SIZE = 32
PHRASE_FONT_SIZE = 36
INPUT_FONT_SIZE = 32

# Frases de práctica
PHRASES = [
    "La práctica hace al maestro",
    "El tiempo es oro y vuela rápido",
    "Aprender a escribir sin mirar es útil",
    "La constancia es la clave del éxito",
    "Cada día es una nueva oportunidad",
    "La paciencia y la dedicación importan",
    "Programar es resolver problemas creativamente",
    "La tecnología avanza a pasos agigantados",
    "Mantén la calma y sigue adelante",
    "El conocimiento es poder infinito",
    "Respirar profundo ayuda a concentrarse",
    "Los desafíos nos hacen más fuertes",
    "La música inspira la creatividad humana",
    "Escribir correctamente requiere práctica diaria",
    "El éxito llega con perseverancia constante"
]