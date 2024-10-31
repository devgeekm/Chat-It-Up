# Audio to summary with Azure AI

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-AI%20Services-0078D4?logo=microsoft-azure&logoColor=white)
![TQDM](https://img.shields.io/badge/TQDM-4.62.3-4B8BBE?logo=python&logoColor=white)
![PyPDF2](https://img.shields.io/badge/PyPDF2-1.26.0-3776AB?logo=python&logoColor=white)
![Pydub](https://img.shields.io/badge/Pydub-0.25.1-4B8BBE?logo=python&logoColor=white)
![yt-dlp](https://img.shields.io/badge/yt--dlp-2021.12.1-FF0000?logo=youtube&logoColor=white)
![RAG](https://img.shields.io/badge/RAG-Retrieval--Augmented%20Generation-FF4500?logo=read-the-docs&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Database-00BFFF?logo=database&logoColor=white)

Este script es una herramienta avanzada que transforma datos de la web, YouTube, audios y documentos de texto en presentaciones de PowerPoint profesionales. Utilizando RAG y una base de datos ChromaDB, SlideGenius AI alimenta un modelo de lenguaje de última generación para generar contenido detallado y preciso, eliminando las alucinaciones y garantizando una experiencia de usuario excepcional.

## Descripción

permite transcribir archivos de audio y analizar archivos de texto utilizando los servicios de Azure AI. Puede procesar archivos de texto en formatos `.txt`, `.docx`, `.pdf` y `.doc`, así como archivos de audio en formatos `.mp3`, `.wav` y `.m4a`. Después de la transcripción o lectura del archivo, el usuario puede seleccionar varias opciones de análisis, como la traducción, la extracción de palabras clave, entidades, enlaces y resúmenes abstractivos.

### **¡Nueva Funcionalidad!** 🎉

Ahora puedes obtener audio directamente desde una URL de YouTube. Esta nueva característica te permite transcribir y analizar el contenido de videos de YouTube de manera rápida y sencilla. Incluso traducirlo a varios idiomas.

## Requisitos

- Python 3.8 o superior
- Azure AI Services
- Archivo `.env` con las credenciales de Azure
- Archivo `requirements.txt` con las librerías necesarias

## Instalación

1. **Clonar el repositorio:**

   ```sh
   git clone https://github.com/CodeGeekR/audio-summary-azure-ai.git
   cd audio-summary-azure-ai
   ```

2. **Crear y activar un entorno virtual:**

   ```sh
   python3 -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```

3. **Instalar las dependencias:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Configurar las variables de entorno:**

   Crear un archivo `.env` en el directorio raíz del proyecto con el siguiente contenido:

   ```env
   AI_SERVICE_ENDPOINT=tu_endpoint_de_ai
   AI_SERVICE_KEY=tu_clave_de_ai
   AZURE_SPEECH_KEY=tu_clave_de_speech
   AZURE_SERVICE_REGION=tu_region_de_servicio
   AZURE_TRANSLATOR_KEY=tu_clave_traslator
   AZURE_TRANSLATOR_ENDPOINT=tu_endpoint_de_traslator
   AZURE_TRANSLATOR_LOCATION=tu_region_de_servicio
   ```

   Reemplaza `tu_clave_de_speech`, `tu_region_de_servicio`, `tu_endpoint_de_ai` y `tu_clave_de_ai` con tus credenciales de Azure.

## Uso

1. **Ejecutar el script:**

   ```sh
   python3 main.py
   ```

2. **Seleccionar la fuente de entrada:**

   El script te pedirá que selecciones la fuente de entrada:

   ```plaintext
   Seleccione la fuente de entrada:
   ```

3. Enlace de YouTube
4. Archivo de audio (mp3, wav, m4a)
5. Archivo de texto (txt, doc, pdf)

   ```

   Ingresa el número de la opción seleccionada.

   ```

6. **Procesar archivos:**

   - Si seleccionas [`1`], el script te pedirá que ingreses el enlace de YouTube. El audio se descargará, se transcribirá y se guardará en la carpeta `audio`. Luego, el script procesará el archivo de texto y te mostrará los resultados.
   - Si seleccionas [`2`], el script transcribirá todos los archivos de audio en la carpeta `audio` y procesará los archivos de texto en la carpeta `reviews`. Luego, te mostrará los resultados en la carpeta `summary`.
   - Si seleccionas [`3`], el script procesará todos los archivos de texto en la carpeta `reviews` y te mostrará los resultados en la carpeta `summary`.

7. **Seleccionar opciones de análisis:**

   Después de procesar cada archivo, el script te pedirá que selecciones las opciones de análisis:

   ```plaintext
   Seleccione los resultados que desea visualizar (separados por comas):
   1. Palabras clave del documento
   2. Entidades
   3. Enlaces
   4. Resumen abstractivo
   ```

   Ingresa los números de las opciones seleccionadas, separados por comas.

## Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal.
- **Azure AI Services**: Servicios de inteligencia artificial para transcripción y análisis de texto.
- **TQDM**: Biblioteca para mostrar barras de progreso.
- **PyPDF2**: Biblioteca para leer archivos PDF.
- **Pydub**: Biblioteca para manipulación de audio.
- **yt-dlp**: Biblioteca para descargar audio de YouTube.
- **RAG**: Esta arquitectura combina un modelo de recuperación y un modelo de generación para generar respuestas a preguntas.
- **ChromaDB**: Base de datos de conocimiento que alimenta el modelo de lenguaje.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que te gustaría realizar.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](https://es.wikipedia.org/wiki/Licencia_MIT) para más detalles.
