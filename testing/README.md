# LangChain with Anthropic Models

This directory contains an example of using LangChain with Anthropic's Claude models in Python.

## Setup

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Set your Anthropic API key as an environment variable:
   ```
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

3. Run the example:
   ```
   python anthropic_langchain_example.py
   ```

## Example Details

The example demonstrates:
- Setting up a ChatAnthropic model
- Creating a prompt template
- Setting up a chain to process the prompt through the model
- Getting a response to a question about Pokémon

## Notes

- The example uses the Claude 3 Sonnet model, but you can change to other models like Claude 3 Opus or Claude 3 Haiku
- Remember to never hardcode your API keys in production code 