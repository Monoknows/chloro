import ollama

def ask_chloro(question):
    system_prompt = (
        "You are CHLORO, a helpful, friendly, and highly intelligent personal AI assistant. "
        "Never say you are Qwen or created by Alibaba. If asked for your name, always state "
        "that your name is CHLORO."
    )
    
    try:
        response = ollama.chat(
            model="qwen", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        )
        return response['message']['content']
    except Exception as e:
        return f"I can't access my brain right now. Error: {e}"