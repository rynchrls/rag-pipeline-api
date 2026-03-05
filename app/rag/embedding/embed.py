from sentence_transformers import SentenceTransformer
import time


class Embedding:
    model = ""

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    # ========================================
    # SECTION 4: QUERY PROCESSING
    # ========================================
    def process_user_query(self, query: str) -> list:
        """Embed a user query and return the embedding as a list."""

        cleaned_query = query.lower().strip()
        print(f"📝 Query: '{cleaned_query}'")

        start = time.perf_counter()

        query_embedding = self.model.encode([cleaned_query])

        end = time.perf_counter()
        elapsed = end - start

        print(f"🔢 Embedding shape: {query_embedding.shape}")
        print(f"⏱️ Embedding generated in {elapsed:.4f} seconds")

        return query_embedding[0].tolist()
