def sanitize_prompt(prompt: str) -> str:
    prompt = prompt.replace("\n", " ").replace("\"", "").strip()
    return prompt[:500]
