import uuid
import re
import numpy as np
from typing import List, Tuple, Dict, Any

from app.infrastructure.embeddings import generate_embedding
from app.infrastructure.vector_store import collection


# ----------------------------
# Add Document
# ----------------------------

def add_document(text: str, metadata: dict):
    """
    Adds a document chunk to the vector database.
    """

    doc_id = str(uuid.uuid4())
    embedding = generate_embedding(text)

    collection.add(
        ids=[doc_id],
        documents=[text],
        metadatas=[metadata],
        embeddings=[embedding]
    )



def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))



# ----------------------------
# Vector Search
# ----------------------------

def search_documents(query: str, k: int = 8):

    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "embeddings"]
    )

    return results



# ----------------------------
# Hybrid Re-Ranking
# ----------------------------

def hybrid_rerank(query: str, results: dict, top_k: int = 4, lambda_param: float = 0.7):

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    embeddings = results.get("embeddings", [[]])[0]

    if not documents:
        return [], [], []

    query_embedding = generate_embedding(query)

    selected_docs = []
    selected_meta = []
    selected_scores = []

    candidate_indices = list(range(len(documents)))

    while len(selected_docs) < min(top_k, len(documents)):

        mmr_scores = []

        for idx in candidate_indices:
            doc_embedding = embeddings[idx]

            relevance = cosine_similarity(query_embedding, doc_embedding)

            diversity = 0
            if selected_docs:
                similarities = [
                    cosine_similarity(doc_embedding, embeddings[i])
                    for i in range(len(documents))
                    if documents[i] in selected_docs
                ]
                diversity = max(similarities) if similarities else 0

            mmr_score = lambda_param * relevance - (1 - lambda_param) * diversity

            mmr_scores.append((mmr_score, idx, relevance))

        mmr_scores.sort(reverse=True, key=lambda x: x[0])

        best_score, best_idx, relevance_score = mmr_scores[0]

        selected_docs.append(documents[best_idx])
        selected_meta.append(metadatas[best_idx])
        selected_scores.append(relevance_score)

        candidate_indices.remove(best_idx)

    return selected_docs, selected_meta, selected_scores

