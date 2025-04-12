from langchain_anthropic import ChatAnthropic
import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_LLM = ChatAnthropic(
            model="claude-3-7-sonnet-20250219",
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            streaming=True
        )