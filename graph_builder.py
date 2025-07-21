from langgraph.graph import StateGraph

# Import your node functions
from nodes.generate_code import generate_code_node
from nodes.save_code import save_code_node
from nodes.run_static import run_static_node
from nodes.eval_llm import evaluate_llm_node
from nodes.final_score import compare_node


def build_graph():
    builder = StateGraph(dict)

    # Step 1: Add all nodes to the graph
    builder.add_node("generate_code", generate_code_node)
    builder.add_node("save_code", save_code_node)
    builder.add_node("run_static", run_static_node)
    builder.add_node("evaluate_llm", evaluate_llm_node)
    builder.add_node("compare", compare_node)
    

    # Step 2: Define execution flow
    builder.set_entry_point("generate_code")
    builder.add_edge("generate_code", "save_code")
    #builder.set_finish_point("save_code")
    builder.add_edge("save_code", "run_static")
    builder.add_edge("run_static", "evaluate_llm")
    builder.add_edge("evaluate_llm", "compare")
    #builder.add_edge("compare", "output")  # or set compare as finish point

    # Step 3: Mark final node
    builder.set_finish_point("compare")

    # Compile the graph
    return builder.compile()
