import time


class VectorSearch:
    def __init__(self):
        pass

    # ========================================
    # SECTION 5: VECTOR SEARCH
    # ========================================

    def search(self, collection, query_embedding, top_k: int = 4):
        """
        Search vector database for relevant document chunks.

        This section demonstrates:
        - Vector similarity search
        - Result ranking and filtering
        - Similarity scoring
        - Top-k result selection
        """
        print("\n🔍 SECTION 4: VECTOR SEARCH")
        print("=" * 50)

        start = time.perf_counter()

        # Perform vector search
        results = collection.query(
            query_embeddings=[list(query_embedding)],
            n_results=top_k,  # How many results are returned?
        )

        print(f"🎯 Searching for top {top_k} results")
        print(f"📊 Found {len(results['ids'][0])} relevant chunks")

        # Process and display results
        search_results = []
        for i, (doc_id, distance, content, metadata) in enumerate(
            zip(
                results["ids"][0],
                results["distances"][0],
                results["documents"][0],
                results["metadatas"][0],
            )
        ):
            similarity = 1 - distance  # Convert distance to similarity
            search_results.append(
                {
                    "id": doc_id,
                    "content": content,
                    "metadata": metadata,
                    "similarity": similarity,
                }
            )

            print(
                f"\n{i + 1}. {metadata['title']} (Document ID: {metadata['document_id']})"
            )
            print(f"   Similarity: {similarity:.3f}")
            print(f"   Content: {content[:100]}...")

        end = time.perf_counter()
        elapsed = end - start
        print(f"⏱️ Search in {elapsed:.4f} seconds")

        return search_results
