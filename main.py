from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
import threading
import os
import logging

from src.gemini_client import GeminiClient
from src.voice_handler_android import VoiceHandlerAndroid

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatBubble(BoxLayout):
    def __init__(self, text, is_user=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(90)
        self.padding = [dp(10), dp(5)]
        self.spacing = dp(10)
        
        if is_user:
            self.build_user_message(text)
        else:
            self.build_bot_message(text)
    
    def build_user_message(self, text):
        """Message utilisateur (à droite)"""
        self.add_widget(BoxLayout(size_hint_x=0.1))
        
        bubble = BoxLayout(
            orientation='vertical',
            size_hint_x=0.7
        )
        
        with bubble.canvas.before:
            Color(0.1, 0.5, 0.9, 1)  # Bleu Okit
            self.rect = RoundedRectangle(
                pos=bubble.pos,
                size=bubble.size,
                radius=[dp(20), dp(20), dp(5), dp(20)]
            )
        
        bubble.bind(pos=self.update_rect, size=self.update_rect)
        
        message = Label(
            text=text,
            text_size=(Window.width * 0.5, None),
            size_hint_y=None,
            height=dp(80),
            halign='right',
            valign='middle',
            color=(1, 1, 1, 1),
            padding=[dp(15), dp(10)],
            font_size='14sp'
        )
        message.bind(texture_size=message.setter('size'))
        bubble.add_widget(message)
        
        self.add_widget(bubble)
        
        avatar = Image(
            source='assets/user_icon.png',
            size_hint=(None, None),
            size=(dp(45), dp(45))
        )
        self.add_widget(avatar)
    
    def build_bot_message(self, text):
        """Message bot (à gauche)"""
        avatar = Image(
            source='assets/wolf_icon.png',
            size_hint=(None, None),
            size=(dp(45), dp(45))
        )
        self.add_widget(avatar)
        
        bubble = BoxLayout(
            orientation='vertical',
            size_hint_x=0.7
        )
        
        with bubble.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Gris clair
            self.rect = RoundedRectangle(
                pos=bubble.pos,
                size=bubble.size,
                radius=[dp(5), dp(20), dp(20), dp(20)]
            )
        
        bubble.bind(pos=self.update_rect, size=self.update_rect)
        
        message = Label(
            text=text,
            text_size=(Window.width * 0.5, None),
            size_hint_y=None,
            height=dp(80),
            halign='left',
            valign='middle',
            color=(0.1, 0.1, 0.1, 1),
            padding=[dp(15), dp(10)],
            font_size='14sp'
        )
        message.bind(texture_size=message.setter('size'))
        bubble.add_widget(message)
        
        self.add_widget(bubble)
        self.add_widget(BoxLayout(size_hint_x=0.1))
    
    def update_rect(self, *args):
        if hasattr(self, 'rect'):
            self.rect.pos = self.pos
            self.rect.size = self.size

class OkitAIApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gemini_client = None
        self.voice_handler = None
        self.is_voice_active = False
        self.title = "Okit AI 🐺"
        
    def build(self):
        # Configuration de la fenêtre
        Window.clearcolor = get_color_from_hex('#f8f9fa')
        
        # Layout principal
        main_layout = BoxLayout(
            orientation='vertical', 
            spacing=dp(10), 
            padding=[dp(15), dp(15), dp(15), dp(10)]
        )
        
        # Header avec dégradé
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(80),
            spacing=dp(15)
        )
        
        with header.canvas.before:
            Color(0.4, 0.2, 0.8, 1)  # Violet Okit
            Rectangle(pos=header.pos, size=header.size)
        
        logo = Image(
            source='assets/wolf_icon.png',
            size_hint=(None, None),
            size=(dp(60), dp(60))
        )
        
        title_layout = BoxLayout(orientation='vertical', spacing=dp(2))
        title = Label(
            text='[b]Okit AI[/b]',
            size_hint_x=0.8,
            font_size='22sp',
            color=(1, 1, 1, 1),
            markup=True
        )
        subtitle = Label(
            text='Assistant Gemini 2.0 Flash',
            size_hint_x=0.8,
            font_size='12sp',
            color=(1, 1, 1, 0.8)
        )
        
        title_layout.add_widget(title)
        title_layout.add_widget(subtitle)
        
        header.add_widget(logo)
        header.add_widget(title_layout)
        header.add_widget(BoxLayout())  # Espace flexible
        
        # Zone de chat
        self.chat_scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False
        )
        self.chat_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            padding=[dp(5), dp(10)]
        )
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.chat_scroll.add_widget(self.chat_layout)
        
        # Zone de saisie
        input_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(65),
            spacing=dp(10)
        )
        
        self.message_input = TextInput(
            hint_text='Tapez votre message...',
            size_hint_x=0.65,
            multiline=False,
            background_color=(1, 1, 1, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            padding=[dp(15), dp(12)],
            font_size='14sp',
            background_normal='',
            background_active='',
            background_color=(1, 1, 1, 0.9)
        )
        self.message_input.bind(on_text_validate=self.send_message)
        
        self.voice_btn = Button(
            text='🎤',
            size_hint_x=0.15,
            background_color=(0.8, 0.2, 0.2, 1),
            font_size='16sp',
            background_normal=''
        )
        self.voice_btn.bind(on_press=self.toggle_voice)
        
        self.send_btn = Button(
            text='➤',
            size_hint_x=0.2,
            background_color=(0.2, 0.6, 1, 1),
            font_size='18sp',
            background_normal=''
        )
        self.send_btn.bind(on_press=self.send_message)
        
        input_layout.add_widget(self.message_input)
        input_layout.add_widget(self.voice_btn)
        input_layout.add_widget(self.send_btn)
        
        # Assemblage final
        main_layout.add_widget(header)
        main_layout.add_widget(self.chat_scroll)
        main_layout.add_widget(input_layout)
        
        # Initialisation différée
        Clock.schedule_once(self.initialize_services, 0.5)
        
        return main_layout
    
    def initialize_services(self, dt):
        """Initialiser Gemini et Voice"""
        def init_services():
            try:
                self.gemini_client = GeminiClient()
                self.voice_handler = VoiceHandlerAndroid()
                Clock.schedule_once(lambda dt: self.add_message(
                    "🐺 Bonjour ! Je suis Okit AI, propulsé par Gemini 2.0 Flash. " +
                    "Comment puis-je vous aider aujourd'hui ?", False
                ), 0)
                logger.info("✅ Services initialisés avec succès")
            except Exception as e:
                error_msg = f"❌ Erreur d'initialisation: {str(e)}"
                logger.error(error_msg)
                Clock.schedule_once(lambda dt: self.add_message(error_msg, False), 0)
        
        threading.Thread(target=init_services, daemon=True).start()
    
    def add_message(self, text, is_user=False):
        """Ajouter un message au chat"""
        def add_msg(dt):
            message = ChatBubble(text, is_user)
            self.chat_layout.add_widget(message)
            Clock.schedule_once(self.scroll_to_bottom, 0.1)
        
        Clock.schedule_once(add_msg, 0)
    
    def scroll_to_bottom(self, dt):
        """Scroller vers le bas"""
        if len(self.chat_layout.children) > 0:
            self.chat_scroll.scroll_to(self.chat_layout.children[0])
    
    def send_message(self, instance):
        """Envoyer un message à Gemini"""
        message = self.message_input.text.strip()
        if not message:
            return
        
        if not self.gemini_client:
            self.add_message("⏳ Initialisation de l'IA en cours...", False)
            return
        
        self.message_input.text = ''
        self.add_message(message, True)
        
        def get_response():
            try:
                response = self.gemini_client.generate_text(message)
                Clock.schedule_once(lambda dt: self.add_message(response, False), 0)
            except Exception as e:
                error_msg = f"❌ Erreur: {str(e)}"
                Clock.schedule_once(lambda dt: self.add_message(error_msg, False), 0)
        
        threading.Thread(target=get_response, daemon=True).start()
    
    def toggle_voice(self, instance):
        """Activer/désactiver la reconnaissance vocale"""
        if not self.voice_handler:
            self.add_message("❌ Service vocal non disponible", False)
            return
        
        if self.is_voice_active:
            self.voice_handler.stop_listening()
            self.voice_btn.background_color = (0.8, 0.2, 0.2, 1)
            self.is_voice_active = False
            self.add_message("🔇 Reconnaissance vocale désactivée", False)
        else:
            def on_voice_result(text):
                if text and "Erreur" not in text and "compris" not in text:
                    self.message_input.text = text
                    self.send_message(None)
            
            self.voice_handler.start_listening(on_voice_result)
            self.voice_btn.background_color = (0.2, 0.8, 0.2, 1)
            self.is_voice_active = True
            self.add_message("🎤 Parlez maintenant...", False)

if __name__ == '__main__':
    OkitAIApp().run()