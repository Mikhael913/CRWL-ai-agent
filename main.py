import argparse
import os


from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt



def main() -> None:

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if api_key is None:
        raise RuntimeError(
            "DEEPSEEK_API_KEY not found. Did you create a .env file with your key?"
        )

    client = OpenAI(
             base_url="https://api.deepseek.com",
             api_key=api_key,
         )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
        ]

    for iteration in range(20):
        if args.verbose:
            print(f"Iteration {iteration + 1}/{20}")

        response = client.chat.completions.create(
            model="deepseek-flash",
            messages=messages,
            tools=available_functions,
            temperature = 0,
        )

        if response.usage is None:
            raise RuntimeError("Failed to get usage data from the response")

        if args.verbose:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print("Final response:")
            print(message.content or "")
            return

        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            messages.append(result_message)

            if not result_message["content"]:
                raise RuntimeError("Function returned empty content")

    print("Error: Agent loop reached the maximum number of iterations without a final response.")
    raise SystemExit(1)

if __name__ == "__main__":
    main()
