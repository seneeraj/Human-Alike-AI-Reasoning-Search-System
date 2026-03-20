from sentence_transformers import SentenceTransformer

model = None

def get_model():
    global model
    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

def get_embedding(texts):
    if isinstance(texts, str):
        texts = [texts]
    model = get_model()
    return model.encode(texts).tolist()