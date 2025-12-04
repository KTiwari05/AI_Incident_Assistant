def chunk_text(text: str, max_length: int = 500):
    chunks = []
    words = text.split()
    current = []

    for w in words:
        current.append(w)
        if len(" ".join(current)) >= max_length:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks
