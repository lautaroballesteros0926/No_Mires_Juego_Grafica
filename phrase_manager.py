import random
from config import PHRASES_BY_DIFFICULTY


class PhraseManager:
    def __init__(self):
        self.current_phrase = ""
        self.user_input = ""
        self.difficulty = 'easy'
        self.phrases_pool = []
        self._init_pool()
    
    def _init_pool(self):
        """Inicializa el pool de frases según la dificultad"""
        if self.difficulty in PHRASES_BY_DIFFICULTY:
            self.phrases_pool = PHRASES_BY_DIFFICULTY[self.difficulty].copy()
        else:
            self.phrases_pool = PHRASES_BY_DIFFICULTY['easy'].copy()
    
    def set_difficulty(self, difficulty):
        """
        Establece la dificultad y reinicia el pool
        
        Args:
            difficulty: 'easy', 'medium', o 'hard'
        """
        self.difficulty = difficulty
        self._init_pool()
    
    def get_random_phrase(self, difficulty=None):
        """
        Selecciona una frase aleatoria del pool
        
        Args:
            difficulty: Opcional, cambia la dificultad antes de seleccionar
        """
        if difficulty:
            self.set_difficulty(difficulty)
        
        if not self.phrases_pool:
            self._init_pool()
        
        self.current_phrase = random.choice(self.phrases_pool)
        self.phrases_pool.remove(self.current_phrase)
        self.user_input = ""
        return self.current_phrase
    
    def add_character(self, char):
        """
        Añade un carácter al input del usuario
        """
        self.user_input += char
    
    def remove_character(self):
        """
        Elimina el último carácter del input
        """
        if len(self.user_input) > 0:
            self.user_input = self.user_input[:-1]
    
    def check_phrase(self):
        """
        Verifica si la frase escrita coincide con la frase objetivo
        Retorna True si es correcta
        """
        return self.user_input == self.current_phrase
    
    def get_current_phrase(self):
        """
        Retorna la frase actual
        """
        return self.current_phrase
    
    def get_user_input(self):
        """
        Retorna el input actual del usuario
        """
        return self.user_input
    
    def get_character_comparison(self):
        """
        Compara carácter por carácter el input del usuario con la frase objetivo
        Retorna una lista de tuplas (carácter, es_correcto)
        """
        comparison = []
        for i, char in enumerate(self.user_input):
            if i < len(self.current_phrase):
                is_correct = char == self.current_phrase[i]
                comparison.append((char, is_correct))
            else:
                # Caracteres extra son incorrectos
                comparison.append((char, False))
        return comparison
    
    def get_accuracy(self):
        """
        Calcula la precisión actual (% de caracteres correctos)
        """
        if len(self.user_input) == 0:
            return 100
        
        correct = sum(1 for char, is_correct in self.get_character_comparison() if is_correct)
        return int((correct / len(self.user_input)) * 100)
    
    def is_character_correct(self, index):
        """
        Verifica si un carácter específico es correcto
        """
        if index < len(self.user_input) and index < len(self.current_phrase):
            return self.user_input[index] == self.current_phrase[index]
        return False
    
    def reset(self):
        """
        Reinicia el input del usuario
        """
        self.user_input = ""