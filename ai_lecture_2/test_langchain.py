
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = "gemini-1.5-flash"

if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY not found.")
else:
    print(f"Testing LangChain with model {MODEL_NAME}...")
    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, google_api_key=GOOGLE_API_KEY)
    try:
        res = llm.invoke("Hi, tell me one word.")
        print(f"Response: {res.content}")
    except Exception as e:
        print(f"Error: {e}")
