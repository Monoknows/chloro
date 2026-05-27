# Save this temporarily as test_api.py and run it
from brain import ask_chloro
print("Sending test request to Chloro...")
response = ask_chloro("give me a life lesson")
print(f"Response received: {response}")