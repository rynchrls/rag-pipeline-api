from ollama import chat
from app.utils.build_message import build_messages
from app.config import settings
import time

# ========================================
# SECTION 7: RESPONSE GENERATION
# ========================================


class GenerateResponse:
    def __init__(self):
        self.model = settings.MODEL

    def generate(self, instruction_prompt: str, context: str, query: str) -> str:
        """
        Generate response using LLM (simulated for demo).

        This section demonstrates:
        - LLM integration (simulated)
        - Response formatting
        - Answer synthesis
        - Output structure
        """
        print("\n🤖 SECTION 6: RESPONSE GENERATION")
        print("=" * 50)

        start = time.perf_counter()

        # Simulate LLM processing time
        print("⏳ Processing with LLM...")

        messages = build_messages(
            instruction_prompt=instruction_prompt, context=context, query=query
        )

        response = chat(
            model=self.model,
            messages=messages,
            options={"temperature": 0},  # 🔥 important for RAG
        )
        print(
            f"✅ Generated response length: {len(response.message.content)} characters"
        )
        print("📋 Response includes: Policy references, key points, limitations")

        end = time.perf_counter()
        elapsed = end - start
        print(f"⏱️ Generate in {elapsed:.4f} seconds")

        return response.message.content
