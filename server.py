#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Servidor Flask para la aplicación de recomendación de cultivos
Conecta el frontend con el modelo de recomendación y la base de datos
"""

import os
import json
import sqlite3
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys

# Agregar directorio del proyecto al path para importar el modelo
sys.path.append('/home/ubuntu/proyecto_cultivos/src')
from modelo_recomendacion import ModeloRecomendacionCultivos

# Inicializar la aplicación Flask
app = Flask(__name__, static_folder='frontend')
CORS(app)  # Habilitar CORS para todas las rutas

# Configuración
DB_PATH = '/home/ubuntu/proyecto_cultivos/data/db/cultivos.db'
ASSETS_PATH = '/home/ubuntu/proyecto_cultivos/src/frontend/assets'

# Inicializar el modelo de recomendación
modelo = ModeloRecomendacionCultivos(DB_PATH)

# Rutas para servir archivos estáticos
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory(ASSETS_PATH, filename)

# API para obtener todos los cultivos
@app.route('/api/cultivos', methods=['GET'])
def get_cultivos():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Consulta para obtener información básica de cultivos
        cursor.execute("""
            SELECT c.id_cultivo, c.nombre, c.descripcion, c.tipo, c.ciclo_dias, c.densidad_siembra, c.imagen
            FROM cultivos c
        """)
        cultivos_basicos = [dict(row) for row in cursor.fetchall()]
        
        # Para cada cultivo, obtener condiciones y costos
        cultivos_completos = []
        for cultivo in cultivos_basicos:
            # Obtener condiciones
            cursor.execute("""
                SELECT temp_min, temp_max, precipitacion_min, precipitacion_max, 
                       tipo_suelo, ph_min, ph_max, altitud_min, altitud_max
                FROM condiciones
                WHERE id_cultivo = ?
            """, (cultivo['id_cultivo'],))
            condiciones = dict(cursor.fetchone() or {})
            
            # Obtener costos
            cursor.execute("""
                SELECT inversion_min, inversion_max, costo_operativo, 
                       precio_interno, precio_export, rentabilidad
                FROM costos
                WHERE id_cultivo = ?
            """, (cultivo['id_cultivo'],))
            costos = cursor.fetchone()
            
            # Agregar a cultivo completo
            cultivo_completo = cultivo.copy()
            cultivo_completo['condiciones'] = condiciones
            cultivo_completo['costos'] = dict(costos) if costos else None
            
            cultivos_completos.append(cultivo_completo)
        
        conn.close()
        return jsonify(cultivos_completos)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API para obtener un cultivo específico
@app.route('/api/cultivos/<int:id_cultivo>', methods=['GET'])
def get_cultivo(id_cultivo):
    try:
        # Usar el modelo para obtener detalles completos
        detalles = modelo.obtener_detalles_cultivo(id_cultivo)
        return jsonify(detalles)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API para obtener recomendaciones
@app.route('/api/recomendaciones', methods=['POST'])
def get_recomendaciones():
    try:
        # Obtener parámetros del usuario desde el cuerpo de la solicitud
        parametros_usuario = request.json
        
        # Validar parámetros mínimos requeridos
        if not all(key in parametros_usuario for key in ['temperatura', 'precipitacion', 'altitud']):
            return jsonify({"error": "Faltan parámetros obligatorios"}), 400
        
        # Obtener recomendaciones usando el modelo
        recomendaciones = modelo.recomendar_cultivos(parametros_usuario)
        
        return jsonify(recomendaciones)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API para calcular costos de implementación
@app.route('/api/costos/<int:id_cultivo>', methods=['GET'])
def calcular_costos(id_cultivo):
    try:
        # Obtener área de la consulta (opcional)
        area = request.args.get('area', default=1, type=float)
        
        # Calcular costos usando el modelo
        costos = modelo.calcular_costos_implementacion(id_cultivo, area)
        
        return jsonify(costos)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API para obtener proveedores de insumos
@app.route('/api/proveedores/<int:id_cultivo>', methods=['GET'])
def get_proveedores(id_cultivo):
    try:
        # Obtener proveedores usando el modelo
        proveedores = modelo.obtener_proveedores_insumos(id_cultivo)
        
        return jsonify(proveedores)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Iniciar el servidor si se ejecuta directamente
if __name__ == '__main__':
    # Crear directorio de assets si no existe
    os.makedirs(ASSETS_PATH, exist_ok=True)
    
    # Iniciar servidor
    app.run(host='0.0.0.0', port=5000, debug=True)
