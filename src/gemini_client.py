import google.generativeai as genai
import os
import logging
from typing import Optional
import requests
import json
import time

# Import de la configuration
from .config import AppConfig

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self, api_key: Optional[str] = None):
        """Initialise le client Gemini avec Gemini 2.0 Flash"""
        # Configuration automatique
        AppConfig.setup()
        
        # Priorité: paramètre > environnement > config intégrée
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "Clé API Gemini non trouvée. "
                "Le build GitHub doit inclure la clé API."
            )
        
        try:
            genai.configure(api_key=self.api_key)
            
            # Utilisation de Gemini 2.0 Flash
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            
            # URL pour l'API REST (fallback)
            self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
            
            logger.info("✅ Client Gemini 2.0 Flash initialisé")
            
        except Exception as e:
            logger.error(f"❌ Erreur initialisation Gemini: {e}")
            raise
    
    def generate_text(self, prompt: str, image_path: Optional[str] = None) -> str:
        """
        Génère du texte avec Gemini 2.0 Flash
        """
        try:
            start_time = time.time()
            
            if image_path and os.path.exists(image_path):
                logger.info(f"🖼️  Analyse d'image: {image_path}")
                response = self._generate_with_image(prompt, image_path)
            else:
                logger.info(f"💬 Prompt: {prompt[:80]}...")
                response = self._generate_text_only(prompt)
            
            response_time = time.time() - start_time
            logger.info(f"⏱️  Réponse reçue en {response_time:.2f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Erreur génération: {e}")
            # Fallback vers l'API REST
            try:
                return self._generate_via_rest_api(prompt)
            except Exception as rest_error:
                return f"❌ Erreur: {str(rest_error)}"
    
    def _generate_text_only(self, prompt: str) -> str:
        """Génération via SDK Google"""
        try:
            response = self.model.generate_content(prompt)
            return self._process_response(response)
        except Exception as e:
            raise Exception(f"Erreur SDK: {str(e)}")
    
    def _generate_with_image(self, prompt: str, image_path: str) -> str:
        """Génération avec image"""
        try:
            import PIL.Image
            
            img = PIL.Image.open(image_path)
            response = self.model.generate_content([prompt, img])
            return self._process_response(response)
            
        except Exception as e:
            raise Exception(f"Erreur analyse image: {str(e)}")
    
    def _generate_via_rest_api(self, prompt: str) -> str:
        """Génération via API REST directe"""
        try:
            headers = {
                'Content-Type': 'application/json',
                'x-goog-api-key': self.api_key
            }
            
            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024,
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                error_msg = f"API Error {response.status_code}"
                logger.error(f"{error_msg}: {response.text}")
                raise Exception(error_msg)
                
        except Exception as e:
            raise Exception(f"Erreur API REST: {str(e)}")
    
    def _process_response(self, response) -> str:
        """Traite la réponse de l'API"""
        try:
            if hasattr(response, 'text'):
                return response.text
            elif hasattr(response, 'parts'):
                return ''.join(part.text for part in response.parts if hasattr(part, 'text'))
            elif hasattr(response, 'candidates'):
                return response.candidates[0]['content']['parts'][0]['text']
            else:
                return "Réponse inattendue de l'API Gemini."
        except Exception as e:
            logger.error(f"Erreur traitement réponse: {e}")
            return f"Erreur traitement: {str(e)}"
    
    def start_chat(self):
        """Démarrer une session de chat"""
        self.chat = self.model.start_chat(history=[])
        logger.info("💬 Session de chat démarrée")
    
    def send_message(self, message: str) -> str:
        """Envoyer un message dans le chat"""
        if not hasattr(self, 'chat'):
            self.start_chat()
        
        try:
            response = self.chat.send_message(message)
            return self._process_response(response)
        except Exception as e:
            return f"Erreur chat: {str(e)}"
    
    def check_api_status(self) -> bool:
        """Vérifier si l'API fonctionne"""
        try:
            test_response = self.generate_text("Réponds juste par 'OK'")
            return "OK" in test_response.upper()
        except:
            return False

# Fonction utilitaire
def create_gemini_client() -> GeminiClient:
    """Crée une instance pré-configurée du client Gemini"""
    return GeminiClient()
