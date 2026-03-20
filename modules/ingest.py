from modules.embed import get_embedding
from modules.db import get_collection
import uuid

from modules.embed import get_embedding
from modules.db import get_collection
import uuid

def chunk_text(text, chunk_size=300):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks


def ingest_data(text, collection_name="human_db"):

    # 🔥 reset collection (correct way)
    collection = get_collection(collection_name, reset=True)

    chunks = chunk_text(text)
    embeddings = get_embedding(chunks)

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            embeddings=[embeddings[i]],
            ids=[str(i)]
        )

    return "PDF ingested successfully!"