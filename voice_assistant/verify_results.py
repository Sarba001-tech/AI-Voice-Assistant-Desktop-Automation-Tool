from commands import VoiceAssistant
import sys

def test_commands():
    va = VoiceAssistant()
    
    results = []
    
    cmds = ["email", "open google", "open twitch"]
    for cmd in cmds:
        res = va.execute_command(cmd)
        results.append(f"CMD: {cmd} -> RES: {res}")
        
    with open("test_results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results))

if __name__ == "__main__":
    test_commands()
