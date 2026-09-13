import ollama

from app.exceptions import ProviderConfigError


def _embeddings_from_response(response) -> list[list[float]]:
    embeddings = (
        response.get("embeddings")
        if isinstance(response, dict)
        else getattr(response, "embeddings", None)
    )
    if not embeddings:
        raise ProviderConfigError("Ollama embedding provider returned no vectors")
    return [list(vector) for vector in embeddings]


def _content_from_response(response) -> str:
    message = (
        response.get("message")
        if isinstance(response, dict)
        else getattr(response, "message", None)
    )
    if isinstance(message, dict):
        content = message.get("content")
    elif message is not None:
        content = getattr(message, "content", None)
    else:
        content = None
    if not content:
        raise ProviderConfigError("Ollama LLM provider returned an empty response")
    return content


class OllamaEmbeddingProvider:
    def __init__(self, model: str, host: str):
        self._model = model
        self._client = ollama.Client(host=host)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        try:
            response = self._client.embed(model=self._model, input=texts)
        except Exception as exc:
            raise ProviderConfigError(f"Ollama embedding request failed: {exc}") from exc
        return _embeddings_from_response(response)

    def embed_query(self, text: str) -> list[float]:
        vectors = self.embed_texts([text])
        if not vectors:
            raise ProviderConfigError(
                "Ollama embedding provider returned no vector for the query"
            )
        return vectors[0]


class OllamaLLMProvider:
    def __init__(self, model: str, host: str):
        self._model = model
        self._client = ollama.Client(host=host)

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self._client.chat(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                options={"temperature": 0.2},
            )
        except Exception as exc:
            raise ProviderConfigError(f"Ollama LLM request failed: {exc}") from exc
        return _content_from_response(response)
