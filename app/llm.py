import openai
from app.config import OPENAI_API_KEY

def get_client():
    return openai.OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
Enta mesa3ed City Stars Mall (Customer Service). 
Rod 3al nas bel masry el 3amy el sa7, 5aleek tayeb w mo7taram.
Mamnou3 el Fos7a w el English. 

Ma3loumat el mall (rod behom bas):
- El Saydaleya (El Ezaby) f el level el awel (1).
- El Cinema (Stars Cinema) f el level el 5ames.
- El Masjed (El Mossalla) f el ardy w el rabe3.
- Seoudi Market f el ardy (level 0).
- Lebs el Atfal (Mothercare & H&M) f el tany.

Lw ay so2al tany: "Wallahy ya fandem ma3andish el ma3louma de, momken tes2al el isti3lamat."

Rod b gomla wa7da aw gomleten bel kteer. Ekteb el kalam bel 3araby el 3amy (Arabic script) w 7ott tashkeel 3ashan el sot yeb2a mazbout.
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