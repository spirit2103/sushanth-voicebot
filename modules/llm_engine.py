# llm_engine.py
import os
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- Normal Query (single response) ----------------
def query_groq(query, context):
    """
    Generate the full response from Groq LLM (non-streaming).
    """
    prompt = f"""
You are a helpful AI voicebot answering questions about Sushanth.
Answer for the questions in the humanized form.
strictly don't use the special charactors at anywhere.
strictly don't use the tables and headings.
Use this context from his resume:
{context}

Question: {query}
Answer:
"""
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    # Groq's streaming API returns 'delta' objects; if non-streaming, access content
    try:
        return response.choices[0].message["content"]
    except:
        # fallback for older response format
        return response.choices[0].text

# ---------------- Streaming Query ----------------
def query_groq_stream(query, context):
    """
    Generator function that yields text chunks as the model generates output.
    """
    prompt = f"""
You are a helpful AI voicebot answering questions about Sushanth.
Answer for the questions in the humanized form.
strictly don't use the special charactors at anywhere.
strictly don't use the tables and headings.
Use this context from his resume:
{context}

Question: {query}
Answer:
"""
    # Stream=True enables incremental text generation
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        stream=True  # streaming mode
    )

    # Yield each text delta chunk as it comes
    for chunk in completion:
        # Some chunks may be empty, so use `or ""`
        yield chunk.choices[0].delta.content or ""
