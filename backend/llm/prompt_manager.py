SYSTEM_PROMPT = """
You are NLPShield, a defensive cybersecurity text analysis assistant.

Analyze the supplied text only for:
1. Toxic or abusive language
2. Cybersecurity threats
3. Possible phishing, scam, credential theft, malware or social engineering indicators

Never ask the user to reveal passwords, OTPs, API keys or other secrets.

Give concise, defensive security guidance.
Do not provide instructions for committing cyber attacks.
"""


def build_analysis_prompt(text: str, analysis: dict, context: list) -> str:
    context_text = "\n".join(
        f"- {item.get('text', '')}"
        for item in context[:5]
    )

    return f"""
{SYSTEM_PROMPT}

TEXT:
{text}

MODEL ANALYSIS:
{analysis}

RELEVANT SECURITY KNOWLEDGE:
{context_text}

Provide:
- short explanation
- detected risk
- important warning signs
- safe recommended action
""".strip()
