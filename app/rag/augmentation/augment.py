from typing import List, Dict, Tuple
import textwrap
import time


class Augmentation:
    def __init__(self):
        pass

    def augment(self, query_embedding: list):
        pass

    # ========================================
    # SECTION 6: CONTEXT AUGMENTATION
    # ========================================

    def augment_prompt_with_context(
        self,
        search_results: List[Dict],
        agent_name: str,
        *,
        max_context_chars: int = 12_000,
        max_sources: int = 8,
    ) -> Tuple[str, str]:
        """
        General-purpose RAG prompt augmentation.

        Returns:
        (prompt, context)

        - prompt: instructions + query + how to use context
        - context: assembled retrieved docs (bounded to max_context_chars)
        """

        print("\n📝 SECTION 5: CONTEXT AUGMENTATION")
        print("=" * 50)

        start = time.perf_counter()

        # 1) Normalize and pick top sources
        results = (search_results or [])[:max_sources]

        # 2) Build context blocks (trim per-source if needed)
        context_parts: List[str] = []
        used_titles: List[str] = []
        remaining = max_context_chars

        for i, r in enumerate(results, 1):
            meta = r.get("metadata") or {}
            title = str(meta.get("title") or meta.get("source") or f"Source {i}")
            content = (r.get("content") or "").strip()

            if not content:
                continue

            block = f"[{i}] {title}\n{content}".strip()

            # If we’re tight on space, trim the block
            if len(block) > remaining:
                # keep a useful slice rather than dropping entirely
                block = block[: max(0, remaining - 50)].rstrip() + "\n…(truncated)"
            if len(block) <= 20:
                # too small to be useful after trimming
                continue

            context_parts.append(block)
            used_titles.append(title)
            remaining -= len(block) + 2  # spacing
            if remaining <= 200:
                break

        context = "\n\n".join(context_parts)

        print(f"📄 Assembled context from {len(context_parts)} sources")
        print(f"📏 Context length: {len(context)} characters")

        # 3) Persona + behavior (general, reusable)
        agent_instructions = f"""
    You are "{agent_name}", a newly created AI assistant.

    Identity & tone:
    - Be helpful, clear, and direct.
    - If the user is vague, ask a concise follow-up question OR provide best-effort assumptions and label them.

    Grounding rules (important):
    - Use the provided CONTEXT as your primary source of truth.
    - If CONTEXT is missing or insufficient, say what is missing and answer using general knowledge cautiously.
    - Do not invent citations or pretend the context says something it doesn't.

    Answer style:
    - Prefer bullet points or short sections when it improves clarity.
    - Provide actionable steps when relevant.
    - When you use information from a specific source, reference it as [1], [2], etc.
    """.strip()

        rag_instructions = """
    Task:
    Answer the user's QUESTION using the CONTEXT. The CONTEXT may contain partial, conflicting, or noisy information.

    How to use context:
    - Extract the most relevant facts from CONTEXT and explain them in your own words.
    - If multiple sources disagree, mention the disagreement and choose the most supported option.
    - If you are unsure, state uncertainty and suggest what to check next.

    Output:
    - Start with the direct answer.
    - Then add supporting details (and cite sources as [#] when used).
    - End with any follow-up questions only if truly necessary.
    """.strip()

        instruction_prompt = textwrap.dedent(
            f"""
            {agent_instructions}

            {rag_instructions}

            CONTEXT:
            (See the CONTEXT section provided separately. Use [#] citations when referencing it.)
            """
        ).strip()

        print(f"📝 Prompt length: {len(instruction_prompt)} characters")
        print(f"🔗 Context sources: {used_titles}")

        end = time.perf_counter()
        elapsed = end - start
        print(f"⏱️ Augment in {elapsed:.4f} seconds")

        return instruction_prompt, context
