import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Configure Groq
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_groq_model(model_name: str, prompt: str) -> str:
    """Call a specific Groq LLM model (e.g., LLaMA or Gemma) to generate driver code."""
    try:
        response = groq_client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"{model_name} error: {e}")
        return f"// {model_name} failed to generate code."

def generate_code_node(state: dict) -> dict:
    """
    Generates two versions of Linux driver code from the prompt:
    - `groq_code`: using LLaMA (llama3-70b-8192)
    - `local_code`: using Gemma (gemma2-9b-it)
    """
    prompt = f"Write a Linux character device driver that {state['prompt']}."

    print("Calling Groq (LLaMA)...")
    llama_code = call_groq_model("llama3-70b-8192", prompt)

    print("Calling Groq (Gemma)...")
    gemma_code = call_groq_model("gemma2-9b-it", prompt)

    return {
        "groq_code": llama_code,
        "local_code": gemma_code  # you can rename these keys if needed
    }
