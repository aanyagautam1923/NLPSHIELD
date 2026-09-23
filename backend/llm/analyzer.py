import os
import requests


def fallback_explanation(
    text,
    toxicity,
    threat,
    rag_context
):

    messages = []

    if toxicity["toxic"]:
        messages.append(
            "The toxicity model detected potentially toxic or abusive language."
        )
    else:
        messages.append(
            "The toxicity model did not detect toxic language."
        )

    if threat["threat"]:
        messages.append(
            f"The cyber-threat model detected potentially "
            f"{threat['category']} content."
        )
    else:
        messages.append(
            "The cyber-threat model did not detect a cyber-threat signal."
        )

    if rag_context:
        messages.append(
            "Relevant cybersecurity guidance was retrieved "
            "from the NLPShield knowledge base."
        )

    messages.append(
        "For safety, never share passwords or OTPs and verify "
        "unexpected requests through a trusted channel."
    )

    return " ".join(messages)


def ollama_explanation(
    text,
    toxicity,
    threat,
    rag_context
):

    url = os.getenv(
        "OLLAMA_URL",
        "http://localhost:11434"
    )

    model = os.getenv(
        "OLLAMA_MODEL",
        "qwen2.5:3b"
    )

    context = "\n\n".join(
        item["text"]
        for item in rag_context
    )

    prompt = f"""
You are NLPShield, a defensive cybersecurity
text-analysis assistant.

Analyze this message:

{text}

Toxicity result:
{toxicity}

Cyber threat result:
{threat}

Retrieved security context:
{context}

Give:
1. Short explanation
2. Main indicators
3. Safe advice

Do not provide instructions for attacking
systems or creating malware/phishing attacks.
"""

    try:

        response = requests.post(
            f"{url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            ""
        ).strip()

    except Exception:

        return None


def explain(
    text,
    toxicity,
    threat,
    rag_context
):

    llm_result = ollama_explanation(
        text,
        toxicity,
        threat,
        rag_context
    )

    if llm_result:
        return llm_result

    return fallback_explanation(
        text,
        toxicity,
        threat,
        rag_context
    )

