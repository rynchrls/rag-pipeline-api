from typing import List, Dict, Any


def build_messages(
    instruction_prompt: str,
    context: str,
    query: str,
    prev_messages: list[dict[str, Any]],
) -> List[Dict]:
    """
    Build LLM chat messages for a general-purpose RAG agent.

    - Uses retrieved context as the knowledge source
    - Prevents hallucinations
    - Allows the agent to work in any domain
    """

    return [
        {"role": "system", "content": instruction_prompt.strip()},
        {"role": "system", "content": f"CONTEXT:\n{context.strip()}"},
        *prev_messages,
        {"role": "user", "content": query.strip()},
    ]
