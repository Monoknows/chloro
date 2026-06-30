import time
from brain import ask_chloro, CONVERSATION_HISTORY

def test_memory_retention():
    print("==================================================")
    print("         CHLORO MEMORY DIAGNOSTIC MATRIX          ")
    print("==================================================")
    
    # 1. Establish data point
    prompt1 = "Remember that my secret override keyword is 'Vortex-99'."
    print(f"🔹 Step 1 (Input): {prompt1}")
    resp1 = ask_chloro(prompt1)
    print(f"🧠 Chloro Response: {resp1}\n")
    
    time.sleep(1) # Brief cooling pause
    
    # 2. Query data point contextually
    prompt2 = "What was my secret override keyword?"
    print(f"🔹 Step 2 (Query): {prompt2}")
    resp2 = ask_chloro(prompt2)
    print(f"🧠 Chloro Response: {resp2}\n")
    
    # 3. Inspect History Array Buffer
    print("🔹 Step 3: Inspecting RAM buffer state...")
    print(f"📋 Current Buffer Size: {len(CONVERSATION_HISTORY)} items.")
    for idx, msg in enumerate(CONVERSATION_HISTORY):
        print(f"  [{idx}] {msg['role'].upper()}: {msg['content']}")
        
    print("==================================================")

if __name__ == "__main__":
    test_memory_retention()