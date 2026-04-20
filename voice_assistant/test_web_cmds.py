from commands import VoiceAssistant
import sys

def test_commands():
    va = VoiceAssistant()
    
    test_cases = [
        "open youtube",
        "email",
        "open email",
        "open google",
        "open twitch",
        "open unknownwebsite123"
    ]
    
    print("Running tests...")
    for cmd in test_cases:
        print(f"\nCommand: '{cmd}'")
        try:
            result = va.execute_command(cmd)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_commands()
