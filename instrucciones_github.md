# Instrucciones para Crear el Repositorio GitHub

A continuación se detallan los pasos para crear un repositorio en GitHub y subir el proyecto CultivosCO:

## 1. Crear una cuenta en GitHub (si aún no tienes una)

1. Ve a [GitHub](https://github.com/)
2. Haz clic en "Sign up" y sigue las instrucciones para crear una cuenta

## 2. Crear un nuevo repositorio

1. Inicia sesión en tu cuenta de GitHub
2. Haz clic en el botón "+" en la esquina superior derecha y selecciona "New repository"
3. Completa la información del repositorio:
   - **Repository name**: cultivosco
   - **Description**: Sistema de Recomendación de Cultivos para Colombia
   - **Visibility**: Public (o Private si prefieres mantenerlo privado)
   - **Initialize this repository with**: Marca la opción "Add a README file"
   - **Add .gitignore**: Python
   - **Choose a license**: MIT License
4. Haz clic en "Create repository"

## 3. Clonar el repositorio en tu computadora

1. En la página del repositorio, haz clic en el botón verde "Code"
2. Copia la URL del repositorio (por ejemplo, https://github.com/tu-usuario/cultivosco.git)
3. Abre una terminal en tu computadora
4. Navega hasta el directorio donde deseas clonar el repositorio
5. Ejecuta el siguiente comando:
   ```
   git clone https://github.com/tu-usuario/cultivosco.git
   cd cultivosco
   ```

## 4. Reemplazar los archivos iniciales con los del proyecto

1. Elimina el README.md inicial que se creó automáticamente
2. Copia todos los archivos y carpetas del proyecto CultivosCO a este directorio
3. Asegúrate de mantener la estructura de directorios tal como está en el proyecto original

## 5. Subir los archivos al repositorio

1. Añade todos los archivos al staging area:
   ```
   git add .
   ```
2. Realiza el commit inicial:
   ```
   git commit -m "Versión inicial del Sistema de Recomendación de Cultivos para Colombia"
   ```
3. Sube los cambios al repositorio remoto:
   ```
   git push origin main
   ```

## 6. Verificar el repositorio

1. Actualiza la página de tu repositorio en GitHub
2. Deberías ver todos los archivos y carpetas del proyecto
3. El README.md se mostrará automáticamente en la página principal del repositorio

## 7. Configurar GitHub Pages (opcional)

Si deseas crear una página web para el proyecto:

1. En la página del repositorio, ve a "Settings"
2. Navega a la sección "Pages" en el menú lateral
3. En "Source", selecciona "main" como rama y "/docs" como carpeta (si has incluido una carpeta docs con archivos HTML)
4. Haz clic en "Save"
5. Después de unos minutos, tu sitio estará disponible en https://tu-usuario.github.io/cultivosco/

## Notas importantes

- Asegúrate de no incluir archivos sensibles o confidenciales en el repositorio
- Si el proyecto es muy grande, considera usar Git LFS para archivos grandes
- Mantén actualizado el repositorio con nuevas mejoras o correcciones
- Considera añadir colaboradores si trabajas en equipo

## Recursos adicionales

- [Documentación oficial de GitHub](https://docs.github.com/)
- [Guía de Git](https://git-scm.com/book/en/v2)
- [GitHub Desktop](https://desktop.github.com/) (interfaz gráfica para Git)
