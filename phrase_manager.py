# phrase_manager.py
"""
Gestión de frases para el juego
"""

import random
from config import PHRASES


class PhraseManager:
    def __init__(self):
        self.current_phrase = ""
        self.user_input = ""
        self.phrases_pool = PHRASES.copy()
    
    def get_random_phrase(self):
        """
        Selecciona una frase aleatoria del pool
        """
        if not self.phrases_pool:
            self.phrases_pool = PHRASES.copy()
        
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
    
    def reset(self):
        """
        Reinicia el input del usuario
        """
        self.user_input = ""