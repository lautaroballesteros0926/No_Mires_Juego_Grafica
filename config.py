# Ventana
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60

# Colores básicos
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)

# Colores Neon/Cyberpunk (aunque usamos B/N, algunos sistemas pueden requerirlos para evitar errores de importación)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 255)
DARK_BLUE = (10, 10, 30)
DANGER_RED = (80, 10, 10)

# Webcam
WEBCAM_WIDTH = 320
WEBCAM_HEIGHT = 240
WEBCAM_X = 700
WEBCAM_Y = 10

# Mediapipe
EYE_ASPECT_RATIO_THRESHOLD = 0.2  # umbral para detectar ojos cerrados

# Suelo
FLOOR_HEIGHT = 16
GROUND_Y = WINDOW_HEIGHT - FLOOR_HEIGHT

# Jugador
PLAYER_SIZE = 80  # Aumentado para mejor visibilidad
PLAYER_START_X = WINDOW_WIDTH // 2 - 40  # Centrado (PLAYER_SIZE/2)
PLAYER_START_Y = GROUND_Y - PLAYER_SIZE

# Paredes
WALL_WIDTH = 30  # Reducido de 50 a 30 para paredes más delgadas
WALL_HEIGHT = 450 # Altura de las paredes
WALL_SPEED = 2  # píxeles por frame cuando los ojos están abiertos (base, se ajusta por nivel)
WALL_START_LEFT = 0
WALL_START_RIGHT = WINDOW_WIDTH - WALL_WIDTH

# Tiempo
TOLERANCE_TIME = 4  # segundos para memorizar la frase (base, se ajusta por nivel)

# Fuentes
FONT_SIZE = 32
PHRASE_FONT_SIZE = 36
INPUT_FONT_SIZE = 32
TITLE_FONT_SIZE = 64
HUD_FONT_SIZE = 24

# Efectos visuales
PARTICLE_COUNT = 3  # partículas por frame cuando las paredes se mueven
SCREEN_SHAKE_INTENSITY = 8
SCREEN_SHAKE_DURATION = 10
GLOW_SIZE = 5

# Frases por dificultad
PHRASES_EASY = [
    "Hola mundo",
    "Buenos dias",
    "La práctica hace al maestro",
    "Cada día es una nueva oportunidad",
    "Mantén la calma y sigue adelante",
]

PHRASES_MEDIUM = [
    "El tiempo es oro y vuela rápido",
    "Aprender a escribir sin mirar es útil",
    "La constancia es la clave del éxito",
    "La paciencia y la dedicación importan",
    "El conocimiento es poder infinito",
    "Respirar profundo ayuda a concentrarse",
    "Los desafíos nos hacen más fuertes",
    "La música inspira la creatividad humana",
]

PHRASES_HARD = [
    "Programar es resolver problemas creativamente",
    "La tecnología avanza a pasos agigantados",
    "Escribir correctamente requiere práctica diaria",
    "El éxito llega con perseverancia constante",
    "La determinación supera cualquier obstáculo difícil",
    "El aprendizaje continuo es fundamental para crecer",
    "La innovación surge de la curiosidad y experimentación",
    "Dominar una habilidad requiere tiempo y dedicación absoluta",
]

# Diccionario de frases por dificultad
PHRASES_BY_DIFFICULTY = {
    'easy': PHRASES_EASY,
    'medium': PHRASES_MEDIUM,
    'hard': PHRASES_HARD
}