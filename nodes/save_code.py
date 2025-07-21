import os
import re

def strip_markdown(code: str) -> str:
    # Remove ```c or ``` and trailing ```
    return re.sub(r"^```[cC]?\s*|```$", "", code.strip(), flags=re.MULTILINE)

def save_code_node(state):
    os.makedirs("generated", exist_ok=True)
    groq_code = state.get("groq_code")
    local_code = state.get("local_code")

    #print("[DEBUG] groq_code:", repr(groq_code[:200]))  # Preview first 200 characters
    #print("[DEBUG] local_code:", repr(local_code[:200]))

    if not groq_code:
        print("[ERROR] groq_code is empty or missing.")
    if not local_code:
        print("[ERROR] local_code is empty or missing.")

    groq_path = "generated/char_driver_groq.c"
    local_path = "generated/char_driver_local.c"

    with open(groq_path, "w") as f:
        f.write(groq_code or "// No code generated.\n")
    with open(local_path, "w") as f:
        f.write(local_code or "// No code generated.\n")

    return {
        "groq_path": groq_path,
        "local_path": local_path,
        "groq_code": groq_code,
        "local_code": local_code
    }
