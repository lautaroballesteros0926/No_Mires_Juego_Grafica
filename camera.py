import mediapipe as mp
import cv2  
import numpy as np
from config import WEBCAM_WIDTH, WEBCAM_HEIGHT, EYE_ASPECT_RATIO_THRESHOLD


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WEBCAM_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WEBCAM_HEIGHT)
        
        # Inicializar Mediapipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.eyes_open = False
        self.frame = None
        
        # Índices de landmarks para los ojos 
        # Ojo izquierdo: [362, 385, 387, 263, 373, 380]
        # Ojo derecho: [33, 160, 158, 133, 153, 144]
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
    
    def calculate_eye_aspect_ratio(self, eye_landmarks):
        """
        Calcula el Eye Aspect Ratio  para determinar si el ojo esta abierto
        """
        # Calcular distancias verticales
        A = np.linalg.norm(eye_landmarks[1] - eye_landmarks[5])
        B = np.linalg.norm(eye_landmarks[2] - eye_landmarks[4])
        
        # Calcular distancia horizontal
        C = np.linalg.norm(eye_landmarks[0] - eye_landmarks[3])
        
        # EAR
        ear = (A + B) / (2.0 * C)
        return ear
    
    def detect_eyes(self):
        """
        Detecta si los ojos estan abiertos o cerrados
        Retorna True si los ojos estan abiertos
        """
        ret, frame = self.cap.read()
        if not ret:
            return self.eyes_open
        
        # Voltear horizontalmente para efecto espejo
        frame = cv2.flip(frame, 1)
        self.frame = frame.copy()
        
        # Convertir a RGB para Mediapipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            
            # Obtener dimensiones de la imagen
            h, w = frame.shape[:2]
            
            # Extraer coordenadas de los ojos
            left_eye_coords = []
            right_eye_coords = []
            
            for idx in self.LEFT_EYE:
                landmark = face_landmarks.landmark[idx]
                left_eye_coords.append([landmark.x * w, landmark.y * h])
            
            for idx in self.RIGHT_EYE:
                landmark = face_landmarks.landmark[idx]
                right_eye_coords.append([landmark.x * w, landmark.y * h])
            
            left_eye_coords = np.array(left_eye_coords)
            right_eye_coords = np.array(right_eye_coords)
            
            # Calcular EAR para ambos ojos
            left_ear = self.calculate_eye_aspect_ratio(left_eye_coords)
            right_ear = self.calculate_eye_aspect_ratio(right_eye_coords)
            
            # Promedio de ambos ojos
            avg_ear = (left_ear + right_ear) / 2.0
            
            # Determinar si los ojos estan abiertos
            self.eyes_open = avg_ear > EYE_ASPECT_RATIO_THRESHOLD
            
            # Dibujar indicador visual en el frame
            color = (0, 0, 255) if self.eyes_open else (0, 255, 0)
            status = "ABIERTOS" if self.eyes_open else "CERRADOS"
            cv2.putText(frame, status, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            self.frame = frame
        
        return self.eyes_open
    
    def get_frame(self):
        """
        Retorna el frame actual de la cámara para mostrar en Pygame
        """
        return self.frame
    
    def release(self):
        """
        Libera los recursos de la cámara
        """
        self.cap.release()
        self.face_mesh.close()