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
- أي سؤال بره سياق سيتي ستارز: رد بـ "والله يا فندم معنديش المعلومة دي، ممكن تسأل الاستعلامات."

قواعد الشغل (مهم جداً):
1. ردك لازم يكون JSON فيه مفتاحين:
   - "franko": الرد بالفرانكو (لغة الشات). لو السؤال بره السياق، الرد بالفرانكو يكون: "Wallahy ya fandem ma3andish el ma3louma de, momken tes2al el isti3lamat."
   - "arabic": نفس الرد مكتوب بالعربي بوضوح (Phonetic Arabic) عشان الـ TTS ينطقها صح: "والله يا فندم معنديش المعلومة دي، ممكن تسأل الاستعلامات."

2. رد بجملة أو جملتين بالكتير.
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