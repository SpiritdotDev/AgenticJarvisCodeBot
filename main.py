import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions,call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("API key not found")

client = genai.Client(api_key=api_key)


def main():
    print("Hello sir.")

    parser = argparse.ArgumentParser(description="Jarvis")
    parser.add_argument("user_prompt", type=str, help="What can I help you with sir?")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0
                )
            )
        
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
    
        function_calls_results = []

        if args.verbose: 
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            if response.function_calls != None:
                for function_call in response.function_calls:
                    function_call_result = call_function(function_call, verbose=True)
                    if function_call_result.parts == []:
                        raise Exception("Error: function call has empty parts list")
                    if function_call_result.parts[0].function_response == None:
                        raise Exception("Error: function call had no response")
                    if function_call_result.parts[0].function_response.response == None:
                        raise Exception("Error: function response was empty")
                    function_calls_results.append(function_call_result.parts[0])
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            else:
                print(response.text)
                return
        else:
            if response.function_calls != None:
                for function_call in response.function_calls:
                    function_call_result = call_function(function_call)
                    if function_call_result.parts == []:
                        raise Exception("Error: function call has empty parts list")
                    if function_call_result.parts[0].function_response == None:
                        raise Exception("Error: function call had no response")
                    if function_call_result.parts[0].function_response.response == None:
                        raise Exception("Error: function response was empty")
                    function_calls_results.append(function_call_result.parts[0])
            else:
                print(response.text)
                return

        messages.append(types.Content(role="user", parts=function_calls_results))
    
    print("Error: maximum number of iterations reached")
    os.exit()


if __name__ == "__main__":
    main()
