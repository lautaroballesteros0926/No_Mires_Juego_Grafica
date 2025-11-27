class Level:
    def __init__(self, number, wall_speed, tolerance_time, phrase_difficulty):
        """
        Representa un nivel del juego
        """
        self.number = number
        self.wall_speed = wall_speed
        self.tolerance_time = tolerance_time
        self.phrase_difficulty = phrase_difficulty


class LevelManager:
    def __init__(self):
        self.current_level = 0
        self.total_levels = 5
        
        # Definir los 5 niveles con dificultad progresiva
        self.levels = [
            Level(1, 1.5, 5.0, 'easy'),      # Nivel 1: Facil
            Level(2, 2.0, 4.0, 'medium'),    # Nivel 2: Medio
            Level(3, 2.5, 3.5, 'medium'),    # Nivel 3: Medio
            Level(4, 3.0, 3.0, 'hard'),      # Nivel 4: Dificil
            Level(5, 3.5, 2.5, 'hard'),      # Nivel 5: Muy Dificil
        ]
    
    def start_level(self, level_number):
        """
        Inicia un nivel especifico
        """
        if 1 <= level_number <= self.total_levels:
            self.current_level = level_number - 1
            return self.get_current_level()
        return None
    
    def next_level(self):
        """
        Avanza al siguiente nivel
        Retorna True si hay mas niveles, False si se completaron todos
        """
        if self.current_level < self.total_levels - 1:
            self.current_level += 1
            return True
        return False
    
    def get_current_level(self):
        """
        Retorna el nivel actual
        """
        if 0 <= self.current_level < self.total_levels:
            return self.levels[self.current_level]
        return None
    
    def is_final_level(self):
        """
        Verifica si es el ultimo nivel
        """
        return self.current_level == self.total_levels - 1
    
    def get_level_number(self):
        """
        Retorna el numero del nivel actual (1-indexed)
        """
        return self.current_level + 1
    
    def reset(self):
        """
        Reinicia al primer nivel
        """
        self.current_level = 0
