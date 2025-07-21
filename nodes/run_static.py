import os
import re
import tempfile


def evaluate_kernel_style(code: str) -> dict:
    """Evaluate C code against the Linux kernel coding style."""
    lines = code.splitlines()
    violations = []

    for i, line in enumerate(lines):
        if line.startswith(" "):  # Space instead of tab
            violations.append(f"Line {i+1}: Uses space instead of tab")
        if len(line) > 80:
            print(f"[DEBUG] Line {i+1} triggered: Exceeds 80 characters")
            violations.append(f"Line {i+1}: Exceeds 80 characters")
        if "//" in line:
            violations.append(f"Line {i+1}: Uses C++ style comment")
        if re.search(r"[a-z][A-Z]", line):
            violations.append(f"Line {i+1}: camelCase found")
        if re.search(r"(if|for|while|else)\s*\(.*\)[^\{]", line) and not re.match(r".*\{", lines[i + 1] if i + 1 < len(lines) else ""):
            violations.append(f"Line {i+1}: Missing braces after control structure")
        if "*" in line and not re.search(r"\w+ \*\w+", line):
            violations.append(f"Line {i+1}: Pointer formatting issue")
        if re.match(r".*printk\s*\(.*\);", line):
            violations.append(f"Line {i+1}: Use of printk — check log level and format.")
        if re.search(r"\bmalloc\b|\bcalloc\b", line):
            violations.append(f"Line {i+1}: Use of malloc/calloc — kernel code should use kmalloc or kzalloc.")
        if "return 0;" not in code and "main" in code:
            violations.append("Missing return statement in main.")
        if "init_module" in code or "cleanup_module" in code:
            violations.append("Deprecated init_module/cleanup_module functions used — prefer module_init/module_exit.")
        if "TODO" in line or "FIXME" in line:
            violations.append(f"Line {i+1}: Found TODO/FIXME comment — incomplete implementation.")


    if "MODULE_LICENSE" not in code:
        violations.append("Missing MODULE_LICENSE macro")



    return {
        "style_score": max(0, 10 - len(violations) * 0.5),
        "violations": violations
    }


def run_static_node(state: dict) -> dict:
    """Run Linux kernel style-based static analysis."""
    groq_code = state.get("groq_code", "")
    local_code = state.get("local_code", "")

    print("[Style Check] Evaluating Groq code style...")
    groq_style = evaluate_kernel_style(groq_code)
    print("[Style Check] Evaluating llama code style...", groq_style)
    for v in groq_style["violations"]:
         print(" -", v)


   

    print("[Style Check] Evaluating Local code style...")
    local_style = evaluate_kernel_style(local_code)
    
    print("[Style Check] Evaluating gemma code style...", local_style)

    return {
        "static_result": {
            "groq": groq_style,
            "local": local_style
        },
        "groq_code": groq_code,
        "local_code": local_code
    }
