
from groq import Groq, AuthenticationError, RateLimitError, APIConnectionError
from config.settings import load_config

SYSTEM_PROMPT = """You are a specialized Banglish text converter for Bangladeshi users.

DEFINITION:
Banglish = Bengali language written in English/Roman script, mixed with actual English words.
This is exactly how Bangladeshis type in social media, WhatsApp, Messenger, etc.

YOUR TASK:
Convert the given Banglish text to the requested language (Bangla Unicode or English).

STRICT RULES:
1. Preserve original meaning, tone, and emotion exactly
2. Handle informal language, slang, and code-mixing naturally
3. For bangla target: Use proper Unicode Bengali script only
4. For english target: Write natural, grammatically correct English
5. Return ONLY the converted text — zero explanations, zero quotes, zero extra text

EXAMPLES:
Input: "ami aj office theke fire khub tired, help lagbe"
Bangla result:  "আমি আজ অফিস থেকে ফিরে খুব ক্লান্ত, সাহায্য দরকার"
English result: "I came back from the office very tired today, I need help"

Input: "bhai ki korcho, call daw ektu urgent"
Bangla result:  "ভাই কী করছ, একটু কল দাও আর্জেন্ট"
English result: "Bro what are you doing, give me a call urgently"
"""


def convert_banglish(text: str, target: str = "bangla") -> str:

    config  = load_config()
    api_key = config.get("api_key", "").strip()

    if not api_key:
        return "❌ Groq API Key not set! Right-click tray icon → Settings"

    if not text or not text.strip():
        return ""

    if target == "bangla":
        instruction = "বাংলা (Bengali Unicode script)"
    else:
        instruction = "English (natural, grammatically correct)"

    user_prompt = f"Convert this Banglish text to {instruction}:\n\n{text.strip()}"

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model=config.get("model", "llama-3.3-70b-versatile"),
            max_tokens=1000,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt},
            ]
        )

        return response.choices[0].message.content.strip()

    except AuthenticationError:
        return "❌ Invalid Groq API Key! Open Settings and check your key."
    except RateLimitError:
        return "❌ Rate limit reached. Wait a moment and try again."
    except APIConnectionError:
        return "❌ No internet connection."
    except Exception as e:
        return f"❌ Error: {str(e)[:80]}"
