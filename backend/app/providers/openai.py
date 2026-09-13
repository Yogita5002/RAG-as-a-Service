from openai import OpenAI

from app.exceptions import ProviderConfigError


class OpenAIEmbeddingProvider:
    def __init__(self, api_key: str, model: str, base_url: str | None = None):
        if not api_key:
            raise ProviderConfigError("OPENAI_API_KEY is not configured")
        client_kwargs: dict[str, str] = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
        self._client = OpenAI(**client_kwargs)
        self._model = model

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        response = self._client.embeddings.create(model=self._model, input=texts)
        ordered = sorted(response.data, key=lambda item: item.index)
        return [item.embedding for item in ordered]

    def embed_query(self, text: str) -> list[float]:
        vectors = self.embed_texts([text])
        if not vectors:
            raise ProviderConfigError("Embedding provider returned no vector for the query")
        return vectors[0]


class OpenAILLMProvider:
    def __init__(self, api_key: str, model: str, base_url: str | None = None):
        if not api_key:
            raise ProviderConfigError("OPENAI_API_KEY is not configured")
        client_kwargs: dict[str, str] = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
        self._client = OpenAI(**client_kwargs)
        self._model = model

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        content = response.choices[0].message.content
        if content is None:
            raise ProviderConfigError("LLM provider returned an empty response")
        return content
