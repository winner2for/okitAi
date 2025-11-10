"""
Configuration Okit AI - Clé API intégrée
Généré automatiquement par GitHub Actions
"""

import os
import logging

logger = logging.getLogger(__name__)

class AppConfig:
    # Clé API - sera remplacée par GitHub Actions
    # ⚠️ NE METTEZ JAMAIS LA VRAIE CLÉ ICI ⚠️
    GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
    
    @classmethod
    def get_api_key(cls):
        """Récupère la clé API avec fallback"""
        # Priorité 1: Variable d'environnement (GitHub Actions)
        env_key = os.getenv('GEMINI_API_KEY')
        if env_key and env_key != "YOUR_GEMINI_API_KEY_HERE":
            logger.info("✅ Clé API chargée depuis l'environnement")
            return env_key
        
        # Priorité 2: Clé intégrée (APK buildée)
        if cls.GEMINI_API_KEY and cls.GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
            logger.info("✅ Clé API chargée depuis la configuration")
            return cls.GEMINI_API_KEY
        
        # Erreur
        error_msg = "Clé API Gemini non configurée. Le build GitHub doit inclure la clé."
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    @classmethod
    def setup(cls):
        """Configuration de l'application"""
        api_key = cls.get_api_key()
        os.environ["GEMINI_API_KEY"] = api_key
        logger.info("✅ Configuration Okit AI chargée avec Gemini 2.0 Flash")

# Configuration automatique au démarrage
setup()
