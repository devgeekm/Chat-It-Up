<div align="right">
  <a href="README.md">
    <img src="https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg" alt="English" width="40">
  </a>
</div>

# Chat It Up!

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.75.0-009688?logo=fastapi&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-Blob%20Storage-0078D4?logo=microsoft-azure&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-AI%20Services-0078D4?logo=microsoft-azure&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-FF9900?logo=openai&logoColor=white)
![PyPDF2](https://img.shields.io/badge/PyPDF2-1.26.0-3776AB?logo=python&logoColor=white)
![Pydub](https://img.shields.io/badge/Pydub-0.25.1-4B8BBE?logo=python&logoColor=white)
![yt-dlp](https://img.shields.io/badge/yt--dlp-2021.12.1-FF0000?logo=youtube&logoColor=white)
![RAG](https://img.shields.io/badge/RAG-Retrieval--Augmented%20Generation-FF4500?logo=read-the-docs&logoColor=white)

**Lema**:

"Convierte tus videos de YouTube en conversaciones inteligentes."

## Descripción

**Chat It Up!** transforma la experiencia de conversación: más que un simple chat, es una herramienta inteligente que extrae y organiza conocimiento de tus videos de YouTube, documentos y archivos de audios, brindándote respuestas precisas y resúmenes accesibles en un instante. Con solo un clic, convierte tus archivos en diálogos enriquecedores que te ahorran tiempo y te acercan al conocimiento de manera intuitiva y elegante.

### 1. Descripción de la Idea de Negocio

La plataforma utiliza inteligencia artificial para procesar contenido en diferentes formatos (audios, videos de YouTube y documentos en PDF) y generar respuestas o resúmenes personalizados mediante un chatbot interactivo. El objetivo principal es convertir contenido multimedia y textual en formatos accesibles y comprensibles, ideal para profesionales y estudiantes que necesitan consultar, resumir o extraer información sin procesar contenido extenso.

### 2. Alcance del Proyecto

**Objetivo del Proyecto**: Crear una aplicación web basada en inteligencia artificial que permita a los usuarios cargar contenido multimedia (archivos de audio, documentos PDF y enlaces de YouTube) y recibir resúmenes o respuestas mediante un chatbot.

### Funcionalidades

- **Subida y almacenamiento de archivos**: El usuario puede subir documentos PDF, audios o enlaces de YouTube.
- **Transcripción y Procesamiento**:
  - Los audios se transcriben con **Whisper**.
  - Los documentos PDF se procesan con **PyPDF2** para extracción de texto.
  - Los audios de YouTube se descargan con **yt-dlp** y se procesan para extraer texto.
- **Generación de Respuestas y Resúmenes**: Mediante la **API de Azure OpenAI**, el chatbot analiza las consultas del usuario y proporciona respuestas basadas en el contenido previamente procesado.
- **Interfaz del Chatbot**: **Streamlit** facilita la interacción del usuario con el chatbot, mostrando resultados en tiempo real y permitiendo cargas de archivos fácilmente.

### Limitaciones del Alcance

- Contenidos de menos de 30 minutos (para audios y videos).
- Documentos PDF de menos de 20 páginas (para garantizar tiempos de procesamiento razonables).
- Soporte para textos en inglés y español en la fase inicial.

### 3. Herramientas y Tecnologías de Integración

1. **FastAPI**: Framework para construir la API web.
2. **Streamlit**: Para crear una interfaz de usuario amigable donde los usuarios puedan interactuar con el chatbot y cargar archivos multimedia.
3. **Azure Blob Storage**: Almacena todos los archivos que el usuario sube para procesamiento, funcionando como la base de datos principal para almacenar y recuperar datos en el modelo RAG, además de cumplir con estándares de alta disponibilidad y eficiencia.
4. **Backend en Python**: Procesa los archivos, controla las interacciones entre las API y gestiona la comunicación entre el usuario y el chatbot.
5. **Whisper (Azure Speech)**: Utilizado para transcribir el audio en texto, permitiendo que el contenido de audio y video sea accesible para la generación de respuestas.
6. **API de Azure OpenAI**: GPT-4 se utiliza para generar resúmenes, responder preguntas y analizar los textos.
7. **PyPDF2**: Permite la lectura de archivos PDF para extraer contenido textual directamente.
8. **Pydub**: Procesa y manipula audios descargados, asegurando que estén en un formato adecuado para transcripción.
9. **yt-dlp**: Descarga el audio de los videos de YouTube proporcionados por el usuario para su posterior procesamiento.

### 4. Escalabilidad hacia un Sistema de Recuperación de Información con RAG (Retrieval-Augmented Generation)

Para llevar esta plataforma a una escala mayor y permitir búsquedas precisas en múltiples contenidos, se puede implementar un sistema **RAG** aprovechando **Azure Blob Storage** para el almacenamiento de archivos y recuperación de información:

1. **Azure Blob Storage como Base de Datos Principal**: Usar Blob Storage para almacenar archivos multimedia y documentos permite una recuperación rápida y eficiente, ideal para el procesamiento RAG.
2. **Azure Cognitive Search**: Crear un índice de búsqueda sobre los textos transcritos y los documentos PDF almacenados en Azure Blob Storage. Este índice permitirá que el modelo de OpenAI recupere y utilice información relevante de manera eficiente.
3. **Generación de Respuestas Enriquecida**: El chatbot buscará en el índice de Azure Cognitive Search el contenido más relevante y lo enviará al modelo de OpenAI, permitiendo respuestas basadas en información específica a la consulta del usuario.

### 5. Cumplimiento de Normativas con Azure Compliance

Al manejar datos de los usuarios, es fundamental cumplir con los estándares de privacidad y seguridad de Azure:

- **Cifrado de Datos**: Azure Blob Storage cifra los datos en reposo y en tránsito. Implementa un sistema de acceso seguro (rol basado) para limitar quién puede ver o modificar los archivos.
- **Cumplimiento de Normativas**: Azure cumple con diversas normativas (GDPR, HIPAA, ISO 27001) que aseguran el manejo de datos de usuarios conforme a la regulación global y local.
- **Auditoría y Monitoreo**: Usar **Azure Monitor** para auditar y monitorear el uso y acceso a los datos, detectando posibles accesos no autorizados.
- **Política de Retención de Datos**: Configurar políticas de almacenamiento y eliminación de datos para que los archivos subidos por los usuarios se eliminen automáticamente después de un periodo de tiempo determinado.

### 6. Modelo Comercial

**Modelo Freemium**: Ofrecer una versión gratuita con límites de uso (como procesamiento de un número limitado de archivos por mes) y una versión premium que permita mayores volúmenes de procesamiento.

- **Clientes Potenciales**: Empresas de educación, creadores de contenido, estudiantes y profesionales que deseen extraer y organizar información de contenido.
- **Suscripciones Mensuales/Anuales**: Ofrecer un modelo de suscripción que permita procesar un número ilimitado de documentos y audios.
- **Planes Personalizados para Organizaciones**: Empresas que requieran análisis de gran volumen podrán adquirir planes personalizados con acceso completo a funciones avanzadas.

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
   python3 run.py
   ```

2. **Interactuar con la API:**

   Utiliza herramientas como Postman o cURL para interactuar con la API. Por ejemplo, para transcribir un video de YouTube, envía una solicitud POST a http://127.0.0.1:8000/api/v1/transcribe/ con el siguiente cuerpo JSON:

   ```plaintext
   {
   "url": "your_video_url"
   }
   ```

3. Ver los resultados:
   Los archivos transcritos, traducidos y mejorados se guardarán en Azure Blob Storage y estarán disponibles para su recuperación y análisis mediante el chatbot.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que te gustaría realizar.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](https://es.wikipedia.org/wiki/Licencia_MIT) para más detalles.

### Hackathon Participation

Somos entusiastas de la programación y la inteligencia artificial. Como parte del **Microsoft Hackathon Innovation Challenge 2024**, hemos desarrollado esta aplicación para atender las necesidades de usuarios que desean transcribir o cargar archivos para contextualizar e interactuar con un chatbot inteligente. Este proyecto busca explorar soluciones innovadoras que faciliten el acceso a la información mediante IA y simplifiquen procesos complejos en una experiencia accesible e intuitiva.

### Participantes

Este proyecto fue desarrollado por un equipo apasionado de entusiastas de la programación y la inteligencia artificial. Para más información sobre cada integrante, puedes visitar sus perfiles:

- [Samuel Diaz](https://www.samuraidev.engineer)
  - **GitHub**: [github.com](https://github.com/CodeGeekR)
  - **LinkedIn**: [linkedin](https://www.linkedin.com/in/samuraidev/)
- [Rafael Castellanos](https://github.com/rafaelcg14)
  - **GitHub**: [github.com](https://github.com/rafaelcg14)
  - **LinkedIn**: [linkedin](https://www.linkedin.com/in/rafael-castellanos-guzman/)
