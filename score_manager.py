import time
import json
import os


class ScoreManager:
    def __init__(self):
        self.total_score = 0
        self.level_score = 0
        self.combo = 0
        self.max_combo = 0
        self.correct_chars = 0
        self.total_chars = 0
        self.typing_start_time = None
        self.eyes_closed_time = 0
        self.eyes_closed_start = None
        self.high_scores_file = "high_scores.json"
    
    def start_typing(self):
        """
        Inicia el contador de tiempo para calcular WPM
        """
        self.typing_start_time = time.time()
    
    def add_correct_character(self):
        """
        Registra un caracter correcto 
        """
        self.correct_chars += 1
        self.total_chars += 1
        self.combo += 1
        if self.combo > self.max_combo:
            self.max_combo = self.combo
    
    def add_incorrect_character(self):
        """
        Registra un carácter incorrecto 
        """
        self.total_chars += 1
        self.combo = 0
    
    def start_eyes_closed(self):
        """
        Inicia el contador de tiempo con ojos cerrados
        """
        if self.eyes_closed_start is None:
            self.eyes_closed_start = time.time()
    
    def stop_eyes_closed(self):
        """
        Detiene el contador de tiempo con ojos cerrados
        """
        if self.eyes_closed_start is not None:
            self.eyes_closed_time += time.time() - self.eyes_closed_start
            self.eyes_closed_start = None
    
    def calculate_wpm(self):
        """
        Calcula palabras por minuto 
        """
        if self.typing_start_time is None:
            return 0
        
        elapsed_time = time.time() - self.typing_start_time
        if elapsed_time == 0:
            return 0
        
        words = self.correct_chars / 5.0
        minutes = elapsed_time / 60.0
        return int(words / minutes) if minutes > 0 else 0
    
    def calculate_accuracy(self):
        """
        Calcula el porcentaje de precision
        """
        if self.total_chars == 0:
            return 100
        return int((self.correct_chars / self.total_chars) * 100)
    
    def calculate_level_score(self, level_number):
        """
        Calcula la puntuacion del nivel actual
        
        Componentes:
        - WPM bonus: 10 puntos por cada WPM
        - Accuracy bonus: 5 puntos por cada % de precision
        - Combo bonus: 2 puntos por cada combo maximo
        - Eyes closed bonus: 50 puntos por cada segundo con ojos cerrados
        - Level multiplier: x nivel
        """
        wpm = self.calculate_wpm()
        accuracy = self.calculate_accuracy()
        
        wpm_bonus = wpm * 10
        accuracy_bonus = accuracy * 5
        combo_bonus = self.max_combo * 2
        eyes_bonus = int(self.eyes_closed_time * 50)
        
        base_score = wpm_bonus + accuracy_bonus + combo_bonus + eyes_bonus
        self.level_score = base_score * level_number
        
        return self.level_score
    
    def complete_level(self, level_number):
        """
        Completa un nivel y añade la puntuacion al total
        """
        score = self.calculate_level_score(level_number)
        self.total_score += score
        return score
    
    def reset_level(self):
        """
        Reinicia las estadisticas del nivel actual
        """
        self.level_score = 0
        self.combo = 0
        self.max_combo = 0
        self.correct_chars = 0
        self.total_chars = 0
        self.typing_start_time = None
        self.eyes_closed_time = 0
        self.eyes_closed_start = None
    
    def reset_game(self):
        """
        Reinicia todas las estadisticas
        """
        self.total_score = 0
        self.reset_level()
    
    def save_high_score(self, player_name="Player"):
        """
        Guarda el puntaje alto en un archivo JSON
        """
        high_scores = self.load_high_scores()
        
        new_score = {
            "name": player_name,
            "score": self.total_score,
            "wpm": self.calculate_wpm(),
            "accuracy": self.calculate_accuracy(),
            "max_combo": self.max_combo
        }
        
        high_scores.append(new_score)
        high_scores.sort(key=lambda x: x["score"], reverse=True)
        high_scores = high_scores[:10]  # Mantener solo top 10
        
        with open(self.high_scores_file, 'w') as f:
            json.dump(high_scores, f, indent=2)
    
    def load_high_scores(self):
        """
        Carga los puntajes altos desde el archivo
        """
        if os.path.exists(self.high_scores_file):
            try:
                with open(self.high_scores_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def get_score_breakdown(self):
        """
        Retorna un desglose detallado de la puntuacion
        """
        return {
            "wpm": self.calculate_wpm(),
            "accuracy": self.calculate_accuracy(),
            "combo": self.max_combo,
            "eyes_closed_time": round(self.eyes_closed_time, 1),
            "level_score": self.level_score,
            "total_score": self.total_score
        }
