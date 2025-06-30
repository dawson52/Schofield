from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

memory_file = "memory.json"
if os.path.exists(memory_file):
    with open(memory_file, "r") as f:
        memory = json.load(f)
else:
    memory = {}

def brain(signal):
    if signal == "status":
        return "Brain is online and functioning properly."
    elif signal == "motivate":
        return "Let’s get after it. No one’s stopping you today."
    elif signal == "stats":
        return f"You currently have {len(memory)} memory items stored."
    elif signal.startswith("remember:"):
        fact = signal.split("remember:")[1].strip()
        key = f"memory_{len(memory)+1}"
        memory[key] = fact
        with open(memory_file, "w") as f:
            json.dump(memory, f)
        return f"Got it. I’ll remember: {fact}"
    elif signal == "list":
        return memory if memory else "Memory is empty."
    elif signal == "clear":
        memory.clear()
        with open(memory_file, "w") as f:
            json.dump(memory, f)
        return "Memory wiped clean."
    else:
        return "Unknown command."

@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    signal = data.get("signal")
    response = brain(signal)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run()
