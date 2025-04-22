# Diseño de Estructura de Base de Datos para Sistema de Recomendación de Cultivos

## Descripción General

Esta base de datos está diseñada para almacenar información completa sobre cultivos en Colombia, incluyendo sus características, requerimientos, costos, proveedores de insumos y técnicas de cultivo. El objetivo es proporcionar una base sólida para un sistema de recomendación que ayude a los agricultores a seleccionar los cultivos más adecuados según sus condiciones específicas y a obtener información detallada sobre su implementación.

## Diagrama Entidad-Relación

```
+----------------+       +-------------------+       +----------------+
| CULTIVOS       |       | CONDICIONES       |       | ZONAS          |
+----------------+       +-------------------+       +----------------+
| id_cultivo (PK)|<----->| id_condicion (PK) |       | id_zona (PK)   |
| nombre         |       | id_cultivo (FK)   |       | nombre         |
| descripcion    |       | temp_min          |       | departamento   |
| tipo           |       | temp_max          |       | altitud_min    |
| ciclo_dias     |       | precipitacion_min |       | altitud_max    |
| densidad_siembra|      | precipitacion_max |       | temp_promedio  |
| imagen         |       | tipo_suelo        |       | precipitacion  |
+----------------+       | ph_min            |       +----------------+
        |                | ph_max            |               |
        |                | altitud_min       |               |
        |                | altitud_max       |               |
        |                +-------------------+               |
        |                                                    |
        v                                                    v
+----------------+       +-------------------+       +----------------+
| COSTOS         |       | PLAGAS_ENFERMEDADES|      | CULTIVO_ZONA   |
+----------------+       +-------------------+       +----------------+
| id_costo (PK)  |       | id_plaga (PK)     |       | id_cultivo (FK)|
| id_cultivo (FK)|       | nombre            |       | id_zona (FK)   |
| inversion_min  |       | tipo              |       | rendimiento    |
| inversion_max  |       | descripcion       |       | rentabilidad   |
| costo_operativo|       | control           |       | popularidad    |
| precio_interno |       | imagen            |       +----------------+
| precio_export  |       +-------------------+
| rentabilidad   |               ^
| fecha_actualizacion|           |
+----------------+               |
        |                        |
        v                        |
+----------------+       +-------------------+
| INSUMOS        |       | CULTIVO_PLAGA     |
+----------------+       +-------------------+
| id_insumo (PK) |       | id_cultivo (FK)   |
| nombre         |       | id_plaga (FK)     |
| categoria      |       | severidad         |
| descripcion    |       | frecuencia        |
| unidad_medida  |       +-------------------+
| precio_promedio|
| fecha_actualizacion|
+----------------+
        |
        v
+----------------+       +-------------------+       +----------------+
| PROVEEDORES    |       | INSUMO_CULTIVO    |       | TECNICAS       |
+----------------+       +-------------------+       +----------------+
| id_proveedor (PK)|     | id_insumo (FK)    |       | id_tecnica (PK)|
| nombre         |       | id_cultivo (FK)   |       | nombre         |
| tipo           |       | cantidad_por_ha   |       | categoria      |
| contacto       |       | etapa_aplicacion  |       | descripcion    |
| ubicacion      |       | frecuencia        |       | dificultad     |
| sitio_web      |       +-------------------+       | beneficios     |
| telefono       |                                   +----------------+
+----------------+                                           |
        |                                                    |
        v                                                    v
+----------------+       +-------------------+       +----------------+
| PROVEEDOR_INSUMO|      | CERTIFICACIONES   |       | TECNICA_CULTIVO|
+----------------+       +-------------------+       +----------------+
| id_proveedor (FK)|     | id_certificacion (PK)|    | id_tecnica (FK)|
| id_insumo (FK)  |      | nombre            |       | id_cultivo (FK)|
| precio          |      | entidad           |       | importancia    |
| disponibilidad  |      | requisitos        |       | etapa_aplicacion|
+----------------+       | beneficios        |       +----------------+
                         | duracion          |
                         +-------------------+
                                 |
                                 v
                         +-------------------+
                         | CULTIVO_CERTIFICACION|
                         +-------------------+
                         | id_cultivo (FK)   |
                         | id_certificacion (FK)|
                         | mercado_objetivo  |
                         | premium_precio    |
                         +-------------------+
```

## Descripción de Tablas

### 1. CULTIVOS
Almacena la información básica de cada cultivo disponible en Colombia.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_cultivo | INTEGER | Identificador único del cultivo (PK) |
| nombre | VARCHAR(100) | Nombre común del cultivo |
| nombre_cientifico | VARCHAR(100) | Nombre científico del cultivo |
| descripcion | TEXT | Descripción general del cultivo |
| tipo | VARCHAR(50) | Categoría del cultivo (cereal, frutal, hortícola, etc.) |
| ciclo_dias | INTEGER | Duración del ciclo productivo en días |
| densidad_siembra | VARCHAR(100) | Densidad de siembra recomendada |
| imagen | VARCHAR(255) | URL o ruta de la imagen del cultivo |

### 2. CONDICIONES
Almacena los requerimientos agroecológicos de cada cultivo.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_condicion | INTEGER | Identificador único de la condición (PK) |
| id_cultivo | INTEGER | Referencia al cultivo (FK) |
| temp_min | DECIMAL(5,2) | Temperatura mínima óptima (°C) |
| temp_max | DECIMAL(5,2) | Temperatura máxima óptima (°C) |
| precipitacion_min | INTEGER | Precipitación mínima requerida (mm/año) |
| precipitacion_max | INTEGER | Precipitación máxima tolerada (mm/año) |
| tipo_suelo | VARCHAR(100) | Tipo de suelo recomendado |
| ph_min | DECIMAL(3,1) | pH mínimo del suelo |
| ph_max | DECIMAL(3,1) | pH máximo del suelo |
| altitud_min | INTEGER | Altitud mínima recomendada (msnm) |
| altitud_max | INTEGER | Altitud máxima recomendada (msnm) |

### 3. ZONAS
Almacena información sobre las zonas productoras en Colombia.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_zona | INTEGER | Identificador único de la zona (PK) |
| nombre | VARCHAR(100) | Nombre de la zona o región |
| departamento | VARCHAR(50) | Departamento al que pertenece |
| altitud_min | INTEGER | Altitud mínima de la zona (msnm) |
| altitud_max | INTEGER | Altitud máxima de la zona (msnm) |
| temp_promedio | DECIMAL(5,2) | Temperatura promedio anual (°C) |
| precipitacion | INTEGER | Precipitación promedio anual (mm) |

### 4. CULTIVO_ZONA
Relaciona cultivos con zonas productoras y almacena información específica.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_cultivo | INTEGER | Referencia al cultivo (FK) |
| id_zona | INTEGER | Referencia a la zona (FK) |
| rendimiento | DECIMAL(10,2) | Rendimiento promedio en la zona (t/ha) |
| rentabilidad | VARCHAR(20) | Nivel de rentabilidad (alta, media, baja) |
| popularidad | INTEGER | Nivel de popularidad del cultivo en la zona (1-10) |

### 5. COSTOS
Almacena información detallada sobre los costos asociados a cada cultivo.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_costo | INTEGER | Identificador único del registro de costo (PK) |
| id_cultivo | INTEGER | Referencia al cultivo (FK) |
| inversion_min | DECIMAL(15,2) | Inversión inicial mínima por hectárea (COP) |
| inversion_max | DECIMAL(15,2) | Inversión inicial máxima por hectárea (COP) |
| costo_operativo | DECIMAL(15,2) | Costo operativo por ciclo (COP/ha) |
| precio_interno | DECIMAL(15,2) | Precio promedio en mercado interno (COP/kg) |
| precio_export | DECIMAL(15,2) | Precio promedio de exportación (USD/kg) |
| rentabilidad | DECIMAL(5,2) | Porcentaje de rentabilidad estimada |
| fecha_actualizacion | DATE | Fecha de la última actualización de los datos |

### 6. PLAGAS_ENFERMEDADES
Almacena información sobre plagas y enfermedades que afectan a los cultivos.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_plaga | INTEGER | Identificador único de la plaga/enfermedad (PK) |
| nombre | VARCHAR(100) | Nombre común de la plaga o enfermedad |
| nombre_cientifico | VARCHAR(100) | Nombre científico |
| tipo | VARCHAR(50) | Tipo (insecto, hongo, bacteria, virus, etc.) |
| descripcion | TEXT | Descripción detallada |
| control | TEXT | Métodos de control recomendados |
| imagen | VARCHAR(255) | URL o ruta de la imagen |

### 7. CULTIVO_PLAGA
Relaciona cultivos con las plagas y enfermedades que los afectan.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_cultivo | INTEGER | Referencia al cultivo (FK) |
| id_plaga | INTEGER | Referencia a la plaga/enfermedad (FK) |
| severidad | VARCHAR(20) | Nivel de severidad (alta, media, baja) |
| frecuencia | VARCHAR(20) | Frecuencia de aparición (común, ocasional, rara) |

### 8. INSUMOS
Almacena información sobre insumos agrícolas.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_insumo | INTEGER | Identificador único del insumo (PK) |
| nombre | VARCHAR(100) | Nombre del insumo |
| categoria | VARCHAR(50) | Categoría (fertilizante, herbicida, fungicida, etc.) |
| descripcion | TEXT | Descripción detallada |
| unidad_medida | VARCHAR(20) | Unidad de medida (kg, l, etc.) |
| precio_promedio | DECIMAL(15,2) | Precio promedio (COP) |
| fecha_actualizacion | DATE | Fecha de la última actualización del precio |

### 9. INSUMO_CULTIVO
Relaciona insumos con cultivos y especifica su uso.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_insumo | INTEGER | Referencia al insumo (FK) |
| id_cultivo | INTEGER | Referencia al cultivo (FK) |
| cantidad_por_ha | DECIMAL(10,2) | Cantidad recomendada por hectárea |
| etapa_aplicacion | VARCHAR(50) | Etapa del cultivo para aplicación |
| frecuencia | VARCHAR(50) | Frecuencia de aplicación |

### 10. PROVEEDORES
Almacena información sobre proveedores de insumos agrícolas.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_proveedor | INTEGER | Identificador único del proveedor (PK) |
| nombre | VARCHAR(100) | Nombre del proveedor |
| tipo | VARCHAR(50) | Tipo de proveedor |
| contacto | VARCHAR(100) | Persona de contacto |
| ubicacion | VARCHAR(255) | Ubicación geográfica |
| sitio_web | VARCHAR(255) | Sitio web |
| telefono | VARCHAR(20) | Número de teléfono |

### 11. PROVEEDOR_INSUMO
Relaciona proveedores con los insumos que ofrecen.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_proveedor | INTEGER | Referencia al proveedor (FK) |
| id_insumo | INTEGER | Referencia al insumo (FK) |
| precio | DECIMAL(15,2) | Precio ofrecido (COP) |
| disponibilidad | VARCHAR(50) | Nivel de disponibilidad |

### 12. TECNICAS
Almacena información sobre técnicas de cultivo.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_tecnica | INTEGER | Identificador único de la técnica (PK) |
| nombre | VARCHAR(100) | Nombre de la técnica |
| categoria | VARCHAR(50) | Categoría (siembra, riego, control de plagas, etc.) |
| descripcion | TEXT | Descripción detallada |
| dificultad | VARCHAR(20) | Nivel de dificultad (alta, media, baja) |
| beneficios | TEXT | Beneficios de la técnica |

### 13. TECNICA_CULTIVO
Relaciona técnicas con cultivos específicos.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_tecnica | INTEGER | Referencia a la técnica (FK) |
| id_cultivo | INTEGER | Referencia al cultivo (FK) |
| importancia | VARCHAR(20) | Nivel de importancia (esencial, recomendada, opcional) |
| etapa_aplicacion | VARCHAR(50) | Etapa del cultivo para aplicación |

### 14. CERTIFICACIONES
Almacena información sobre certificaciones agrícolas.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_certificacion | INTEGER | Identificador único de la certificación (PK) |
| nombre | VARCHAR(100) | Nombre de la certificación |
| entidad | VARCHAR(100) | Entidad certificadora |
| requisitos | TEXT | Requisitos para obtener la certificación |
| beneficios | TEXT | Beneficios de la certificación |
| duracion | VARCHAR(50) | Duración de la validez |

### 15. CULTIVO_CERTIFICACION
Relaciona cultivos con certificaciones aplicables.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_cultivo | INTEGER | Referencia al cultivo (FK) |
| id_certificacion | INTEGER | Referencia a la certificación (FK) |
| mercado_objetivo | VARCHAR(100) | Mercado objetivo para productos certificados |
| premium_precio | DECIMAL(5,2) | Premio de precio estimado (%) |

## Consideraciones Adicionales

1. **Índices**: Se crearán índices en todas las claves primarias y foráneas para optimizar las consultas.

2. **Restricciones de Integridad**: Se implementarán restricciones de integridad referencial para mantener la consistencia de los datos.

3. **Escalabilidad**: La estructura permite agregar nuevas tablas o campos según sea necesario para ampliar la funcionalidad del sistema.

4. **Actualización**: Se incluyen campos de fecha de actualización en tablas críticas para mantener un registro de la vigencia de los datos.

5. **Normalización**: La estructura está normalizada para minimizar la redundancia y mejorar la integridad de los datos.

Esta estructura de base de datos proporcionará una base sólida para el desarrollo del sistema de recomendación de cultivos, permitiendo consultas complejas y análisis detallados para generar recomendaciones precisas y personalizadas para los usuarios.
