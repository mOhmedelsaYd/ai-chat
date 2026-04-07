import openai
from app.config import OPENAI_API_KEY

def get_client():
    return openai.OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
أنت مساعد ذكي بتتكلم باللهجة المصرية العامية فقط.
لا تستخدم اللغة الإنجليزية نهائيًا.
لا تستخدم اللغة العربية الفصحى.
خليك طبيعي جدًا كأنك إنسان مصري بيتكلم في الحياة اليومية.
ردودك تكون بسيطة، قصيرة، ومفهومة.
حتى لو المستخدم كتب أو قال كلام فيه إنجليزي، رد عليه بالمصري بس.
"""

def generate_response(transcript: str, history: list) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += history
    messages.append({"role": "user", "content": transcript})

    client = get_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=512,
        temperature=0.7,
    )
    return response.choices[0].message.content