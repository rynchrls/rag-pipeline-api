# service.py
from typing import List, Dict
from .strategies import SentenceStrategy, ParagraphStrategy, SemanticStrategy


class ChunkingService:
    def __init__(
        self,
        strategy: str,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        if strategy == "sentence":
            self.strategy = SentenceStrategy()
        elif strategy == "paragraph":
            self.strategy = ParagraphStrategy()
        elif strategy == "ai_semantic":
            self.strategy = SemanticStrategy()
        else:
            raise ValueError("Invalid strategy")

    # -------------------------
    # Apply size + overlap
    # -------------------------
    def _apply_windowing(self, segments: List[str]) -> List[str]:
        chunks = []
        current_chunk = ""
        current_length = 0

        for segment in segments:
            segment_length = len(segment)

            if current_length + segment_length <= self.chunk_size:
                current_chunk += " " + segment
                current_length += segment_length
            else:
                chunks.append(current_chunk.strip())

                # apply overlap
                overlap_text = current_chunk[-self.chunk_overlap :]
                current_chunk = overlap_text + " " + segment
                current_length = len(current_chunk)

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    # -------------------------
    # Public method
    # -------------------------
    def chunk_documents(self, documents: List[Dict]) -> List[Dict]:
        all_chunks = []

        for doc in documents:
            base_segments = self.strategy.split(doc["content"])
            sized_chunks = self._apply_windowing(base_segments)

            for index, chunk in enumerate(sized_chunks):
                all_chunks.append(
                    {
                        "chunk_id": f"{doc['id']}_chunk_{index}",
                        "document_id": doc["id"],
                        "title": doc["title"],
                        "content": chunk,
                    }
                )

        return all_chunks
