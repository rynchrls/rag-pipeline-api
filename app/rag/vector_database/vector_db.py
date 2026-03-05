import chromadb
from typing import List, Dict
from pathlib import Path
import time

# ========================================
# SECTION 3: VECTOR DATABASE SETUP
# ========================================


class VectorDatabase:
    def __init__(self):
        # Cache: { resolved_path_str -> chromadb.Collection }
        self._cache: dict = {}

    def clean_metadata(self, value):
        """Ensure value is Chroma-safe."""
        if value is None:
            return ""
        if isinstance(value, (str, int, float, bool)):
            return value
        return str(value)

    def setup_vector_database(self, chunks: List[Dict], collection_path: str):
        """
        Persistent ChromaDB collection:
        - Upserts chunks (adds new, updates existing)
        - Skips invalid chunks
        - Deduplicates incoming chunk_ids (keeps the last one)
        """

        print("\n🗄️ SECTION 2: VECTOR DATABASE SETUP")
        print("=" * 50)

        persist_path = Path(collection_path)
        persist_path.mkdir(parents=True, exist_ok=True)

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

        before = collection.count()

        # ---- Build & validate incoming items ----
        # Deduplicate by chunk_id (if duplicates exist in the same batch, last wins)
        by_id: Dict[str, Dict] = {}
        for chunk in chunks or []:
            cid = chunk.get("chunk_id")
            content = chunk.get("content")

            # Basic validation
            if not cid or not isinstance(cid, str):
                continue
            if not content or not isinstance(content, str):
                continue

            by_id[cid] = chunk

        if not by_id:
            print("⚠️ No valid chunks to store (missing chunk_id/content).")
            print(f"📈 Collection count: {before}")
            return collection

        ids = list(by_id.keys())
        documents = [by_id[cid]["content"] for cid in ids]
        metadatas = [
            {
                "document_id": self.clean_metadata(by_id[cid].get("document_id")),
                "title": self.clean_metadata(by_id[cid].get("title")),
            }
            for cid in ids
        ]

        # ---- Upsert: add new + update existing ----
        collection.upsert(ids=ids, documents=documents, metadatas=metadatas)

        after = collection.count()
        print(f"✅ Upserted {len(ids)} chunks")
        print(f"📦 Count before: {before} → after: {after} (Δ {after - before})")

        return collection

    def get_collection(self, collection_path: str):
        """
        Get existing ChromaDB collection.
        """
        start = time.perf_counter()
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

        end = time.perf_counter()
        elapsed = end - start
        print(f"⏱️ Get Collection in {elapsed:.4f} seconds")
        return collection

    def fetch_collection(self, collection_path: str):
        """
        Fetch an existing ChromaDB collection with caching.

        - First call for a path: ~250-300ms (disk read, cold start)
        - Subsequent calls for the same path: <1ms (memory cache)
        - Returns None if path doesn't exist or collection not created yet.
        """
        start = time.perf_counter()

        persist_path = Path(collection_path)
        resolved = str(persist_path.resolve())

        # ── Guard: folder must exist ──────────────────────────────────
        if not persist_path.exists():
            print(f"⚠️ Collection path does not exist: {persist_path}")
            return None

        # ── Cache hit ─────────────────────────────────────────────────
        if resolved in self._cache:
            elapsed = (time.perf_counter() - start) * 1000
            print(f"⚡ Cache hit in {elapsed:.2f} ms")
            return self._cache[resolved]

        # ── Cache miss: connect and cache ─────────────────────────────
        try:
            client = chromadb.PersistentClient(path=resolved)
            collection = client.get_collection("rag_docs")
            self._cache[resolved] = collection
            elapsed = (time.perf_counter() - start) * 1000
            print(
                f"✅ Fetched collection in {elapsed:.2f} ms (cold — cached for next call)"
            )
            return collection
        except Exception:
            print(f"⚠️ Collection 'rag_docs' not found in: {persist_path}")
            return None
