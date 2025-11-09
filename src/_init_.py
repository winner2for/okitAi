"""
Okit AI - Package principal
IA multimodale avec Gemini 2.0 Flash et interface vocale
"""

__version__ = "2.0.0"
__author__ = "Okit AI Team"
__description__ = "Assistant IA multimodal avec Gemini 2.0 Flash"

from .gemini_client import GeminiClient
from .voice_handler_android import VoiceHandlerAndroid

__all__ = ['GeminiClient', 'VoiceHandlerAndroid']