import os
from groq import Groq, RateLimitError
from dotenv import load_dotenv
import time

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_response(prompt, retries=3, delay=5):
    attempt = 0
    while attempt < retries:
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            return response.choices[0].message.content
        except RateLimitError as e:
            attempt += 1
            if attempt == retries:
                return f"Error: Rate limit exceeded after {retries} attempts. {str(e)}"
            print(f"Rate limit hit, retrying in {delay} seconds... (Attempt {attempt}/{retries})")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
        except Exception as e:
            return f"Error: An unexpected error occurred: {str(e)}"