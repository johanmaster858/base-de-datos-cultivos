import sqlite3
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

class ModeloRecomendacionCultivos:
    """
    Modelo de predicción y recomendación de cultivos para Colombia
    basado en condiciones específicas del usuario y datos históricos.
    """
    
    def __init__(self, db_path):
        """
        Inicializa el modelo con la conexión a la base de datos.
        
        Args:
            db_path (str): Ruta al archivo de base de datos SQLite
        """
        self.db_path = db_path
        self.conn = None
        self.cultivos_df = None
        self.condiciones_df = None
        self.costos_df = None
        self.zonas_df = None
        self.plagas_df = None
        self.insumos_df = None
        self.tecnicas_df = None
        self.certificaciones_df = None
        
        # Cargar datos
        self._cargar_datos()
    
    def _cargar_datos(self):
        """Carga los datos necesarios desde la base de datos."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            
            # Cargar tablas principales
            self.cultivos_df = pd.read_sql("SELECT * FROM cultivos", self.conn)
            self.condiciones_df = pd.read_sql("SELECT * FROM condiciones", self.conn)
            self.costos_df = pd.read_sql("SELECT * FROM costos", self.conn)
            self.zonas_df = pd.read_sql("SELECT * FROM zonas", self.conn)
            
            # Cargar relaciones
            self.cultivo_zona_df = pd.read_sql("SELECT * FROM cultivo_zona", self.conn)
            
            # Cargar datos complementarios
            self.plagas_df = pd.read_sql("""
                SELECT pe.*, cp.id_cultivo, cp.severidad, cp.frecuencia 
                FROM plagas_enfermedades pe
                JOIN cultivo_plaga cp ON pe.id_plaga = cp.id_plaga
            """, self.conn)
            
            self.insumos_cultivo_df = pd.read_sql("""
                SELECT i.*, ic.id_cultivo, ic.cantidad_por_ha, ic.etapa_aplicacion, ic.frecuencia
                FROM insumos i
                JOIN insumo_cultivo ic ON i.id_insumo = ic.id_insumo
            """, self.conn)
            
            self.tecnicas_cultivo_df = pd.read_sql("""
                SELECT t.*, tc.id_cultivo, tc.importancia, tc.etapa_aplicacion
                FROM tecnicas t
                JOIN tecnica_cultivo tc ON t.id_tecnica = tc.id_tecnica
            """, self.conn)
            
            self.certificaciones_cultivo_df = pd.read_sql("""
                SELECT c.*, cc.id_cultivo, cc.mercado_objetivo, cc.premium_precio
                FROM certificaciones c
                JOIN cultivo_certificacion cc ON c.id_certificacion = cc.id_certificacion
            """, self.conn)
            
            print(f"Datos cargados correctamente. {len(self.cultivos_df)} cultivos disponibles.")
        except Exception as e:
            print(f"Error al cargar datos: {e}")
    
    def recomendar_cultivos(self, parametros_usuario):
        """
        Recomienda cultivos basados en los parámetros proporcionados por el usuario.
        
        Args:
            parametros_usuario (dict): Diccionario con los parámetros del usuario
                - temperatura (float): Temperatura promedio en °C
                - precipitacion (float): Precipitación anual en mm
                - altitud (int): Altitud en msnm
                - tipo_suelo (str, opcional): Tipo de suelo
                - ph_suelo (float, opcional): pH del suelo
                - area_disponible (float, opcional): Área disponible en hectáreas
                - presupuesto (float, opcional): Presupuesto disponible en COP
                - experiencia (str, opcional): Nivel de experiencia ('Baja', 'Media', 'Alta')
                - departamento (str, opcional): Departamento de Colombia
                - preferencia_mercado (str, opcional): Preferencia de mercado ('Local', 'Exportación')
                - tiempo_disponible (int, opcional): Tiempo disponible en días
        
        Returns:
            list: Lista de diccionarios con las recomendaciones de cultivos
        """
        # Extraer parámetros obligatorios
        temperatura = parametros_usuario.get('temperatura')
        precipitacion = parametros_usuario.get('precipitacion')
        altitud = parametros_usuario.get('altitud')
        
        if temperatura is None or precipitacion is None or altitud is None:
            raise ValueError("Los parámetros temperatura, precipitación y altitud son obligatorios")
        
        # Filtrar cultivos por condiciones básicas
        cultivos_filtrados = self._filtrar_por_condiciones_basicas(temperatura, precipitacion, altitud)
        
        # Si hay parámetros adicionales, refinar la búsqueda
        if 'tipo_suelo' in parametros_usuario and parametros_usuario['tipo_suelo']:
            cultivos_filtrados = self._filtrar_por_tipo_suelo(cultivos_filtrados, parametros_usuario['tipo_suelo'])
        
        if 'ph_suelo' in parametros_usuario and parametros_usuario['ph_suelo']:
            cultivos_filtrados = self._filtrar_por_ph(cultivos_filtrados, parametros_usuario['ph_suelo'])
        
        if 'presupuesto' in parametros_usuario and parametros_usuario['presupuesto']:
            cultivos_filtrados = self._filtrar_por_presupuesto(cultivos_filtrados, parametros_usuario['presupuesto'])
        
        if 'tiempo_disponible' in parametros_usuario and parametros_usuario['tiempo_disponible']:
            cultivos_filtrados = self._filtrar_por_tiempo(cultivos_filtrados, parametros_usuario['tiempo_disponible'])
        
        if 'departamento' in parametros_usuario and parametros_usuario['departamento']:
            cultivos_filtrados = self._ajustar_por_zona(cultivos_filtrados, parametros_usuario['departamento'])
        
        if 'preferencia_mercado' in parametros_usuario and parametros_usuario['preferencia_mercado']:
            cultivos_filtrados = self._ajustar_por_mercado(cultivos_filtrados, parametros_usuario['preferencia_mercado'])
        
        # Calcular puntuación de compatibilidad
        cultivos_puntuados = self._calcular_puntuacion(cultivos_filtrados, parametros_usuario)
        
        # Ordenar por puntuación y seleccionar los mejores
        cultivos_recomendados = cultivos_puntuados.sort_values('puntuacion', ascending=False).head(10)
        
        # Preparar resultados detallados
        resultados = self._preparar_resultados_detallados(cultivos_recomendados)
        
        return resultados
    
    def _filtrar_por_condiciones_basicas(self, temperatura, precipitacion, altitud):
        """
        Filtra cultivos que se adaptan a las condiciones básicas proporcionadas.
        """
        # Unir tablas de cultivos y condiciones
        df = pd.merge(self.cultivos_df, self.condiciones_df, on='id_cultivo')
        
        # Filtrar por temperatura
        df_temp = df[(df['temp_min'] <= temperatura) & (df['temp_max'] >= temperatura)]
        
        # Si no hay resultados, relajar un poco el filtro de temperatura
        if len(df_temp) == 0:
            margen = 2.0  # Margen de tolerancia en °C
            df_temp = df[(df['temp_min'] - margen <= temperatura) & (df['temp_max'] + margen >= temperatura)]
        
        # Filtrar por precipitación
        df_precip = df_temp[(df_temp['precipitacion_min'] <= precipitacion) & 
                            (df_temp['precipitacion_max'] >= precipitacion)]
        
        # Si no hay resultados, relajar un poco el filtro de precipitación
        if len(df_precip) == 0:
            margen = 200  # Margen de tolerancia en mm
            df_precip = df_temp[(df_temp['precipitacion_min'] - margen <= precipitacion) & 
                               (df_temp['precipitacion_max'] + margen >= precipitacion)]
        
        # Filtrar por altitud
        df_alt = df_precip[(df_precip['altitud_min'] <= altitud) & 
                          (df_precip['altitud_max'] >= altitud)]
        
        # Si no hay resultados, relajar un poco el filtro de altitud
        if len(df_alt) == 0:
            margen = 200  # Margen de tolerancia en msnm
            df_alt = df_precip[(df_precip['altitud_min'] - margen <= altitud) & 
                             (df_precip['altitud_max'] + margen >= altitud)]
        
        return df_alt
    
    def _filtrar_por_tipo_suelo(self, df, tipo_suelo):
        """Filtra cultivos por tipo de suelo."""
        # Búsqueda flexible por palabras clave en el tipo de suelo
        palabras_clave = tipo_suelo.lower().split()
        
        # Crear una máscara para cada palabra clave
        mascara = df['tipo_suelo'].str.lower().apply(
            lambda x: any(palabra in x for palabra in palabras_clave) if isinstance(x, str) else False
        )
        
        df_filtrado = df[mascara]
        
        # Si no hay resultados, devolver el dataframe original
        if len(df_filtrado) == 0:
            return df
        
        return df_filtrado
    
    def _filtrar_por_ph(self, df, ph_suelo):
        """Filtra cultivos por pH del suelo."""
        return df[(df['ph_min'] <= ph_suelo) & (df['ph_max'] >= ph_suelo)]
    
    def _filtrar_por_presupuesto(self, df, presupuesto):
        """Filtra cultivos por presupuesto disponible."""
        # Unir con tabla de costos
        df_con_costos = pd.merge(df, self.costos_df, on='id_cultivo')
        
        # Filtrar por inversión mínima
        df_filtrado = df_con_costos[df_con_costos['inversion_min'] <= presupuesto]
        
        return df_filtrado
    
    def _filtrar_por_tiempo(self, df, tiempo_disponible):
        """Filtra cultivos por tiempo disponible."""
        # Convertir tiempo a días si es necesario
        tiempo_dias = tiempo_disponible
        
        # Filtrar por ciclo de cultivo
        df_filtrado = df[df['ciclo_dias'] <= tiempo_dias]
        
        return df_filtrado
    
    def _ajustar_por_zona(self, df, departamento):
        """Ajusta recomendaciones según la zona geográfica."""
        # Buscar zonas que coincidan con el departamento
        zonas_dept = self.zonas_df[self.zonas_df['departamento'].str.lower() == departamento.lower()]
        
        if len(zonas_dept) == 0:
            return df  # Si no hay zonas específicas, mantener recomendaciones originales
        
        # Obtener cultivos populares en esas zonas
        ids_zonas = zonas_dept['id_zona'].tolist()
        cultivos_zona = self.cultivo_zona_df[self.cultivo_zona_df['id_zona'].isin(ids_zonas)]
        
        # Unir con el dataframe filtrado y ajustar puntuación
        df_con_zona = pd.merge(df, cultivos_zona, on='id_cultivo', how='left')
        
        # Si un cultivo está en la zona, se mantiene; si no, se filtra
        df_filtrado = df_con_zona[~df_con_zona['id_zona'].isna()]
        
        # Si no quedan cultivos, devolver el original
        if len(df_filtrado) == 0:
            return df
        
        return df_filtrado
    
    def _ajustar_por_mercado(self, df, preferencia_mercado):
        """Ajusta recomendaciones según preferencia de mercado."""
        # Unir con tabla de costos para obtener información de precios
        df_con_costos = pd.merge(df, self.costos_df, on='id_cultivo')
        
        if preferencia_mercado.lower() == 'exportación':
            # Priorizar cultivos con precio de exportación
            df_filtrado = df_con_costos[~df_con_costos['precio_export'].isna()]
            
            # Si no hay cultivos de exportación, mantener los originales
            if len(df_filtrado) == 0:
                return df
            
            return df_filtrado
        else:  # Mercado local
            # Priorizar cultivos con precio interno
            df_filtrado = df_con_costos[~df_con_costos['precio_interno'].isna()]
            
            # Si no hay cultivos para mercado local, mantener los originales
            if len(df_filtrado) == 0:
                return df
            
            return df_filtrado
    
    def _calcular_puntuacion(self, df, parametros_usuario):
        """
        Calcula una puntuación de compatibilidad para cada cultivo.
        """
        if len(df) == 0:
            return pd.DataFrame()
        
        # Crear copia para no modificar el original
        df_puntuado = df.copy()
        
        # Inicializar puntuación base
        df_puntuado['puntuacion'] = 100.0
        
        # Ajustar por cercanía a condiciones óptimas
        temperatura = parametros_usuario.get('temperatura')
        precipitacion = parametros_usuario.get('precipitacion')
        altitud = parametros_usuario.get('altitud')
        
        # Temperatura óptima es el promedio de min y max
        df_puntuado['temp_optima'] = (df_puntuado['temp_min'] + df_puntuado['temp_max']) / 2
        df_puntuado['distancia_temp'] = abs(df_puntuado['temp_optima'] - temperatura)
        # Normalizar y ajustar puntuación (máx 20 puntos)
        max_dist_temp = df_puntuado['distancia_temp'].max() if df_puntuado['distancia_temp'].max() > 0 else 1
        df_puntuado['ajuste_temp'] = 20 * (1 - df_puntuado['distancia_temp'] / max_dist_temp)
        
        # Precipitación óptima es el promedio de min y max
        df_puntuado['precip_optima'] = (df_puntuado['precipitacion_min'] + df_puntuado['precipitacion_max']) / 2
        df_puntuado['distancia_precip'] = abs(df_puntuado['precip_optima'] - precipitacion)
        # Normalizar y ajustar puntuación (máx 20 puntos)
        max_dist_precip = df_puntuado['distancia_precip'].max() if df_puntuado['distancia_precip'].max() > 0 else 1
        df_puntuado['ajuste_precip'] = 20 * (1 - df_puntuado['distancia_precip'] / max_dist_precip)
        
        # Altitud óptima es el promedio de min y max
        df_puntuado['altitud_optima'] = (df_puntuado['altitud_min'] + df_puntuado['altitud_max']) / 2
        df_puntuado['distancia_altitud'] = abs(df_puntuado['altitud_optima'] - altitud)
        # Normalizar y ajustar puntuación (máx 20 puntos)
        max_dist_altitud = df_puntuado['distancia_altitud'].max() if df_puntuado['distancia_altitud'].max() > 0 else 1
        df_puntuado['ajuste_altitud'] = 20 * (1 - df_puntuado['distancia_altitud'] / max_dist_altitud)
        
        # Ajustar puntuación base con los ajustes calculados
        df_puntuado['puntuacion'] = df_puntuado['puntuacion'] - 20 + df_puntuado['ajuste_temp']
        df_puntuado['puntuacion'] = df_puntuado['puntuacion'] - 20 + df_puntuado['ajuste_precip']
        df_puntuado['puntuacion'] = df_puntuado['puntuacion'] - 20 + df_puntuado['ajuste_altitud']
        
        # Ajustar por rentabilidad si hay datos de costos
        if 'rentabilidad' in df_puntuado.columns:
            # Normalizar rentabilidad (máx 20 puntos)
            max_rent = df_puntuado['rentabilidad'].max() if df_puntuado['rentabilidad'].max() > 0 else 1
            df_puntuado['ajuste_rentabilidad'] = 20 * (df_puntuado['rentabilidad'] / max_rent)
            df_puntuado['puntuacion'] = df_puntuado['puntuacion'] + df_puntuado['ajuste_rentabilidad']
        
        # Ajustar por experiencia del usuario si está disponible
        if 'experiencia' in parametros_usuario and parametros_usuario['experiencia']:
            experiencia = parametros_usuario['experiencia'].lower()
            
            # Definir dificultad de cultivos (simplificado)
            dificultad_cultivos = {
                'Maíz': 'Baja', 'Fríjol': 'Baja', 'Yuca': 'Baja', 'Plátano': 'Baja',
                'Arroz': 'Media', 'Papa': 'Media', 'Tomate de árbol': 'Media',
                'Café': 'Alta', 'Cacao': 'Alta', 'Gulupa': 'Alta', 'Arándano': 'Alta'
            }
            
            # Mapear nombres de cultivos a dificultad
            df_puntuado['dificultad'] = df_puntuado['nombre'].map(
                lambda x: dificultad_cultivos.get(x, 'Media')
            )
            
            # Ajustar puntuación según coincidencia de experiencia y dificultad
            ajuste_exp = {
                ('baja', 'Baja'): 10,    # Experiencia baja, cultivo fácil: buena coincidencia
                ('baja', 'Media'): 0,    # Experiencia baja, cultivo medio: neutral
                ('baja', 'Alta'): -10,   # Experiencia baja, cultivo difícil: mala coincidencia
                ('media', 'Baja'): 5,    # Experiencia media, cultivo fácil: coincidencia moderada
                ('media', 'Media'): 10,  # Experiencia media, cultivo medio: buena coincidencia
                ('media', 'Alta'): 0,    # Experiencia media, cultivo difícil: neutral
                ('alta', 'Baja'): 0,     # Experiencia alta, cultivo fácil: neutral
                ('alta', 'Media'): 5,    # Experiencia alta, cultivo medio: coincidencia moderada
                ('alta', 'Alta'): 10     # Experiencia alta, cultivo difícil: buena coincidencia
            }
            
            # Aplicar ajuste
            df_puntuado['ajuste_experiencia'] = df_puntuado['dificultad'].apply(
                lambda x: ajuste_exp.get((experiencia, x), 0)
            )
            
            df_puntuado['puntuacion'] = df_puntuado['puntuacion'] + df_puntuado['ajuste_experiencia']
        
        # Asegurar que la puntuación esté en un rango razonable
        df_puntuado['puntuacion'] = df_puntuado['puntuacion'].clip(0, 100)
        
        return df_puntuado
    
    def _preparar_resultados_detallados(self, df_recomendados):
        """
        Prepara resultados detallados para cada cultivo recomendado.
        """
        resultados = []
        
        for _, cultivo in df_recomendados.iterrows():
            id_cultivo = cultivo['id_cultivo']
            
            # Información básica del cultivo
            info_cultivo = {
                'id_cultivo': id_cultivo,
                'nombre': cultivo['nombre'],
                'tipo': cultivo['tipo'],
                'descripcion': cultivo['descripcion'],
                'ciclo_dias': cultivo['ciclo_dias'],
                'densidad_siembra': cultivo['densidad_siembra'],
                'puntuacion': round(cultivo['puntuacion'], 2),
                'condiciones_optimas': {
                    'temperatura': f"{cultivo['temp_min']} - {cultivo['temp_max']} °C",
                    'precipitacion': f"{cultivo['precipitacion_min']} - {cultivo['precipitacion_max']} mm/año",
                    'altitud': f"{cultivo['altitud_min']} - {cultivo['altitud_max']} msnm",
                    'tipo_suelo': cultivo['tipo_suelo'],
                    'ph_suelo': f"{cultivo['ph_min']} - {cultivo['ph_max']}"
                }
            }
            
            # Información de costos si está disponible
            if 'inversion_min' in cultivo:
                info_cultivo['costos'] = {
                    'inversion_inicial': f"{cultivo['inversion_min']:,.0f} - {cultivo['inversion_max']:,.0f} COP/ha",
                    'costo_operativo': f"{cultivo['costo_operativo']:,.0f} COP/ha",
                    'precio_interno': f"{cultivo['precio_interno']:,.0f} COP/kg" if pd.notna(cultivo['precio_interno']) else "No disponible",
                    'precio_exportacion': f"{cultivo['precio_export']:,.2f} USD/kg" if pd.notna(cultivo['precio_export']) else "No disponible",
                    'rentabilidad_estimada': f"{cultivo['rentabilidad']:.2f}%"
                }
            
            # Plagas y enfermedades
            plagas = self.plagas_df[self.plagas_df['id_cultivo'] == id_cultivo]
            if not plagas.empty:
                info_cultivo['plagas_enfermedades'] = []
                for _, plaga in plagas.iterrows():
                    info_cultivo['plagas_enfermedades'].append({
                        'nombre': plaga['nombre'],
                        'tipo': plaga['tipo'],
                        'severidad': plaga['severidad'],
                        'control': plaga['control']
                    })
            
            # Insumos recomendados
            insumos = self.insumos_cultivo_df[self.insumos_cultivo_df['id_cultivo'] == id_cultivo]
            if not insumos.empty:
                info_cultivo['insumos_recomendados'] = []
                for _, insumo in insumos.iterrows():
                    info_cultivo['insumos_recomendados'].append({
                        'nombre': insumo['nombre'],
                        'categoria': insumo['categoria'],
                        'cantidad_por_ha': f"{insumo['cantidad_por_ha']} {insumo['unidad_medida']}",
                        'etapa_aplicacion': insumo['etapa_aplicacion'],
                        'precio_promedio': f"{insumo['precio_promedio']:,.0f} COP/{insumo['unidad_medida']}"
                    })
            
            # Técnicas de cultivo
            tecnicas = self.tecnicas_cultivo_df[self.tecnicas_cultivo_df['id_cultivo'] == id_cultivo]
            if not tecnicas.empty:
                info_cultivo['tecnicas_recomendadas'] = []
                for _, tecnica in tecnicas.iterrows():
                    info_cultivo['tecnicas_recomendadas'].append({
                        'nombre': tecnica['nombre'],
                        'categoria': tecnica['categoria'],
                        'importancia': tecnica['importancia'],
                        'descripcion': tecnica['descripcion'],
                        'beneficios': tecnica['beneficios']
                    })
            
            # Certificaciones aplicables
            certificaciones = self.certificaciones_cultivo_df[self.certificaciones_cultivo_df['id_cultivo'] == id_cultivo]
            if not certificaciones.empty:
                info_cultivo['certificaciones_aplicables'] = []
                for _, cert in certificaciones.iterrows():
                    info_cultivo['certificaciones_aplicables'].append({
                        'nombre': cert['nombre'],
                        'entidad': cert['entidad'],
                        'mercado_objetivo': cert['mercado_objetivo'],
                        'premium_precio': f"{cert['premium_precio']}%"
                    })
            
            resultados.append(info_cultivo)
        
        return resultados
    
    def obtener_detalles_cultivo(self, id_cultivo):
        """
        Obtiene detalles completos de un cultivo específico.
        
        Args:
            id_cultivo (int): ID del cultivo
            
        Returns:
            dict: Diccionario con todos los detalles del cultivo
        """
        # Obtener información básica del cultivo
        cultivo_info = self.cultivos_df[self.cultivos_df['id_cultivo'] == id_cultivo]
        
        if cultivo_info.empty:
            return {"error": "Cultivo no encontrado"}
        
        # Crear dataframe con toda la información del cultivo
        cultivo_completo = pd.merge(cultivo_info, self.condiciones_df, on='id_cultivo')
        cultivo_completo = pd.merge(cultivo_completo, self.costos_df, on='id_cultivo', how='left')
        
        # Convertir a formato de resultado detallado
        df_recomendados = cultivo_completo.copy()
        df_recomendados['puntuacion'] = 100  # Puntuación máxima para detalles completos
        
        # Usar la misma función que para recomendaciones
        resultados = self._preparar_resultados_detallados(df_recomendados)
        
        if resultados:
            return resultados[0]
        else:
            return {"error": "No se pudieron obtener detalles completos"}
    
    def calcular_costos_implementacion(self, id_cultivo, area_hectareas=1):
        """
        Calcula los costos detallados de implementación para un cultivo específico.
        
        Args:
            id_cultivo (int): ID del cultivo
            area_hectareas (float): Área en hectáreas
            
        Returns:
            dict: Desglose detallado de costos
        """
        # Obtener información de costos
        costos_info = self.costos_df[self.costos_df['id_cultivo'] == id_cultivo]
        
        if costos_info.empty:
            return {"error": "Información de costos no disponible"}
        
        # Obtener insumos para este cultivo
        insumos = self.insumos_cultivo_df[self.insumos_cultivo_df['id_cultivo'] == id_cultivo]
        
        # Calcular costos
        inversion_min = costos_info['inversion_min'].values[0] * area_hectareas
        inversion_max = costos_info['inversion_max'].values[0] * area_hectareas
        costo_operativo = costos_info['costo_operativo'].values[0] * area_hectareas
        
        # Desglose de costos de insumos
        desglose_insumos = []
        total_insumos = 0
        
        for _, insumo in insumos.iterrows():
            cantidad = insumo['cantidad_por_ha'] * area_hectareas
            precio = insumo['precio_promedio']
            subtotal = cantidad * precio
            total_insumos += subtotal
            
            desglose_insumos.append({
                'nombre': insumo['nombre'],
                'categoria': insumo['categoria'],
                'cantidad': f"{cantidad} {insumo['unidad_medida']}",
                'precio_unitario': f"{precio:,.0f} COP/{insumo['unidad_medida']}",
                'subtotal': f"{subtotal:,.0f} COP"
            })
        
        # Estimar costos de mano de obra (simplificado)
        costo_mano_obra = costo_operativo * 0.4  # Estimación: 40% del costo operativo
        
        # Estimar otros costos
        otros_costos = costo_operativo * 0.1  # Estimación: 10% del costo operativo
        
        # Resultados
        resultado = {
            'area_hectareas': area_hectareas,
            'inversion_inicial': {
                'rango': f"{inversion_min:,.0f} - {inversion_max:,.0f} COP",
                'promedio': f"{(inversion_min + inversion_max) / 2:,.0f} COP"
            },
            'costos_operativos': {
                'total': f"{costo_operativo:,.0f} COP",
                'desglose': {
                    'insumos': {
                        'total': f"{total_insumos:,.0f} COP",
                        'detalle': desglose_insumos
                    },
                    'mano_obra': f"{costo_mano_obra:,.0f} COP",
                    'otros': f"{otros_costos:,.0f} COP"
                }
            },
            'estimacion_ingresos': {
                'precio_interno': f"{costos_info['precio_interno'].values[0]:,.0f} COP/kg" if pd.notna(costos_info['precio_interno'].values[0]) else "No disponible",
                'precio_exportacion': f"{costos_info['precio_export'].values[0]:,.2f} USD/kg" if pd.notna(costos_info['precio_export'].values[0]) else "No disponible",
                'rentabilidad_estimada': f"{costos_info['rentabilidad'].values[0]:.2f}%"
            }
        }
        
        return resultado
    
    def obtener_proveedores_insumos(self, id_cultivo):
        """
        Obtiene información sobre proveedores de insumos para un cultivo específico.
        
        Args:
            id_cultivo (int): ID del cultivo
            
        Returns:
            list: Lista de proveedores con sus insumos
        """
        # Obtener insumos para este cultivo
        insumos_cultivo = self.insumos_cultivo_df[self.insumos_cultivo_df['id_cultivo'] == id_cultivo]
        
        if insumos_cultivo.empty:
            return {"error": "Información de insumos no disponible"}
        
        # Obtener IDs de insumos
        ids_insumos = insumos_cultivo['id_insumo'].unique()
        
        # Consultar proveedores para estos insumos
        query = f"""
            SELECT p.*, pi.id_insumo, pi.precio, pi.disponibilidad, i.nombre as nombre_insumo, 
                   i.categoria as categoria_insumo, i.unidad_medida
            FROM proveedores p
            JOIN proveedor_insumo pi ON p.id_proveedor = pi.id_proveedor
            JOIN insumos i ON pi.id_insumo = i.id_insumo
            WHERE pi.id_insumo IN ({','.join(['?'] * len(ids_insumos))})
        """
        
        proveedores_df = pd.read_sql_query(query, self.conn, params=ids_insumos.tolist())
        
        # Organizar resultados por proveedor
        proveedores = {}
        
        for _, row in proveedores_df.iterrows():
            id_proveedor = row['id_proveedor']
            
            if id_proveedor not in proveedores:
                proveedores[id_proveedor] = {
                    'id_proveedor': id_proveedor,
                    'nombre': row['nombre'],
                    'tipo': row['tipo'],
                    'contacto': row['contacto'],
                    'ubicacion': row['ubicacion'],
                    'sitio_web': row['sitio_web'],
                    'telefono': row['telefono'],
                    'insumos': []
                }
            
            proveedores[id_proveedor]['insumos'].append({
                'id_insumo': row['id_insumo'],
                'nombre': row['nombre_insumo'],
                'categoria': row['categoria_insumo'],
                'precio': f"{row['precio']:,.0f} COP/{row['unidad_medida']}",
                'disponibilidad': row['disponibilidad']
            })
        
        return list(proveedores.values())
    
    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()
            print("Conexión a la base de datos cerrada.")


# Ejemplo de uso
if __name__ == "__main__":
    # Ruta a la base de datos
    db_path = "/home/ubuntu/proyecto_cultivos/data/db/cultivos.db"
    
    # Inicializar modelo
    modelo = ModeloRecomendacionCultivos(db_path)
    
    # Ejemplo de parámetros de usuario
    parametros_usuario = {
        'temperatura': 25.0,
        'precipitacion': 1500,
        'altitud': 1200,
        'tipo_suelo': 'Franco',
        'ph_suelo': 6.0,
        'presupuesto': 10000000,
        'experiencia': 'Media',
        'departamento': 'Antioquia',
        'preferencia_mercado': 'Local',
        'tiempo_disponible': 365
    }
    
    # Obtener recomendaciones
    recomendaciones = modelo.recomendar_cultivos(parametros_usuario)
    
    # Imprimir resultados
    print(f"Se encontraron {len(recomendaciones)} cultivos recomendados:")
    for i, rec in enumerate(recomendaciones[:3], 1):
        print(f"\n{i}. {rec['nombre']} (Puntuación: {rec['puntuacion']})")
        print(f"   Tipo: {rec['tipo']}")
        print(f"   Ciclo: {rec['ciclo_dias']} días")
        print(f"   Condiciones óptimas: {rec['condiciones_optimas']['temperatura']} | {rec['condiciones_optimas']['precipitacion']}")
    
    # Cerrar conexión
    modelo.cerrar_conexion()
