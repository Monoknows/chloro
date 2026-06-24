import time
from datetime import datetime
# 🧠 Import Chloro's actual processing brain
from brain import ask_chloro

def run_brain_diagnostics():
    print("==================================================")
    print("      CHLORO CORE COGNITIVE DIAGNOSTIC            ")
    print("==================================================")

    # TEST 1: Basic Gateway Communication
    print("\n[DIAGNOSTIC 1]: Testing Gateway Latency & Response...")
    try:
        t0 = time.time()
        response1 = ask_chloro("System ping check. Confirm operational status.")
        latency = time.time() - t0
        print(f"🟢 [SUCCESS] Latency: {latency:.2f}s")
        print(f"🧠 CHLORO: \"{response1}\"")
    except Exception as e:
        print(f"🔴 [FAIL] Gateway unreachable: {e}")
        return

    # TEST 2: Active Working Memory Verification
    print("\n[DIAGNOSTIC 2]: Testing Rolling Context Window Memory...")
    try:
        # Step A: Feed her a specific parameter
        secret_code = "Alpha-99"
        print(f"📡 Sending Parameter: 'Remember that my security clearance code is {secret_code}.'")
        ask_chloro(f"Remember that my security clearance code is {secret_code}.")
        time.sleep(1) # Brief pause for thread cooling
        
        # Step B: Force her to look back into her history array
        print("📡 Querying Memory: 'What was my clearance code?'")
        response2 = ask_chloro("What was my clearance code?")
        
        if secret_code in response2:
            print("🟢 [SUCCESS] Context retention verified.")
            print(f"🧠 CHLORO: \"{response2}\"")
        else:
            print("🟡 [WARNING] Response received, but context validation failed.")
            print(f"🧠 CHLORO: \"{response2}\"")
            
    except Exception as e:
        print(f"🔴 [FAIL] Memory validation crashed: {e}")

    print("\n==================================================")
    print("             DIAGNOSTICS COMPLETE                 ")
    print("==================================================")

if __name__ == "__main__":
    run_brain_diagnostics()