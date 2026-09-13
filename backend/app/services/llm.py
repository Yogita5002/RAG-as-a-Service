from app.providers.factory import get_llm_provider


def generate_answer(*, system_prompt: str, user_prompt: str) -> str:
    return get_llm_provider().generate(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )
