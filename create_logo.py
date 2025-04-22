#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para crear un logo minimalista para el proyecto de Cultivos Colombianos
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Configuración
OUTPUT_DIR = '/home/ubuntu/proyecto_cultivos/docs/branding'
COLORS = {
    'primary': (46, 125, 50),     # Verde oscuro
    'secondary': (129, 199, 132), # Verde claro
    'accent': (255, 193, 7),      # Ámbar
    'text': (33, 33, 33),         # Casi negro
    'background': (255, 255, 255) # Blanco
}

def create_logo(size=(500, 500), bg_color=COLORS['background']):
    """Crea un logo minimalista para el proyecto"""
    # Crear imagen base
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Dimensiones
    width, height = size
    center_x, center_y = width // 2, height // 2
    
    # Dibujar círculo verde (representa la tierra/campo)
    circle_radius = min(width, height) // 3
    draw.ellipse(
        (center_x - circle_radius, center_y - circle_radius, 
         center_x + circle_radius, center_y + circle_radius), 
        fill=COLORS['primary']
    )
    
    # Dibujar planta estilizada
    stem_width = circle_radius // 10
    stem_height = circle_radius * 1.2
    
    # Tallo
    draw.rectangle(
        (center_x - stem_width // 2, center_y - stem_height // 2,
         center_x + stem_width // 2, center_y + stem_height // 2),
        fill=COLORS['secondary']
    )
    
    # Hojas (triángulos)
    leaf_size = circle_radius // 2
    
    # Hoja izquierda
    draw.polygon(
        [
            (center_x, center_y - leaf_size // 2),
            (center_x - leaf_size, center_y - leaf_size),
            (center_x - leaf_size // 2, center_y)
        ],
        fill=COLORS['secondary']
    )
    
    # Hoja derecha
    draw.polygon(
        [
            (center_x, center_y - leaf_size // 2),
            (center_x + leaf_size, center_y - leaf_size),
            (center_x + leaf_size // 2, center_y)
        ],
        fill=COLORS['secondary']
    )
    
    # Sol (representado por un semicírculo)
    sun_radius = circle_radius // 2
    draw.arc(
        (center_x - sun_radius, center_y - sun_radius * 3,
         center_x + sun_radius, center_y - sun_radius),
        start=0, end=180, fill=COLORS['accent'], width=stem_width
    )
    
    return img

def create_logo_with_text(size=(800, 500), text="CultivosCO", subtitle="Recomendador de Cultivos"):
    """Crea un logo con texto para el proyecto"""
    # Crear imagen base
    img = Image.new('RGB', size, COLORS['background'])
    
    # Crear logo
    logo_size = min(size[0] // 2, size[1])
    logo = create_logo(size=(logo_size, logo_size))
    
    # Pegar logo en la imagen
    logo_pos = (50, (size[1] - logo_size) // 2)
    img.paste(logo, logo_pos)
    
    # Añadir texto
    draw = ImageDraw.Draw(img)
    
    # Intentar cargar fuentes
    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=60)
        subtitle_font = ImageFont.truetype("DejaVuSans.ttf", size=30)
    except IOError:
        # Usar fuente por defecto si no se encuentra la especificada
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Posición del texto
    text_x = logo_pos[0] + logo_size + 50
    title_y = size[1] // 2 - 50
    subtitle_y = size[1] // 2 + 20
    
    # Dibujar texto
    draw.text((text_x, title_y), text, font=title_font, fill=COLORS['primary'])
    draw.text((text_x, subtitle_y), subtitle, font=subtitle_font, fill=COLORS['text'])
    
    return img

def create_favicon(size=(32, 32)):
    """Crea un favicon para el proyecto"""
    # Crear logo pequeño
    logo = create_logo(size=size)
    return logo

def main():
    """Función principal"""
    # Crear directorio si no existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Crear y guardar logo
    logo = create_logo()
    logo.save(os.path.join(OUTPUT_DIR, "logo.png"), "PNG")
    
    # Crear y guardar logo con texto
    logo_with_text = create_logo_with_text()
    logo_with_text.save(os.path.join(OUTPUT_DIR, "logo_with_text.png"), "PNG")
    
    # Crear y guardar favicon
    favicon = create_favicon()
    favicon.save(os.path.join(OUTPUT_DIR, "favicon.ico"), "ICO")
    
    print("Logos creados exitosamente en:", OUTPUT_DIR)

if __name__ == "__main__":
    main()
