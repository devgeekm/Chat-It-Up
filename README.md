<div align="right">
  <a href="README_es.md">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Flag_of_Spain.svg/1200px-Flag_of_Spain.svg.png" alt="Español" width="40">
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

**Motto**:

"Transform your YouTube videos into smart conversations."

## Description

**Chat It Up!** redefines conversational experiences: more than just chat, it’s an intelligent tool that extracts and organizes knowledge from your YouTube videos, documents, and audio files, providing precise answers and accessible summaries in an instant. With just one click, transform your files into enriching dialogues that save you time and connect you to knowledge intuitively and elegantly.

### 1. Business Idea Overview

The platform leverages artificial intelligence to process content in various formats (audio, YouTube videos, and PDF documents) and generates customized responses or summaries via an interactive chatbot. The main goal is to convert multimedia and textual content into accessible, understandable formats, ideal for professionals and students who need to review, summarize, or extract information without processing lengthy content.

### 2. Project Scope

**Project Objective**: To create an AI-based web application that allows users to upload multimedia content (audio files, PDF documents, and YouTube links) and receive summaries or answers via a chatbot.

### Features

- **File Upload and Storage**: Users can upload PDF documents, audio files, or YouTube links.
- **Transcription and Processing**:
  - Audio files are transcribed using **Whisper**.
  - PDF documents are processed with **PyPDF2** to extract text.
  - YouTube videos are downloaded with **yt-dlp** and processed to extract text.
- **Answer and Summary Generation**: Through the **Azure OpenAI API**, the chatbot analyzes user queries and provides responses based on previously processed content.
- **Chatbot Interface**: **Streamlit** facilitates user interaction with the chatbot, displaying results in real time and enabling easy file uploads.

### Project Limitations

- Content up to 30 minutes long (for audio and video).
- PDF documents up to 20 pages (to ensure reasonable processing times).
- Support for texts in English and Spanish in the initial phase.

### 3. Integration Tools and Technologies

1. **FastAPI**: Framework for building the web API.
2. **Streamlit**: For creating a user-friendly interface where users can interact with the chatbot and upload multimedia files.
3. **Azure Blob Storage**: Stores all files uploaded by users for processing, functioning as the primary database for storing and retrieving data within the RAG model, meeting high availability and efficiency standards.
4. **Python Backend**: Processes files, manages API interactions, and controls communication between the user and the chatbot.
5. **Whisper (Azure Speech)**: Used for transcribing audio to text, making audio and video content accessible for response generation.
6. **Azure OpenAI API**: GPT-4 is used to generate summaries, answer questions, and analyze text content.
7. **PyPDF2**: Allows PDF files to be read for direct text content extraction.
8. **Pydub**: Processes and manipulates downloaded audio to ensure it is in the proper format for transcription.
9. **yt-dlp**: Downloads audio from YouTube videos provided by the user for further processing.

### 4. Scalability Towards a Retrieval-Augmented Generation (RAG) Information Retrieval System

To scale this platform for more extensive and precise searches across multiple pieces of content, a **RAG** system can be implemented by leveraging **Azure Blob Storage** for file storage and information retrieval:

1. **Azure Blob Storage as Primary Database**: Using Blob Storage to store multimedia files and documents allows for quick and efficient retrieval, ideal for RAG processing.
2. **Azure Cognitive Search**: Create a search index on transcribed texts and PDF documents stored in Azure Blob Storage. This index will allow the OpenAI model to retrieve and use relevant information efficiently.
3. **Enhanced Answer Generation**: The chatbot will search Azure Cognitive Search’s index for the most relevant content and send it to the OpenAI model, enabling responses based on specific information relevant to the user’s query.

### 5. Compliance with Regulations Using Azure Compliance

When handling user data, it is crucial to comply with Azure’s privacy and security standards:

- **Data Encryption**: Azure Blob Storage encrypts data at rest and in transit. A secure (role-based) access system is implemented to limit who can view or modify files.
- **Regulatory Compliance**: Azure complies with various regulations (GDPR, HIPAA, ISO 27001) to ensure user data is managed per global and local regulations.
- **Auditing and Monitoring**: Use **Azure Monitor** to audit and monitor data usage and access, detecting any unauthorized access.
- **Data Retention Policy**: Configure storage and data deletion policies so that user-uploaded files are automatically deleted after a specified period.

### 6. Business Model

**Freemium Model**: Offer a free version with usage limits (such as processing a limited number of files per month) and a premium version allowing higher processing volumes.

- **Potential Customers**: Education companies, content creators, students, and professionals looking to extract and organize content information.
- **Monthly/Annual Subscriptions**: Provide a subscription model allowing unlimited document and audio processing.
- **Custom Plans for Organizations**: Companies requiring high-volume analysis can purchase custom plans with full access to advanced features.

## Requirements

- Python 3.8 or higher
- Azure AI Services
- `.env` file with Azure credentials
- `requirements.txt` file with necessary libraries

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/CodeGeekR/audio-summary-azure-ai.git
   cd audio-summary-azure-ai
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a .env file in the project's root directory with the following content:

   ```env
   AI_SERVICE_ENDPOINT=tu_endpoint_de_ai
   AI_SERVICE_KEY=tu_clave_de_ai
   AZURE_SPEECH_KEY=tu_clave_de_speech
   AZURE_SERVICE_REGION=tu_region_de_servicio
   AZURE_TRANSLATOR_KEY=tu_clave_traslator
   AZURE_TRANSLATOR_ENDPOINT=tu_endpoint_de_traslator
   AZURE_TRANSLATOR_LOCATION=tu_region_de_servicio
   ```

   Replace your_speech_key, your_service_region, your_ai_service_endpoint, and your_ai_service_key with your Azure credentials.

## Usage

1. **Run the script:**

   ```sh
   python3 run.py
   ```

2. **Interact with the API:**

   Use tools like Postman or cURL to interact with the API. For example, to transcribe a YouTube video, send a POST request to http://127.0.0.1:8000/api/v1/transcribe/ with the following JSON body:

   ```plaintext
   {
   "url": "your_video_url"
   }
   ```

3. View the results: Transcribed, translated, and improved files will be saved in Azure Blob Storage, where they can be retrieved and analyzed via the chatbot.

## Contributions

Contributions are welcome! Please open an issue or a pull request to discuss any changes you'd like to make.

## Licencia

This project is licensed under the MIT License. See the [LICENSE](https://es.wikipedia.org/wiki/Licencia_MIT) file for more details.

### Hackathon Participation

We are programming and artificial intelligence enthusiasts. As part of the **Microsoft Hackathon Innovation Challenge 2024**, we developed this application to meet the needs of users who want to transcribe or upload files to provide context and interact with an intelligent chatbot. This project aims to explore innovative solutions that enhance information accessibility through AI and simplify complex processes in an accessible and intuitive experience.

### Participants

This project was developed by a passionate team of programming and AI enthusiasts. For more information about each team member, visit their profiles:

- [Samuel Diaz](https://www.samuraidev.engineer)
  - **GitHub**: [github](https://github.com/CodeGeekR)
  - **LinkedIn**: [linkedin](https://www.linkedin.com/in/samuraidev/)
- [Rafael Castellanos](https://github.com/rafaelcg14)
  - **GitHub**: [github](https://github.com/rafaelcg14)
  - **LinkedIn**: [linkedin](https://www.linkedin.com/in/rafael-castellanos-guzman/)
