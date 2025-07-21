import argparse
from graph_builder import build_graph
import json

def main():
    parser = argparse.ArgumentParser(description="LLM Linux Driver Evaluator")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt describing the Linux driver")
    args = parser.parse_args()

    graph = build_graph()

    result = graph.invoke({
        "prompt": args.prompt
    })

    # # Save report as JSON
    # with open("reports/report.json", "w") as f:
    #     json.dump(result["report"], f, indent=2)

    # print("Report saved to reports/report.json")
    # print("Result:", result["report"]["winner"])

if __name__ == "__main__":
    main()
