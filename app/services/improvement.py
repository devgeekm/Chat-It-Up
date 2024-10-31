from openai import AzureOpenAI
from app.utils.file_utils import print_styled_message
from app.utils.text_utils import split_text_gpt

def improve_transcription(text: str, ai_client: AzureOpenAI, language: str = None) -> str:
    """
    Mejora el texto completo utilizando el modelo GPT-3.5-turbo-instruct de Azure OpenAI.
    """
    if not text:
        raise ValueError("El texto de entrada está vacío")

    max_tokens = 1000  # Límite de tokens por fragmento
    text_chunks = split_text_gpt(text, max_tokens)

    # Definir el prompt según el idioma
    if language == 'es':
        prompt = (
            "Actúa como un especialista en optimización de textos en español. "
            "Cuando te proporcione contenido de texto de diversas fuentes, analízalo y mejóralo de la siguiente manera:\n"
            "1. Primero, identifica el tema principal, estilo de escritura y nivel técnico del contenido\n"
            "2. Elimina anuncios, palabras de relleno, marcas de tiempo y contenido fuera de tema\n"
            "3. Organiza los puntos clave usando formato apropiado (viñetas, números, párrafos)\n"
            "4. Preserva la terminología especializada y acrónimos, asegurando su uso correcto\n"
            "5. Estandariza valores numéricos y ecuaciones en notación apropiada\n"
            "6. Corrige gramática, ortografía y puntuación manteniendo la voz del autor\n"
            "7. Estructura el contenido con encabezados y secciones claras donde sea apropiado\n"
            "8. Mantén toda la precisión técnica e información esencial\n"
            "9. Mantén el texto en español\n"
            "10. Finaliza con una breve verificación de calidad\n"
            "Mejora el siguiente texto:\n\n"
        )
    else:
        prompt = (
            "I want you to act as a text optimization specialist. "
            "When I provide you with raw text content from various sources, analyze it and improve it in the following structured way:\n"
            "1. First, identify the main topic, writing style, and technical level of the content\n"
            "2. Remove all advertisements, filler words, timestamps, and off-topic content\n"
            "3. Organize the key points using appropriate formatting (bullets, numbers, paragraphs)\n"
            "4. Preserve specialized terminology and acronyms while ensuring they're used correctly\n"
            "5. Standardize numerical values and equations into proper notation\n"
            "6. Fix grammar, spelling, and punctuation while maintaining the author's voice\n"
            "7. Structure the content with clear headings and sections where appropriate\n"
            "8. Maintain all technical accuracy and essential information\n"
            "9. Keep the text in its original language\n"
            "10. End with a brief quality check\n"
            "Improve the following text:\n\n"
        )

    improved_texts = []

    print_styled_message("Mejorando la transcripción...")

    for idx, chunk in enumerate(text_chunks, 1):
        try:
            response = ai_client.completions.create(
                model="gpt-35-turbo-instruct",
                prompt=f"{prompt}{chunk}",
                temperature=0,
                max_tokens=max_tokens,
                top_p=0.9,  # Ajuste del parámetro top_p para mejorar la coherencia
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )
            improved_text = response.choices[0].text.strip()
            improved_texts.append(improved_text)
            print_styled_message(f"Fragmento {idx}/{len(text_chunks)} mejorado.")
        except Exception as e:
            print_styled_message(f"Error al mejorar el texto: {str(e)}")
            raise

    print_styled_message("Mejora de transcripción completada.")

    return ' '.join(improved_texts)