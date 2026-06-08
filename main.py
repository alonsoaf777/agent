import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from available_schemas import available_functions
from call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("No api key found.")

# App args
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

# Model parameters
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

- When the task is complete, give a concise summary of what you did.
"""

messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]

config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

response_list = []

# Model call
client = genai.Client(api_key=api_key)

for _ in range(20):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=config,
    )

    if response.usage_metadata is None:
        raise RuntimeError("No response retrieved.")

    for candidate in response.candidates:
        messages.append(candidate)

    if response.function_calls is not None:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call)

            if not function_call_result.parts:
                raise Exception("No parts in function call")

            if function_call_result.parts[0].function_response is None:
                raise Exception("No FunctionResponse object")
            
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("No result from AI call")
            
            response_list.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            
            messages.append(types.Content(role="user", parts=response_list))
    else:
        print(response.text)
        sys.exit(0)

print("Agent didn't resolve in default iterations.")
sys.exit(1)