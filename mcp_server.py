import sys, json
from client import ContextWindowLostInMiddleReorderer

def main():
    engine = ContextWindowLostInMiddleReorderer()
    for line in sys.stdin:
        line = line.strip()
        if not line: continue
        try:
            req = json.loads(line)
            method = req.get("method")
            rid = req.get("id")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "reorder", "description": "Reorder documents.", "inputSchema": {"type": "object", "properties": {"documents": {"type": "array"}}, "required": ["documents"]}},
                        {"name": "format_prompt_context", "description": "Format context.", "inputSchema": {"type": "object", "properties": {"reordered_result": {"type": "object"}}, "required": ["reordered_result"]}},
                        {"name": "run_benchmark_reorderer", "description": "Run self-test.", "inputSchema": {"type": "object"}}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "reorder":
                    out = engine.reorder(args.get("documents", []))
                elif tname == "format_prompt_context":
                    out = engine.format_prompt_context(args.get("reordered_result", {}))
                elif tname == "run_benchmark_reorderer":
                    out = engine.run_benchmark_reorderer()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
