import pickle
import numpy as np

from app.retrieval.embeddings import embed_text

with open("app/data/catalog_clean_chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

vectors = []

for chunk in chunks:

    vec = embed_text(chunk["text"])

    vectors.append(vec)

vectors = np.array(vectors)

np.save("app/data/embeddings.npy", vectors)

print("embeddings built successfully")