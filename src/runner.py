import json
import time
from datetime import datetime

# Reuse the chatbot function you built in Phase 2
from chatbot import ask_chatbot

TEST_FILE = "tests/test_cases.json"
OUTPUT_FILE = "results/raw_results.json"


def load_tests(path):
    """Read the test cases file and return them as a Python list."""
    with open(path, "r") as f:
        return json.load(f)


def run_tests(tests):
    """Send every test prompt to the chatbot and collect the answers."""
    results = []
    total = len(tests)

    for number, test in enumerate(tests, start=1):
        print(f"[{number}/{total}] Running {test['id']} ...")

        start = time.time()
        try:
            answer = ask_chatbot(test["prompt"])
            error = None
        except Exception as e:
            # If the API call fails, record the error and keep going
            answer = ""
            error = str(e)
        seconds = round(time.time() - start, 2)

        # Save the original test info plus what the chatbot said
        results.append({
            "id": test["id"],
            "category": test["category"],
            "severity": test["severity"],
            "prompt": test["prompt"],
            "must_not_contain": test["must_not_contain"],
            "must_contain_any": test["must_contain_any"],
            "answer": answer,
            "error": error,
            "response_seconds": seconds,
        })

        # Short pause so we don't send requests too fast
        time.sleep(0.5)

    return results


def save_results(results, path):
    """Write the results to a JSON file."""
    output = {
        "run_time": datetime.now().isoformat(timespec="seconds"),
        "total_tests": len(results),
        "results": results,
    }
    with open(path, "w") as f:
        json.dump(output, f, indent=2)


if __name__ == "__main__":
    tests = load_tests(TEST_FILE)
    print(f"Loaded {len(tests)} test cases.\n")

    results = run_tests(tests)
    save_results(results, OUTPUT_FILE)

    errors = sum(1 for r in results if r["error"])
    print(f"\nDone. Saved to {OUTPUT_FILE}")
    print(f"Tests with API errors: {errors}")