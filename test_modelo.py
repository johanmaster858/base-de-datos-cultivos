#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de prueba corregido para validar el modelo de recomendación de cultivos
"""

import sqlite3
import json
import sys
import os
import re

# Agregar directorio del proyecto al path para importar el modelo
sys.path.append('/home/ubuntu/proyecto_cultivos/src')
from modelo_recomendacion import ModeloRecomendacionCultivos

# Configuración
DB_PATH = '/home/ubuntu/proyecto_cultivos/data/db/cultivos.db'
OUTPUT_DIR = '/home/ubuntu/proyecto_cultivos/tests'

# Crear directorio de salida si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

def test_recomendaciones():
    """Prueba el sistema de recomendación con diferentes escenarios"""
    print("Iniciando pruebas del modelo de recomendación...")
    
    # Inicializar modelo
    modelo = ModeloRecomendacionCultivos(DB_PATH)
    
    # Definir casos de prueba
    casos_prueba = [
        {
            "nombre": "Zona cafetera",
            "parametros": {
                "temperatura": 21.0,
                "precipitacion": 2200,
                "altitud": 1500,
                "tipo_suelo": "Franco",
                "ph_suelo": 5.8,
                "experiencia": "Media",
                "preferencia_mercado": "Exportación"
            }
        },
        {
            "nombre": "Zona costera",
            "parametros": {
                "temperatura": 28.0,
                "precipitacion": 1500,
                "altitud": 200,
                "tipo_suelo": "Arenoso",
                "ph_suelo": 6.5,
                "experiencia": "Baja",
                "preferencia_mercado": "Local"
            }
        },
        {
            "nombre": "Zona andina alta",
            "parametros": {
                "temperatura": 14.0,
                "precipitacion": 900,
                "altitud": 2800,
                "tipo_suelo": "Franco arcilloso",
                "ph_suelo": 5.5,
                "experiencia": "Alta",
                "preferencia_mercado": "Local"
            }
        },
        {
            "nombre": "Llanos orientales",
            "parametros": {
                "temperatura": 27.0,
                "precipitacion": 2500,
                "altitud": 300,
                "tipo_suelo": "Franco",
                "ph_suelo": 5.0,
                "experiencia": "Media",
                "preferencia_mercado": "Ambos"
            }
        }
    ]
    
    # Ejecutar pruebas
    resultados = {}
    
    for caso in casos_prueba:
        print(f"\nProbando caso: {caso['nombre']}")
        print(f"Parámetros: {json.dumps(caso['parametros'], indent=2)}")
        
        try:
            # Obtener recomendaciones
            recomendaciones = modelo.recomendar_cultivos(caso['parametros'])
            
            # Guardar resultados
            resultados[caso['nombre']] = {
                "parametros": caso['parametros'],
                "recomendaciones": recomendaciones
            }
            
            # Mostrar resultados resumidos
            print(f"Se encontraron {len(recomendaciones)} cultivos recomendados:")
            for i, rec in enumerate(recomendaciones[:3], 1):
                print(f"  {i}. {rec['nombre']} (Puntuación: {rec['puntuacion']})")
                print(f"     Tipo: {rec['tipo']}")
                print(f"     Condiciones: {rec['condiciones_optimas']['temperatura']} | {rec['condiciones_optimas']['precipitacion']}")
        
        except Exception as e:
            print(f"Error en caso {caso['nombre']}: {e}")
            resultados[caso['nombre']] = {
                "parametros": caso['parametros'],
                "error": str(e)
            }
    
    # Guardar resultados en archivo
    with open(os.path.join(OUTPUT_DIR, 'resultados_pruebas.json'), 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    
    print("\nPruebas completadas. Resultados guardados en:", os.path.join(OUTPUT_DIR, 'resultados_pruebas.json'))
    
    # Cerrar conexión
    modelo.cerrar_conexion()
    
    return resultados

def test_detalles_cultivo():
    """Prueba la obtención de detalles de cultivos específicos"""
    print("\nProbando obtención de detalles de cultivos...")
    
    # Inicializar modelo
    modelo = ModeloRecomendacionCultivos(DB_PATH)
    
    # Cultivos a probar
    cultivos_prueba = [1, 12, 33]  # Maíz, Papa, Café
    
    resultados = {}
    
    for id_cultivo in cultivos_prueba:
        try:
            # Obtener detalles
            detalles = modelo.obtener_detalles_cultivo(id_cultivo)
            
            # Guardar resultados
            resultados[id_cultivo] = detalles
            
            # Mostrar resultados resumidos
            print(f"\nDetalles de {detalles['nombre']}:")
            print(f"  Tipo: {detalles['tipo']}")
            print(f"  Ciclo: {detalles['ciclo_dias']} días")
            print(f"  Condiciones: {detalles['condiciones_optimas']['temperatura']} | {detalles['condiciones_optimas']['precipitacion']}")
            
            if 'costos' in detalles:
                print(f"  Inversión: {detalles['costos']['inversion_inicial']}")
                print(f"  Rentabilidad: {detalles['costos']['rentabilidad_estimada']}")
        
        except Exception as e:
            print(f"Error al obtener detalles del cultivo {id_cultivo}: {e}")
            resultados[id_cultivo] = {"error": str(e)}
    
    # Guardar resultados en archivo
    with open(os.path.join(OUTPUT_DIR, 'detalles_cultivos.json'), 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    
    print("\nPruebas de detalles completadas. Resultados guardados en:", os.path.join(OUTPUT_DIR, 'detalles_cultivos.json'))
    
    # Cerrar conexión
    modelo.cerrar_conexion()
    
    return resultados

def test_costos_implementacion():
    """Prueba el cálculo de costos de implementación"""
    print("\nProbando cálculo de costos de implementación...")
    
    # Inicializar modelo
    modelo = ModeloRecomendacionCultivos(DB_PATH)
    
    # Cultivos y áreas a probar
    casos_prueba = [
        {"id_cultivo": 1, "area": 1.0},    # Maíz, 1 hectárea
        {"id_cultivo": 12, "area": 2.5},   # Papa, 2.5 hectáreas
        {"id_cultivo": 33, "area": 5.0}    # Café, 5 hectáreas
    ]
    
    resultados = {}
    
    for caso in casos_prueba:
        try:
            # Calcular costos
            costos = modelo.calcular_costos_implementacion(caso['id_cultivo'], caso['area'])
            
            # Guardar resultados
            resultados[f"{caso['id_cultivo']}_{caso['area']}ha"] = costos
            
            # Mostrar resultados resumidos
            print(f"\nCostos para cultivo ID {caso['id_cultivo']} en {caso['area']} hectáreas:")
            print(f"  Inversión inicial: {costos['inversion_inicial']['rango']}")
            print(f"  Costos operativos: {costos['costos_operativos']['total']}")
            print(f"  Rentabilidad estimada: {costos['estimacion_ingresos']['rentabilidad_estimada']}")
        
        except Exception as e:
            print(f"Error al calcular costos para cultivo {caso['id_cultivo']}: {e}")
            resultados[f"{caso['id_cultivo']}_{caso['area']}ha"] = {"error": str(e)}
    
    # Guardar resultados en archivo
    with open(os.path.join(OUTPUT_DIR, 'costos_implementacion.json'), 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    
    print("\nPruebas de costos completadas. Resultados guardados en:", os.path.join(OUTPUT_DIR, 'costos_implementacion.json'))
    
    # Cerrar conexión
    modelo.cerrar_conexion()
    
    return resultados

def validar_recomendaciones(resultados):
    """Valida la calidad de las recomendaciones generadas"""
    print("\nValidando calidad de las recomendaciones...")
    
    validaciones = {}
    
    for caso, datos in resultados.items():
        if "error" in datos:
            validaciones[caso] = {"estado": "error", "mensaje": datos["error"]}
            continue
        
        parametros = datos["parametros"]
        recomendaciones = datos["recomendaciones"]
        
        # Verificar que hay recomendaciones
        if not recomendaciones:
            validaciones[caso] = {"estado": "error", "mensaje": "No se generaron recomendaciones"}
            continue
        
        # Verificar coherencia con parámetros
        coherencia = True
        mensajes = []
        
        # Verificar top 3 recomendaciones
        for i, rec in enumerate(recomendaciones[:min(3, len(recomendaciones))]):
            # Verificar temperatura
            temp_str = rec['condiciones_optimas']['temperatura']
            temp_match = re.search(r'(\d+)\s*-\s*(\d+)', temp_str)
            if temp_match:
                temp_min = int(temp_match.group(1))
                temp_max = int(temp_match.group(2))
                if not (temp_min - 5 <= parametros['temperatura'] <= temp_max + 5):
                    coherencia = False
                    mensajes.append(f"Recomendación {i+1} ({rec['nombre']}): Temperatura {temp_str} no coherente con parámetro {parametros['temperatura']}")
            
            # Verificar altitud
            alt_str = rec['condiciones_optimas']['altitud']
            alt_match = re.search(r'(\d+)\s*-\s*(\d+)', alt_str)
            if alt_match:
                alt_min = int(alt_match.group(1))
                alt_max = int(alt_match.group(2))
                if not (alt_min - 300 <= parametros['altitud'] <= alt_max + 300):
                    coherencia = False
                    mensajes.append(f"Recomendación {i+1} ({rec['nombre']}): Altitud {alt_str} no coherente con parámetro {parametros['altitud']}")
        
        # Verificar diversidad de tipos
        tipos = set(rec['tipo'] for rec in recomendaciones[:min(5, len(recomendaciones))])
        if len(tipos) < 2 and len(recomendaciones) >= 3:
            mensajes.append(f"Poca diversidad en tipos de cultivo: {tipos}")
        
        # Guardar resultado de validación
        validaciones[caso] = {
            "estado": "válido" if coherencia else "advertencia",
            "mensaje": "Recomendaciones coherentes con parámetros" if coherencia else "Algunas recomendaciones pueden no ser óptimas",
            "detalles": mensajes
        }
    
    # Guardar validaciones en archivo
    with open(os.path.join(OUTPUT_DIR, 'validacion_recomendaciones.json'), 'w', encoding='utf-8') as f:
        json.dump(validaciones, f, ensure_ascii=False, indent=2)
    
    print("\nValidación completada. Resultados guardados en:", os.path.join(OUTPUT_DIR, 'validacion_recomendaciones.json'))
    
    # Mostrar resumen
    for caso, validacion in validaciones.items():
        print(f"\nCaso: {caso}")
        print(f"  Estado: {validacion['estado']}")
        print(f"  Mensaje: {validacion['mensaje']}")
        if "detalles" in validacion and validacion["detalles"]:
            print("  Detalles:")
            for detalle in validacion["detalles"]:
                print(f"    - {detalle}")
    
    return validaciones

def main():
    """Función principal"""
    print("=== PRUEBAS DEL SISTEMA DE RECOMENDACIÓN DE CULTIVOS ===\n")
    
    # Probar recomendaciones
    resultados = test_recomendaciones()
    
    # Probar detalles de cultivos
    test_detalles_cultivo()
    
    # Probar cálculo de costos
    test_costos_implementacion()
    
    # Validar calidad de recomendaciones
    validar_recomendaciones(resultados)
    
    print("\n=== PRUEBAS COMPLETADAS ===")

if __name__ == "__main__":
    main()
