from typing import Protocol


class EmbeddingProvider(Protocol):
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Return one embedding vector per input text."""

    def embed_query(self, text: str) -> list[float]:
        """Return a single embedding for a search query."""


class LLMProvider(Protocol):
    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        """Return a model completion for the given prompts."""
