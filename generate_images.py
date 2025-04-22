#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para generar imágenes de ejemplo para los cultivos
"""

import os
import random
from PIL import Image, ImageDraw, ImageFont

# Configuración
OUTPUT_DIR = '/home/ubuntu/proyecto_cultivos/src/frontend/assets/cultivos'
WIDTH = 400
HEIGHT = 300
COLORS = [
    (76, 175, 80),    # Verde
    (139, 195, 74),   # Verde claro
    (205, 220, 57),   # Lima
    (255, 235, 59),   # Amarillo
    (255, 193, 7),    # Ámbar
    (255, 152, 0),    # Naranja
    (121, 85, 72),    # Marrón
]

# Lista de cultivos
CULTIVOS = [
    'maiz', 'arroz', 'trigo', 'cebada', 'sorgo', 'quinua', 'frijol', 'soya', 
    'arveja', 'garbanzo', 'lenteja', 'papa', 'yuca', 'batata', 'name', 
    'arracacha', 'achira', 'banano', 'platano', 'mango', 'papaya', 'pina', 
    'naranja', 'limon', 'gulupa', 'curuba', 'tomate_arbol', 'lulo', 'mora', 
    'fresa', 'uchuva', 'arandano', 'cafe', 'cacao', 'cana_azucar', 'palma_aceite'
]

def create_placeholder_image(cultivo, width=WIDTH, height=HEIGHT):
    """Crea una imagen de marcador de posición para un cultivo"""
    # Crear imagen con color aleatorio
    color = random.choice(COLORS)
    img = Image.new('RGB', (width, height), color)
    draw = ImageDraw.Draw(img)
    
    # Intentar cargar una fuente, usar default si no está disponible
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 30)
    except IOError:
        font = ImageFont.load_default()
    
    # Dibujar texto
    text = cultivo.replace('_', ' ').title()
    textwidth, textheight = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (width//2, height//4)
    
    # Centrar texto
    x = (width - textwidth) // 2
    y = (height - textheight) // 2
    
    # Agregar sombra para legibilidad
    draw.rectangle([(0, y-10), (width, y+textheight+10)], fill=(0, 0, 0, 128))
    
    # Dibujar texto
    draw.text((x, y), text, font=font, fill=(255, 255, 255))
    
    return img

def main():
    """Función principal"""
    # Crear directorio si no existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Crear imagen para cada cultivo
    for cultivo in CULTIVOS:
        filename = os.path.join(OUTPUT_DIR, f"{cultivo}.jpg")
        img = create_placeholder_image(cultivo)
        img.save(filename, "JPEG", quality=90)
        print(f"Creada imagen para {cultivo}")
    
    # Crear imagen default
    default_img = create_placeholder_image("cultivo")
    default_img.save(os.path.join(OUTPUT_DIR, "default.jpg"), "JPEG", quality=90)
    print("Creada imagen default")

if __name__ == "__main__":
    main()
