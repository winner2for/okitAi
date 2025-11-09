#!/usr/bin/env python3
"""
Script pour builder l'APK avec la clé API intégrée
Utilisé par GitHub Actions
"""

import os
import sys
import hashlib

def update_config_file(api_key: str):
    """Met à jour le fichier config.py avec la vraie clé API"""
    
    # Vérification basique de la clé
    if not api_key.startswith('AIza'):
        raise ValueError("❌ Format de clé API invalide")
    
    if len(api_key) < 20:
        raise ValueError("❌ Clé API trop courte")
    
    # Hash pour logging (sécurisé)
    key_hash = hashlib.md5(api_key.encode()).hexdigest()[:8]
    print(f"🔑 Injection de la clé API (hash: {key_hash})")
    
    config_content = f'''"""
Configuration Okit AI - Clé API intégrée
Généré automatiquement par GitHub Actions
"""

import os
import logging

logger = logging.getLogger(__name__)

class AppConfig:
    # Clé API intégrée lors du build
    GEMINI_API_KEY = "{api_key}"
    
    @classmethod
    def get_api_key(cls):
        """Récupère la clé API avec fallback"""
        # Priorité 1: Variable d'environnement (GitHub Actions)
        env_key = os.getenv('GEMINI_API_KEY')
        if env_key and env_key != "GEMINI_API_KEY_PLACEHOLDER":
            logger.info("✅ Clé API chargée depuis l'environnement")
            return env_key
        
        # Priorité 2: Clé intégrée (APK buildée)
        if cls.GEMINI_API_KEY and cls.GEMINI_API_KEY != "GEMINI_API_KEY_PLACEHOLDER":
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
'''
    
    with open('src/config.py', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print("✅ Fichier config.py mis à jour avec Gemini 2.0 Flash")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python build_apk_with_key.py <GEMINI_API_KEY>")
        sys.exit(1)
    
    api_key = sys.argv[1]
    
    try:
        update_config_file(api_key)
        print("🎉 Clé API intégrée avec succès !")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)
