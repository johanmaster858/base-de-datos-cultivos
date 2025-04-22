# Documentación Técnica - Sistema de Recomendación de Cultivos para Colombia

## 1. Introducción

Este documento describe la arquitectura, componentes y funcionamiento del Sistema de Recomendación de Cultivos para Colombia, una aplicación desarrollada para ayudar a agricultores y productores a seleccionar los cultivos más adecuados según sus condiciones específicas.

El sistema integra una base de datos completa de cultivos colombianos, un modelo de predicción y recomendación, y una interfaz de usuario interactiva que permite a los usuarios obtener recomendaciones personalizadas basadas en sus condiciones geográficas, recursos disponibles y preferencias.

## 2. Arquitectura del Sistema

El sistema sigue una arquitectura de tres capas:

### 2.1. Capa de Datos
- Base de datos SQLite con información detallada de cultivos colombianos
- Esquema relacional con 15 tablas interconectadas
- Datos sobre cultivos, condiciones óptimas, costos, plagas, insumos, etc.

### 2.2. Capa de Lógica de Negocio
- Modelo de recomendación implementado en Python
- Algoritmos de filtrado y puntuación de cultivos
- API REST para comunicación entre frontend y backend
- Módulos para cálculo de costos y análisis de compatibilidad

### 2.3. Capa de Presentación
- Interfaz web responsiva desarrollada con HTML, CSS y JavaScript
- Formulario de entrada de datos del usuario
- Visualización de recomendaciones y detalles de cultivos
- Catálogo completo de cultivos con filtros

## 3. Base de Datos

### 3.1. Esquema de la Base de Datos

La base de datos está estructurada en las siguientes tablas principales:

- `cultivos`: Información básica de cada cultivo
- `condiciones`: Condiciones óptimas para cada cultivo
- `costos`: Información económica y de rentabilidad
- `zonas_productoras`: Regiones donde se cultiva cada producto
- `plagas_enfermedades`: Problemas fitosanitarios comunes
- `insumos`: Requerimientos de insumos agrícolas
- `proveedores`: Información de proveedores de insumos
- `tecnicas_cultivo`: Prácticas recomendadas para cada cultivo
- `certificaciones`: Requisitos para certificaciones aplicables
- `mercados`: Información de mercados y canales de comercialización

### 3.2. Relaciones entre Tablas

El esquema implementa relaciones uno a muchos y muchos a muchos entre las entidades, permitiendo consultas complejas y recuperación eficiente de información relacionada.

## 4. Modelo de Recomendación

### 4.1. Algoritmo de Recomendación

El modelo de recomendación utiliza un enfoque de filtrado basado en contenido con las siguientes etapas:

1. **Filtrado por condiciones básicas**: Temperatura, precipitación, altitud
2. **Filtrado por condiciones secundarias**: Tipo de suelo, pH, drenaje
3. **Filtrado por recursos disponibles**: Área, presupuesto, tiempo
4. **Cálculo de puntuación**: Asignación de puntuaciones basadas en:
   - Compatibilidad con condiciones ambientales
   - Rentabilidad esperada
   - Dificultad de manejo
   - Preferencias del usuario

### 4.2. Cálculo de Costos

El sistema calcula los costos de implementación considerando:

- Inversión inicial por hectárea
- Costos operativos anuales
- Rendimiento esperado según condiciones
- Precios de mercado actualizados
- Área de cultivo especificada por el usuario

## 5. API REST

### 5.1. Endpoints Disponibles

- `GET /api/cultivos`: Retorna lista completa de cultivos
- `GET /api/cultivos/<id>`: Retorna detalles de un cultivo específico
- `POST /api/recomendaciones`: Recibe parámetros del usuario y retorna recomendaciones
- `GET /api/costos/<id>?area=X`: Calcula costos de implementación para un cultivo
- `GET /api/proveedores/<id>`: Retorna proveedores de insumos para un cultivo

### 5.2. Formato de Datos

Todas las respuestas de la API utilizan formato JSON con estructuras de datos consistentes.

## 6. Interfaz de Usuario

### 6.1. Componentes Principales

- **Formulario de Recomendación**: Dividido en secciones (ubicación, suelo, recursos, preferencias)
- **Visualización de Resultados**: Tarjetas con información resumida de cultivos recomendados
- **Detalles de Cultivo**: Modal con información detallada de cada cultivo
- **Catálogo de Cultivos**: Explorador con filtros por categoría, altitud y ciclo
- **Calculadora de Costos**: Herramienta para estimar costos según área

### 6.2. Tecnologías Frontend

- HTML5 para estructura
- CSS3 con Bootstrap para diseño responsivo
- JavaScript para interactividad
- Gráficos y visualizaciones con Bootstrap Icons

## 7. Despliegue

### 7.1. Requisitos del Sistema

- Python 3.8 o superior
- Bibliotecas: Flask, Flask-CORS, SQLite3, Scikit-learn, Pandas, NumPy
- Servidor web compatible con WSGI
- Navegador web moderno

### 7.2. Instrucciones de Instalación

1. Clonar el repositorio
2. Instalar dependencias: `pip install -r requirements.txt`
3. Inicializar la base de datos: `python init_db.py`
4. Iniciar el servidor: `python server.py`

## 8. Pruebas y Validación

### 8.1. Pruebas Realizadas

- Pruebas de recomendación con diferentes escenarios geográficos
- Validación de coherencia de recomendaciones
- Pruebas de cálculo de costos
- Pruebas de obtención de detalles de cultivos

### 8.2. Resultados de Validación

Las pruebas demostraron que el sistema genera recomendaciones coherentes para diferentes zonas geográficas de Colombia, incluyendo:
- Zona cafetera (altitud media, alta precipitación)
- Zona andina alta (baja temperatura, altitud elevada)
- Llanos orientales (alta temperatura, alta precipitación)

## 9. Limitaciones y Trabajo Futuro

### 9.1. Limitaciones Actuales

- Base de datos limitada a 36 cultivos principales
- No considera variaciones microclimáticas
- Datos de costos y precios requieren actualización periódica

### 9.2. Mejoras Futuras

- Integración con datos climáticos en tiempo real
- Implementación de aprendizaje automático para mejorar recomendaciones
- Expansión de la base de datos con más cultivos y variedades
- Desarrollo de aplicación móvil
- Integración con sistemas de información geográfica

## 10. Conclusiones

El Sistema de Recomendación de Cultivos para Colombia proporciona una herramienta valiosa para agricultores y productores, facilitando la toma de decisiones informadas sobre qué cultivos implementar según sus condiciones específicas. La combinación de una base de datos completa, un modelo de recomendación preciso y una interfaz de usuario intuitiva hace que el sistema sea accesible y útil para usuarios con diferentes niveles de experiencia agrícola.

---

## Apéndice A: Estructura de Directorios

```
proyecto_cultivos/
├── data/
│   ├── db/
│   │   └── cultivos.db
│   ├── schema.sql
│   └── seed_data.sql
├── docs/
│   ├── documentacion_tecnica.md
│   ├── manual_usuario.md
│   └── investigacion_datos_adicionales.md
├── src/
│   ├── frontend/
│   │   ├── index.html
│   │   ├── app.js
│   │   ├── styles.css
│   │   └── assets/
│   │       └── cultivos/
│   ├── modelo_recomendacion.py
│   ├── server.py
│   ├── generate_images.py
│   └── test_modelo.py
└── tests/
    ├── resultados_pruebas.json
    ├── detalles_cultivos.json
    ├── costos_implementacion.json
    └── validacion_recomendaciones.json
```

## Apéndice B: Referencias

1. Base de datos original de cultivos colombianos
2. UPRA - Metodología de Costos
3. ICA - Buenas Prácticas Agrícolas
4. Agronet - Planificación de costos y presupuestos
5. Agroexport - Guía de cultivos
