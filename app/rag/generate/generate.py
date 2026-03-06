from typing import Any, Iterator
import time

from ollama import Client as OllamaClient
from openai import OpenAI
from google import genai

from app.utils.build_message import build_messages
from app.config import settings


class GenerateResponse:
    def __init__(self):
        self.ollama_model = settings.OLLAMA_MODEL
        self.openai_model = settings.OPENAI_MODEL
        self.gemini_model = settings.GEMINI_MODEL

        # OpenAI hosted API
        self.openai_client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

        # Gemini hosted API
        self.gemini_client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

        # Ollama hosted API or remote Ollama server
        # Example cloud host: https://ollama.com
        # Example self-hosted remote host: https://my-ollama.company.com
        ollama_headers = {}
        if getattr(settings, "OLLAMA_API_KEY", None):
            ollama_headers["Authorization"] = f"Bearer {settings.OLLAMA_API_KEY}"

        self.ollama_client = OllamaClient(
            host=settings.OLLAMA_HOST,
            headers=ollama_headers or None,
        )

    def generate_ollama(
        self,
        instruction_prompt: str,
        context: str,
        query: str,
        prev_messages: list[dict[str, Any]],
    ):
        print("\n🤖 OLLAMA RESPONSE GENERATION")
        print("=" * 50)

        start = time.perf_counter()
        print("⏳ Processing with Ollama API...")

        messages = build_messages(
            instruction_prompt=instruction_prompt,
            context=context,
            query=query,
            prev_messages=prev_messages,
        )

        response = self.ollama_client.chat(
            model=self.ollama_model,
            messages=messages,
            options={"temperature": 0},
            stream=True,
        )

        print(f"⏱️ Streaming started in {time.perf_counter() - start:.4f} seconds")
        return response

    def generate_openai(
        self,
        instruction_prompt: str,
        context: str,
        query: str,
        prev_messages: list[dict[str, Any]],
    ):
        print("\n🤖 OPENAI RESPONSE GENERATION")
        print("=" * 50)

        start = time.perf_counter()
        print("⏳ Processing with OpenAI API...")

        messages = build_messages(
            instruction_prompt=instruction_prompt,
            context=context,
            query=query,
            prev_messages=prev_messages,
        )

        response = self.openai_client.chat.completions.create(
            model=self.openai_model,
            messages=messages,
            temperature=0,
            stream=True,
        )

        print(f"⏱️ Streaming started in {time.perf_counter() - start:.4f} seconds")
        return response

    def generate_gemini(
        self,
        instruction_prompt: str,
        context: str,
        query: str,
        prev_messages: list[dict[str, Any]],
    ):
        print("\n🤖 GEMINI RESPONSE GENERATION")
        print("=" * 50)

        start = time.perf_counter()
        print("⏳ Processing with Gemini API...")

        messages = build_messages(
            instruction_prompt=instruction_prompt,
            context=context,
            query=query,
            prev_messages=prev_messages,
        )

        gemini_contents = self._messages_to_gemini_contents(messages)

        response = self.gemini_client.models.generate_content_stream(
            model=self.gemini_model,
            contents=gemini_contents,
        )

        print(f"⏱️ Streaming started in {time.perf_counter() - start:.4f} seconds")
        return response

    def _messages_to_gemini_contents(
        self,
        messages: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Convert OpenAI/Ollama-style messages into Gemini contents format.
        Gemini SDK supports API-key auth via Client(api_key=...).
        """
        contents: list[dict[str, Any]] = []

        for msg in messages:
            role = msg.get("role", "user")
            content = str(msg.get("content", "")).strip()

            if not content:
                continue

            # Gemini generally expects user/model roles.
            # We fold system messages into user content with a prefix.
            if role == "system":
                contents.append(
                    {
                        "role": "user",
                        "parts": [{"text": f"[SYSTEM]\n{content}"}],
                    }
                )
            elif role == "assistant":
                contents.append(
                    {
                        "role": "model",
                        "parts": [{"text": content}],
                    }
                )
            else:
                contents.append(
                    {
                        "role": "user",
                        "parts": [{"text": content}],
                    }
                )

        return contents

    def generate(
        self,
        provider: str,
        instruction_prompt: str,
        context: str,
        query: str,
        prev_messages: list[dict[str, Any]],
    ):
        if provider == "ollama":
            return self.generate_ollama(
                instruction_prompt=instruction_prompt,
                context=context,
                query=query,
                prev_messages=prev_messages,
            )

        if provider == "openai":
            return self.generate_openai(
                instruction_prompt=instruction_prompt,
                context=context,
                query=query,
                prev_messages=prev_messages,
            )

        if provider == "gemini":
            return self.generate_gemini(
                instruction_prompt=instruction_prompt,
                context=context,
                query=query,
                prev_messages=prev_messages,
            )

        raise ValueError(f"Unsupported provider: {provider}")

    def stream_text(self, provider: str, response: Any) -> Iterator[str]:
        if provider == "ollama":
            for chunk in response:
                text = chunk.get("message", {}).get("content", "")
                if text:
                    yield text
            return

        if provider == "openai":
            for chunk in response:
                if chunk.choices:
                    text = chunk.choices[0].delta.content or ""
                    if text:
                        yield text
            return

        if provider == "gemini":
            for chunk in response:
                text = getattr(chunk, "text", "") or ""
                if text:
                    yield text
            return

        raise ValueError(f"Unsupported provider: {provider}")
