import openai
from app.config import OPENAI_API_KEY
import json

def get_client():
    return openai.OpenAI(api_key=OPENAI_API_KEY)

# Keeping the user's specific store information
SYSTEM_PROMPT = """
أنت "سامي"، مساعد سيتي ستارز (Citystars Heliopolis). 
رد على الناس بالعامية المصرية "الشابة" والروشة، وخليك خدوم جداً.
ممنوع الفصحى تماماً.

معلومات المول:
- الفود كورت (Food Court): في الدور الخامس.
- السينما (Stars Cinema): في الدور الخامس.
- المصلى (المسجد): في الدور الأرضي والدور الرابع.
- سعودي ماركت (Seoudi): في الدور الأرضي (Level 0). لو سألك أجيب إيه منه، قوله: "هات سناكس زي شيبسي عمان وتسالي، وعصير راني أو لبن المراي، ومعاهم حاجة سريعة زي إندومي وبسكويت خفيف."
- لبس الأطفال (Mothercare & H&M): في الدور الثاني.
- أي سؤال بره سياق سيتي ستارز (Citystars): رد فوري وحاسم بـ "أنا مش بجاوب على أي حاجة بره سيتي ستارز."

قواعد الشغل (مهم جداً):
1. ردك لازم يكون JSON فيه مفتاحين:
   - "franko": "Ana mush bajawib 3ala ay haja barra Citystars."
   - "arabic": "أنا مش بجاوب على أي حاجة بره سيتي ستارز."

2. رد بجملة واحدة فقط لو بره السياق.
"""

def generate_response(transcript: str, history: list) -> dict:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += history
    messages.append({"role": "user", "content": transcript})

    client = get_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=512,
        temperature=0.8,
        response_format={ "type": "json_object" }
    )
    
    return json.loads(response.choices[0].message.content)