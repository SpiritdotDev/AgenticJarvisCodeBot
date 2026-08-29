import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions,call_function

JARVIS_BANNER = r"""
       __ ___     ____  _    __ _____ _____
      / //   |   / __ \| |  / //_  _// ___/
 __  / // /| |  / /_/ /| | / /  / /  \__ \ 
/ /_/ // ___ | / _, _/ | |/ / _/ /  ___/ / 
\____//_/  |_|/_/ |_|  |___/ /___/ /____/  
"""

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("API key not found")

client = genai.Client(api_key=api_key)

MAX_STEPS = 10


def main():
    print(JARVIS_BANNER)
    print("Hello sir.")
    print("Type 'exit' to quit.\n")

    # Built-in chat automatically tracks conversation history cleanly
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0,
        ),
    )

    while True:
        user_input = input(">>> ").strip()
        if user_input.lower() == "exit":
            print("Powering down.")
            print(JARVIS_BANNER)
            break
        if not user_input:
            continue

        response = chat.send_message(user_input)

        steps = 0
        while steps < MAX_STEPS:
            steps += 1

            if response.function_calls:
                function_call_parts = []
                for function_call in response.function_calls:
                    function_call_result = call_function(
                        function_call, verbose=True
                    )
                    part = function_call_result.parts[0]
                    function_call_parts.append(part)

                # Send function results back to the ongoing chat
                response = chat.send_message(function_call_parts)
            else:
                print(response.text)
                break
        else:
            print("Error: maximum number of iterations reached for this turn.")


if __name__ == "__main__":
    main()
