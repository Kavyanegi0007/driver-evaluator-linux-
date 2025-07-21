We are building linux evaluator system. I will be documenting by progress in this 

I am creating a Directed Acyclic LangGraph:
Directed: Each step flows in one direction (like → arrows)
Acyclic: No cycles or loops — the graph can't go backward or repeat steps

[prompt] 
   ↓
[generate_code]
   ↓
[save_code]
   ↓
[run_static]
   ↓
[eval_llm]
   ↓
[final_score]

generate_code
Uses both Groq and Ollama to generate Linux device driver code from the input prompt.

save_code
Saves each generated code snippet as a .c file in the generated/ directory.

run_static
Compiles both .c files using gcc and collects static analysis metrics like errors, warnings, and compile status.

eval_llm
Evaluates the quality of both generated code files using an LLM, based on structure, safety, and correctness.

final_score
Calculates a final score for each model using a weighted rubric and selects the better-performing model as the winner.


