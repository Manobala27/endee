import agent
import sys
import os
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class MockColor:
        def __getattr__(self, name): return ""
    Fore = Style = MockColor()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print(Style.BRIGHT + Fore.MAGENTA + "+" + "-"*58 + "+")
    print(Style.BRIGHT + Fore.MAGENTA + "|" + Fore.CYAN + "       AGENTIC AI: ADVANCED SMART TASK ASSISTANT        " + Fore.MAGENTA + "|")
    print(Style.BRIGHT + Fore.MAGENTA + "+" + "-"*58 + "+")
    print(Fore.WHITE + "  Conversational • Context-Aware • Priority-Based Memory")
    print(Fore.WHITE + "  Type 'help' for commands | 'exit' to quit\n")

def print_help():
    print(Fore.YELLOW + "\nAvailable Commands:")
    print(" - 'add task <task>'      (e.g., add task Study AI urgent)")
    print(" - 'remind me to <task>'  (e.g., remind me to call Mom)")
    print(" - 'show tasks'           (List everything in memory)")
    print(" - 'delete task <name>'   (Remove a specific task)")
    print(" - 'clear tasks'          (Wipe the memory)")
    print(" - 'what should I do?'    (Get a smart suggestion)")
    print(" - Just chat with me!     (Try 'Hi' or 'I feel tired')")

def main():
    clear_screen()
    print_header()
    
    while True:
        try:
            user_input = input(Style.BRIGHT + Fore.GREEN + "User > " + Style.RESET_ALL).strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit", "bye"]:
                print(Fore.CYAN + "\nAgent: Goodbye! I'll keep your tasks safe in memory.")
                break
                
            if user_input.lower() == "help":
                print_help()
                continue
                
            if user_input.lower() == "cls" or user_input.lower() == "clear":
                clear_screen()
                print_header()
                continue
            
            # Get AI response
            response = agent.agent_response(user_input)
            
            # Print with subtle indent
            print(Fore.CYAN + f"\nAI Assistant: {response}\n")
            
        except KeyboardInterrupt:
            print(Fore.CYAN + "\n\nAgent: Goodbye!")
            sys.exit()
        except Exception as e:
            print(Fore.RED + f"\nError: {e}")

if __name__ == "__main__":
    main()
