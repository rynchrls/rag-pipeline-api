# strategies.py
import nltk
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
from .base import BaseChunkingStrategy


nltk.download("punkt_tab")


# -------------------------
# Sentence Strategy
# -------------------------
class SentenceStrategy(BaseChunkingStrategy):
    def split(self, text: str) -> List[str]:
        return nltk.sent_tokenize(text)


# -------------------------
# Paragraph Strategy
# -------------------------
class ParagraphStrategy(BaseChunkingStrategy):
    def split(self, text: str) -> List[str]:
        return [p.strip() for p in text.split("\n\n") if p.strip()]


# -------------------------
# Semantic Strategy
# -------------------------
class SemanticStrategy(BaseChunkingStrategy):
    def __init__(self, threshold: float = 0.80, model="text-embedding-3-small"):
        self.client = OpenAI()
        self.threshold = threshold
        self.model = model

    def _embed(self, sentences: List[str]):
        response = self.client.embeddings.create(model=self.model, input=sentences)
        return [d.embedding for d in response.data]

    def split(self, text: str) -> List[str]:
        sentences = nltk.sent_tokenize(text)
        if len(sentences) <= 1:
            return sentences

        embeddings = self._embed(sentences)

        chunks = []
        current_chunk = [sentences[0]]

        for i in range(1, len(sentences)):
            sim = cosine_similarity([embeddings[i - 1]], [embeddings[i]])[0][0]

            if sim >= self.threshold:
                current_chunk.append(sentences[i])
            else:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentences[i]]

        chunks.append(" ".join(current_chunk))
        return chunks
