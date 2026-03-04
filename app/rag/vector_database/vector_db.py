import chromadb
from typing import List, Dict
from pathlib import Path

# ========================================
# SECTION 3: VECTOR DATABASE SETUP
# ========================================


class VectorDatabase:
    def clean_metadata(self, value):
        """Ensure value is Chroma-safe."""
        if value is None:
            return ""
        if isinstance(value, (str, int, float, bool)):
            return value
        return str(value)

    def setup_vector_database(self, chunks: List[Dict], collection_path: str):
        """
        Set up persistent ChromaDB vector database and store document chunks.
        """

        print("\n🗄️ SECTION 2: VECTOR DATABASE SETUP")
        print("=" * 50)

        # ✅ Ensure persistent directory exists (root-level)
        persist_path = Path(collection_path)
        persist_path.mkdir(parents=True, exist_ok=True)

        # ✅ Use PersistentClient (KEY CHANGE)
        client = chromadb.PersistentClient(path=str(persist_path))

        # Create or get collection
        try:
            collection = client.create_collection(
                name="rag_docs",
                metadata={"hnsw:space": "cosine"},
            )
            print("🆕 Created new collection")
        except Exception:
            collection = client.get_collection("rag_docs")
            print("♻️ Using existing collection")

        print(f"🗄️ Collection: {collection.name}")
        print("📊 Similarity metric: cosine")

        # Prepare data
        ids = [chunk["chunk_id"] for chunk in chunks]
        documents = [chunk["content"] for chunk in chunks]
        metadatas = [
            {
                "document_id": self.clean_metadata(chunk.get("document_id")),
                "title": self.clean_metadata(chunk.get("title")),
            }
            for chunk in chunks
        ]

        # Add only if empty (simple guard)
        if collection.count() == 0:
            collection.add(ids=ids, documents=documents, metadatas=metadatas)
            print(f"✅ Stored {len(chunks)} chunks in vector database")
        else:
            print(f"✅ Collection already contains {collection.count()} chunks")

        print(f"📈 Collection count: {collection.count()}")

        return collection

    def get_collection(self, collection_path: str):
        """
        Get existing ChromaDB collection.
        """
        persist_path = Path(collection_path)
        client = chromadb.PersistentClient(path=str(persist_path))
        # Create or get collection
        try:
            collection = client.create_collection(
                name="rag_docs",
                metadata={"hnsw:space": "cosine"},
            )
            print("🆕 Created new collection")
        except Exception:
            collection = client.get_collection("rag_docs")
            print("♻️ Using existing collection")
        return collection
