from client import ContextWindowLostInMiddleReorderer
import json

def main():
    reorderer = ContextWindowLostInMiddleReorderer()
    res = reorderer.run_benchmark_reorderer()
    print("Context Window Lost In Middle Reorderer Benchmark Result:")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
