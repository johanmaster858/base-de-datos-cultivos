# CultivosCO - Sistema de Recomendación de Cultivos para Colombia

![Logo CultivosCO](docs/branding/logo_with_text.png)

## Descripción

CultivosCO es un sistema completo de recomendación de cultivos para Colombia que ayuda a agricultores y productores a seleccionar los cultivos más adecuados según sus condiciones específicas. El sistema integra una base de datos detallada de cultivos colombianos, un modelo de predicción y recomendación, y una interfaz de usuario interactiva.

## Características

- **Base de datos ampliada**: Información detallada sobre 36 cultivos colombianos, incluyendo condiciones óptimas, costos, rentabilidad, plagas, técnicas de cultivo y proveedores de insumos.
- **Modelo de predicción**: Algoritmo que analiza las condiciones específicas del usuario y genera recomendaciones personalizadas.
- **Aplicación web interactiva**: Interfaz intuitiva con formulario de entrada, visualización de recomendaciones, catálogo de cultivos y calculadora de costos.
- **Documentación completa**: Documentación técnica, manual de usuario y resultados de pruebas.

## Estructura del Proyecto

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
│   ├── investigacion_datos_adicionales.md
│   └── branding/
│       ├── logo.png
│       ├── logo_with_text.png
│       ├── favicon.ico
│       └── manual_marca.md
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
│   ├── create_logo.py
│   └── test_modelo.py
└── tests/
    ├── resultados_pruebas.json
    ├── detalles_cultivos.json
    ├── costos_implementacion.json
    └── validacion_recomendaciones.json
```

## Requisitos

- Python 3.8 o superior
- Bibliotecas: Flask, Flask-CORS, SQLite3, Scikit-learn, Pandas, NumPy, Pillow
- Navegador web moderno

## Instalación

1. Clonar el repositorio:
   ```
   git clone https://github.com/tu-usuario/cultivosco.git
   cd cultivosco
   ```

2. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

3. Inicializar la base de datos:
   ```
   cd data
   sqlite3 db/cultivos.db < schema.sql
   sqlite3 db/cultivos.db < seed_data.sql
   cd ..
   ```

4. Generar imágenes de ejemplo para los cultivos:
   ```
   cd src
   python generate_images.py
   ```

## Uso

1. Iniciar el servidor:
   ```
   cd src
   python server.py
   ```

2. Abrir en el navegador:
   ```
   http://localhost:5000
   ```

3. Utilizar el formulario para ingresar datos específicos y obtener recomendaciones personalizadas de cultivos.

## Pruebas

Para ejecutar las pruebas del modelo de recomendación:

```
cd src
python test_modelo.py
```

Los resultados de las pruebas se guardarán en el directorio `tests/`.

## Documentación

- [Documentación Técnica](docs/documentacion_tecnica.md): Arquitectura, componentes y funcionamiento del sistema.
- [Manual de Usuario](docs/manual_usuario.md): Instrucciones paso a paso para utilizar la aplicación.
- [Manual de Marca](docs/branding/manual_marca.md): Directrices para el uso correcto de la identidad visual.

## Contribuir

1. Hacer un fork del repositorio
2. Crear una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Hacer commit de tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Hacer push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Para consultas o soporte:
- Email: soporte@cultivosco.co
- Web: www.cultivosco.co

---

© 2025 CultivosCO. Todos los derechos reservados.
