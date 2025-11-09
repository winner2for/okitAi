"""
Gestion vocale adaptée pour Android/Kivy
"""
import threading
import time
import logging

logger = logging.getLogger(__name__)

class VoiceHandlerAndroid:
    def __init__(self):
        self.is_listening = False
        self.callback = None
        logger.info("VoiceHandler: Initialisé pour Android")
    
    def start_listening(self, callback):
        """Démarrer la reconnaissance vocale"""
        self.callback = callback
        self.is_listening = True
        
        def listen_thread():
            logger.info("VoiceHandler: Écoute démarrée")
            # Simulation - Dans une vraie app, utiliser SpeechRecognition
            # avec les permissions Android appropriées
            time.sleep(2)
            if self.is_listening and self.callback:
                self.callback("Bonjour ! Ceci est une démonstration de la reconnaissance vocale sur Okit AI.")
        
        threading.Thread(target=listen_thread, daemon=True).start()
    
    def stop_listening(self):
        """Arrêter l'écoute"""
        self.is_listening = False
        logger.info("VoiceHandler: Écoute arrêtée")
    
    def speak(self, text):
        """Synthèse vocale"""
        logger.info(f"VoiceHandler: Lecture: {text[:100]}...")
        # À implémenter avec TTS Android
        # from jnius import autoclass
        # TextToSpeech = autoclass('android.speech.tts.TextToSpeech')

# Instance globale pour faciliter l'utilisation
voice_handler = VoiceHandlerAndroid()