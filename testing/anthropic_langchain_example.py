"""
Example of using LangChain with Anthropic's Claude model in Python
"""
import os
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Initialize the Anthropic model
# Set your API key in environment variables or replace directly (not recommended)
# os.environ["ANTHROPIC_API_KEY"] = "your-api-key-here"

model = ChatAnthropic(
    model="claude-3-sonnet-20240229",  # You can use other models like claude-3-opus or claude-3-haiku
    temperature=0.7,
    anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# Create a prompt template
prompt = ChatPromptTemplate.from_template("""
Answer the following question about Pokémon:
{question}

Provide your answer in a concise, informative manner.
""")

# Create a simple chain
chain = prompt | model | StrOutputParser()

def main():
    try:
        question = "What are the strengths and weaknesses of Fire-type Pokémon?"
        
        print(f"Question: {question}")
        print("Thinking...")
        
        response = chain.invoke({"question": question})
        
        print("Response:")
        print(response)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 