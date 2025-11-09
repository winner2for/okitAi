#!/usr/bin/env python3
"""
Crée les assets par défaut pour Okit AI
"""

from PIL import Image, ImageDraw
import os

def create_wolf_icon():
    """Crée une icône de loup stylisée"""
    size = (512, 512)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Fond circulaire bleu
    draw.ellipse([50, 50, 462, 462], fill=(100, 150, 255, 255))
    
    # Tête de loup
    draw.ellipse([150, 150, 362, 362], fill=(255, 255, 255, 255))
    
    # Oreilles
    draw.ellipse([180, 180, 230, 230], fill=(255, 255, 255, 255))  # Gauche
    draw.ellipse([282, 180, 332, 230], fill=(255, 255, 255, 255))  # Droite
    
    # Yeux
    draw.ellipse([200, 250, 220, 270], fill=(50, 50, 50, 255))  # Gauche
    draw.ellipse([292, 250, 312, 270], fill=(50, 50, 50, 255))  # Droite
    
    # Museau
    draw.ellipse([240, 300, 272, 332], fill=(200, 200, 200, 255))
    
    img.save('assets/wolf_icon.png', 'PNG')
    print("✅ Icône loup créée")

def create_user_icon():
    """Crée une icône utilisateur simple"""
    size = (512, 512)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Fond circulaire vert
    draw.ellipse([50, 50, 462, 462], fill=(100, 200, 100, 255))
    
    # Tête
    draw.ellipse([200, 150, 312, 262], fill=(255, 255, 255, 255))
    
    # Corps
    draw.ellipse([180, 262, 332, 412], fill=(255, 255, 255, 255))
    
    img.save('assets/user_icon.png', 'PNG')
    print("✅ Icône utilisateur créée")

def create_app_icon():
    """Crée l'icône principale de l'app"""
    size = (512, 512)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Fond dégradé violet (couleur Okit AI)
    for i in range(512):
        alpha = int(255 * (1 - i/512))
        draw.ellipse([i//4, i//4, 512-i//4, 512-i//4], 
                    fill=(100, 50, 200, alpha))
    
    # Logo loup simplifié
    draw.ellipse([150, 150, 362, 362], fill=(255, 255, 255, 255))
    draw.ellipse([180, 180, 230, 230], fill=(255, 255, 255, 255))
    draw.ellipse([282, 180, 332, 230], fill=(255, 255, 255, 255))
    draw.ellipse([200, 250, 220, 270], fill=(100, 50, 200, 255))
    draw.ellipse([292, 250, 312, 270], fill=(100, 50, 200, 255))
    
    img.save('assets/icon.png', 'PNG')
    print("✅ Icône app créée")

def main():
    """Crée tous les assets"""
    os.makedirs('assets', exist_ok=True)
    
    create_wolf_icon()
    create_user_icon()
    create_app_icon()
    
    print("🎉 Tous les assets créés avec succès !")

if __name__ == '__main__':
    main()
