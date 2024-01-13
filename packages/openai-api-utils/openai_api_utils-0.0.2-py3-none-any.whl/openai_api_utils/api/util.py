import colorama
from colorama import Fore

def _colored(s, color: colorama.ansi.AnsiFore):
    return f"{color}{s}{Fore.RESET}"
def pprint_message(messages):

    print("#### Message conversation ###\n")
    for message in messages:
        # if message["role"] == "system":
        #     print(_colored(f"system: '{message['content']}'\n", Fore.RED))

        if message["role"] == "user":
            print(_colored(f"user: '{message['content']}'\n", Fore.GREEN))

        elif message["role"] == "assistant" and message.get("function_call"):
            print(_colored(f"[f]assistant: '{message['content']}' \n\t {message['function_call']}\n", Fore.BLUE))

        elif message["role"] == "assistant" and not message.get("function_call"):
            print(_colored(f"assistant: '{message['content']}'\n", Fore.CYAN))

        elif message["role"] == "tool":
            print(_colored(f"function ({message['name']}): {message['content']}\n", Fore.MAGENTA))

        elif message["role"] == "function":
            print(_colored(f"function({message['name']}): {message['content']}\n", Fore.RED))
        else:
            print(f"else: {message}")



def pprint_tools(tools):
    print("#### Tools Applied ###\n")
    for t in tools:
        print(_colored(str(t), Fore.YELLOW))


def pprint_raw_completion_response(completion):
    print(_colored("\t#### Raw Choices ###", Fore.YELLOW))
    print(_colored(f"\t{completion}", Fore.LIGHTYELLOW_EX))
    print()

def pprint_response_choices(choices):
    print(_colored("\t#### Response Choices ###", Fore.YELLOW))

    for i, ch in enumerate(choices):
        if ch.message.content:
            print(_colored(f"\t[{i+1}] {ch.message.role}: {ch.message.content}", Fore.LIGHTYELLOW_EX))
            if ch.message.function_call:
                print(_colored(f"\t[{i+1}] - {ch.message.function_call}: {ch.message.function_call}", Fore.LIGHTYELLOW_EX))
            if ch.message.tool_calls:
                print(_colored(f"\t[{i+1}] - {ch.message.tool_calls}: {ch.message.tool_calls}", Fore.LIGHTYELLOW_EX))
    print()

def pprint_assistant_message(m):
    print(_colored(f"assistant: '{m.content}'\n", Fore.CYAN))

