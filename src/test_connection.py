import os
from dotenv import load_dotenv
from google import genai
import anthropic

load_dotenv()


def test_gemini():
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Devuelve solo la palabra 'Gemini OK' si me recibes.",
    )
    print(f"Gemini:    {response.text.strip()}")


def test_anthropic():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=16,
        messages=[
            {"role": "user", "content": "Devuelve solo la palabra 'Claude OK' si me recibes."}
        ],
    )
    print(f"Anthropic: {response.content[0].text.strip()}")


if __name__ == "__main__":
    test_gemini()
    test_anthropic()