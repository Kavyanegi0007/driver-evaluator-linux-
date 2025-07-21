# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# def call_groq_eval(prompt: str) -> str:
#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "model": "llama3-70b-8192",
#         "messages": [
#             {
#                 "role": "system",
#                 "content": "You are a strict Linux kernel expert reviewing C code. Compare two implementations objectively."
#             },
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ]
#     }

#     response = requests.post(
#         "https://api.groq.com/openai/v1/chat/completions",
#         headers=headers,
#         json=payload
#     )
#     response.raise_for_status()
#     return response.json()["choices"][0]["message"]["content"]

# def evaluate_llm_node(state: dict) -> dict:
#     groq_code = state["groq_code"]
#     local_code = state["local_code"]
#     static = state.get("static_result", {})

#     prompt = f"""
# You are a Linux kernel C code reviewer.

# Compare two char device driver implementations written in C. Use the following criteria:
# - Correctness
# - API usage
# - Structure and formatting
# - Compilation errors/warnings
# - Clang-tidy violations
# - Best practices

# ### Static analysis summary:
# Groq: {static.get('groq')}
# Local: {static.get('local')}

# ### Code A (Groq):
# {groq_code}

# ### Code B (Gemini or Local):
# {local_code}

# Score both out of 10, choose a winner, and justify your reasoning.

# Return your response in the format:

# Groq Score: X/10  
# Local Score: Y/10  
# Winner: Groq / Local  
# Justification: <your evaluation>
# """

#     print("🧠 Calling Groq for evaluation...")
#     result_text = call_groq_eval(prompt)
#     print("🧠 Evaluation result:", result_text)

#     return { "report" : {
#         "llm_scores": {
#             "evaluation_text": result_text }
#         }
#     }

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Configure Groq
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def evaluate_llm_node(state: dict) -> dict:
    groq_code = state["groq_code"]
    local_code = state["local_code"]
    static = state.get("static_result", {})
    

    # Save the code to files
    os.makedirs("generated", exist_ok=True)
    groq_path = "generated/char_driver_groq.c"
    local_path = "generated/char_driver_local.c"

    with open(groq_path, "w") as f:
        f.write(groq_code)

    with open(local_path, "w") as f:
        f.write(local_code)

    # Build the evaluation prompt
    prompt = f"""
You are a Linux kernel C code reviewer.

Compare two char device driver implementations written in C. Use the following criteria:

1. **Correctness (25%)**: Functional accuracy, logic errors, edge case handling
2. **API Usage (20%)**: Proper kernel API calls, error handling, resource management
3. **Structure & Formatting (15%)**: Code organization, readability, Linux coding style compliance
4. **Compilation Issues (15%)**: Errors, warnings, potential build failures
5. **Static Analysis (15%)**: Clang-tidy violations, potential bugs, security issues
6. **Best Practices (10%)**: Memory safety, locking, performance considerations


### Static analysis summary:
Groq: {static.get('groq')}
Local: {static.get('local')}

### Code A (Groq):
{groq_code}

### Code B (Local):
{local_code}

Score both out of 10, choose a winner, and justify your reasoning.

Return your response in the format:


1. **Correctness: llama X/10, gemma Y/10**
2. **API Usage: llama X/10, gemma Y/10**    
3. **Structure & Formatting: llama X/10, gemma Y/10**
4. **Compilation Issues: llama X/10, gemma Y/10**
5. **Static Analysis: llama X/10, gemma Y/10**
6. **Best Practices : llama X/10, gemma Y/10**

Groq Score: X/10  
Local Score: Y/10  
Winner: Groq / Local  
Justification: <your evaluation>

Also make sure to replace Groq with llama and Local with gemma in your response.
"""

    print("Calling Groq...")
    try:
        groq_resp = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        result_code = groq_resp.choices[0].message.content
        print("Evaluation result:", result_code)
    except Exception as e:
        print(f"Groq failed: {e}")
        return

    return {
        "llm_scores": {
            "evaluation_text": result_code
        },
        "groq_path": groq_path,
        "local_path": local_path
        
        # "metrics": {
        #     "groq": groq_result.get("metrics", {}),
        #     "local": local_result.get("metrics", {})
        }
    
