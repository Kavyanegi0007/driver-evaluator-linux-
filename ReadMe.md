#Linux Driver Evaluator
A modular Python project that generates, analyzes, and evaluates Linux character device drivers using LLMs like Groq's LLaMA and Gemma. The project runs style checks and computes static scores for generated code.

#Directed Acyclic LangGraph:
Directed: Each step flows in one direction (like → arrows)
Acyclic: No cycles or loops — the graph can't go backward or repeat steps

[prompt] 
   >
[generate_code]
   >
[save_code]
   >
[run_static]
   >
[eval_llm]
   >
[final_score]

1 generate_code
Uses both Groq and Ollama to generate Linux device driver code from the input prompt.

2 save_code
Saves each generated code snippet as a .c file in the generated/ directory.

3 run_static
Compiles both .c files using gcc and collects static analysis metrics like errors, warnings, and compile status.

4 eval_llm
Evaluates the quality of both generated code files using an LLM, based on structure, safety, and correctness.

5 final_score
Calculates a final score for each model using a weighted rubric and selects the better-performing model as the winner.

📦 Features
✅ Generate Linux character device driver code using Groq LLMs (LLaMA and Gemma)

🧪 Perform static analysis based on Linux kernel coding style

📊 Compute a static score based on warnings, errors, and violations

📝 Save generated code and reports locally

🧠 Designed to work with LangGraph for composable AI workflows

# Requirements
poetry install
Python 3.10+
Groq API key

# Run the evaluator with a prompt
poetry run python main.py --prompt "performs read and write operations"

linux-driver-evaluator/
├── main.py # Entry point for the app
├── .env # Stores API keys
├── generated/ # Stores generated C code
│ ├── char_driver_groq.c
│ └── char_driver_local.c
├── nodes/ # Modular evaluation nodes
│ ├── eval_llm.py # LLM code generation node
│ ├── run_static.py # Static style checker node
│ ├── final_score.py # Static score computation node
│ └── save_code.py # Saves code to disk
├── graph_builder.py # LangGraph node definitions
├── README.md # This file
├── poetry.lock
└── pyproject.toml # Poetry configuration


Developed with ❤️ by Kavya Negi. Contributions are welcome!
