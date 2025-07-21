# def compare_node(state: dict) -> dict:
#     """
#     Compute final winner from all evaluation sources: static and LLM.

#     Expects:
#     - state["static_result"]: dict with "groq_score" and "local_score"
#     - state["llm_scores"]: dict with "evaluation_text" containing "Groq Score", "Local Score", "Winner"

#     Returns:
#     - state["final_decision"]: {
#         "groq_final": float,
#         "local_final": float,
#         "winner": "groq" or "local",
#         "summary": str
#       }
#     """
#     static = state.get("static_result", {})
#     llm_text = state.get("llm_scores", {}).get("evaluation_text", "")

#     def extract_llm_scores(text):
#         import re
#         groq_score = re.search(r"Groq Score:\s*(\d+)/10", text)
#         local_score = re.search(r"Local Score:\s*(\d+)/10", text)
#         winner = re.search(r"Winner:\s*(Groq|Local)", text, re.IGNORECASE)

#         return {
#             "groq": int(groq_score.group(1)) if groq_score else 0,
#             "local": int(local_score.group(1)) if local_score else 0,
#             "winner": winner.group(1).lower() if winner else "unknown"
#         }

#     llm_result = extract_llm_scores(llm_text)

#     # Normalize static scores
#     static_groq = static.get("groq_score", 0)
#     static_local = static.get("local_score", 0)

#     # Combine using weighted average (e.g., 50% static, 50% LLM)
#     groq_final = 0.5 * static_groq + 0.5 * llm_result["groq"]
#     local_final = 0.5 * static_local + 0.5 * llm_result["local"]

#     final_winner = "groq" if groq_final > local_final else "local"

#     state["final_decision"] = {
#         "groq_final": round(groq_final, 2),
#         "local_final": round(local_final, 2),
#         "winner": final_winner,
#         "summary": f"Groq Final: {round(groq_final, 2)}/10\nLocal Final: {round(local_final, 2)}/10\nWinner: {final_winner.title()}"
#     }

#     return state
def compute_static_score(metrics: dict) -> float:
    base = 5
    score = base
    score -= metrics.get("warnings", 0) * 1
    score -= metrics.get("errors", 0) * 3

    if metrics.get("violations") is not None:
        score -= metrics["violations"] * 0.5
        print("Computing static score with metrics:", metrics)

    return round(score, 2)


def compare_node(state: dict) -> dict:
    static = state.get("static_result", {})
    llm_eval = state.get("llm_scores", {}).get("evaluation_text", "")

    # 1. Parse LLM scores
    def parse_llm_scores(text):
        import re
        groq = re.search(r"Groq Score:\s*(\d+)/10", text)
        local = re.search(r"Local Score:\s*(\d+)/10", text)
        winner = re.search(r"Winner:\s*(Groq|Local)", text, re.IGNORECASE)
        return (
            int(groq.group(1)) if groq else 0,
            int(local.group(1)) if local else 0,
            winner.group(1).lower() if winner else "unknown"
        )

    groq_llm, local_llm, _ = parse_llm_scores(llm_eval)

    # 2. Static analysis scores
    groq_static = compute_static_score(static.get("groq", {}))
    local_static = compute_static_score(static.get("local", {}))

    # 3. Weighted scoring
    final_groq = groq_static + (groq_llm * 2)
    final_local = local_static + (local_llm * 2)

    winner = "llama" if final_groq > final_local else "gemma"

    # 4. Return final decision
    state["final_decision"] = {
        "groq_final": round(final_groq, 2),
        "local_final": round(final_local, 2),
        "winner": winner,
        "summary": f"Llama: {round(final_groq, 2)}/30\n"
                   f"Gemma: {round(final_local, 2)}/30\n"
                   f"Winner: {winner.title()}"
    }

    return state
