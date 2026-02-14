import ollama


def embed_text(text: str):

    response = ollama.embeddings(
        model="nomic-embed-text",   # lightweight + fast
        prompt=text
    )

    return response["embedding"]
