from .llm_openai import infer_issue_openai
from .llm_gemini import infer_issue_gemini

def infer_issue(subject: str, email_body: str, provider: str = "openai") -> dict:
    if provider == "openai":
        return infer_issue_openai(subject, email_body)
    elif provider == "gemini":
        return infer_issue_gemini(subject, email_body)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
