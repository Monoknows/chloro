import ollama;

def ask_chloro(question):
    response = ollama.chat(model ="qwen", messages=[{"role": "user", "content": question}])
    return response["message"]["content"]
