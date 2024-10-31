from app.utils.file_utils import print_styled_message

def split_text(text: str, max_length: int) -> list:
    """
    Divide el texto en partes más pequeñas de longitud máxima `max_length`.
    """
    try:
        return [text[i:i + max_length] for i in range(0, len(text), max_length)]
    except Exception as e:
        print_styled_message(f"Error al dividir el texto: {str(e)}")
        raise

def split_text_gpt(text: str, max_tokens: int) -> list:
    """
    Divide el texto en fragmentos que no excedan el límite de tokens.
    """
    try:
        words = text.split()
        chunks = []
        current_chunk = []

        for word in words:
            if len(current_chunk) + len(word.split()) > max_tokens:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
            else:
                current_chunk.append(word)

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks
    except Exception as e:
        print_styled_message(f"Error al dividir el texto para GPT: {str(e)}")
        raise