import pickle
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi

from app.retrieval.embeddings import embed_text


with open("app/data/catalog_clean_chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

embeddings = np.load("app/data/embeddings.npy")


tokenized_docs = [
    chunk["text"].lower().split()
    for chunk in chunks
]

bm25 = BM25Okapi(tokenized_docs)


def search(query, top_k=5):

    query_embedding = embed_text(query)

    semantic_scores = cosine_similarity(
        [query_embedding],
        embeddings
    )[0]

    keyword_scores = bm25.get_scores(
        query.lower().split()
    )

    max_keyword = max(keyword_scores)

    if max_keyword > 0:
        keyword_scores = keyword_scores / max_keyword

    final_scores = (
        0.7 * semantic_scores +
        0.3 * keyword_scores
    )

    ranked_indices = np.argsort(final_scores)[::-1]

    results = []

    blocked_words = [
        "report",
        "profile",
        "interpretation"
    ]

    for idx in ranked_indices:

        chunk = chunks[idx]

        name = chunk["metadata"]["name"].lower()

        blocked = False

        for word in blocked_words:

            if word in name:
                blocked = True
                break

        if blocked:
            continue

        results.append(chunk)

        if len(results) >= top_k:
            break

    return results