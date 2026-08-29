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
    print("Type 'exit' to quit.")

    while True:
        user_input = input(">>> ").strip()
        if user_input.lower() == "exit":
            print("Exiting REPL.")
            break

        if not user_input:
            continue

        # Initialize conversation messages for this turn
        messages = [
            types.Content(
                role="user", parts=[types.Part.from_text(text=user_input)]
            )
        ]

        steps = 0
        while steps < MAX_STEPS:
            steps += 1

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                    temperature=0,
                ),
            )

            # Check if the model made any function calls
            if response.function_calls:
                # Add the model's tool call response to history
                for candidate in response.candidates:
                    messages.append(candidate.content)

                # Execute calls and collect function results
                function_call_parts = []
                for function_call in response.function_calls:
                    function_call_result = call_function(
                        function_call, verbose=True
                    )

                    if not function_call_result.parts:
                        raise Exception(
                            "Error: function call has empty parts list"
                        )
                    part = function_call_result.parts[0]
                    if part.function_response is None:
                        raise Exception("Error: function call had no response")
                    if part.function_response.response is None:
                        raise Exception("Error: function response was empty")

                    print(f"-> {part.function_response.response}")
                    function_call_parts.append(part)

                # Send function results back as a tool role message
                messages.append(
                    types.Content(role="tool", parts=function_call_parts)
                )
            else:
                # No more function calls; output final response and end inner loop
                print(response.text)
                break
        else:
            print("Error: maximum number of iterations reached for this turn.")


if __name__ == "__main__":
    main()
