from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from pktcgai.llm.ai import ANTHROPIC_LLM

class Master:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_template("""
            
        """)

    def make_chain(self):
        player_chain = self.prompt | ANTHROPIC_LLM
        return player_chain
    