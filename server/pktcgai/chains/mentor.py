from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from pktcgai.llm.ai import ANTHROPIC_LLM
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain.schema import AgentAction, AgentFinish
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_anthropic.embeddings import AnthropicEmbeddings
from langchain_core.runnables import RunnablePassthrough
import os

class Master:
    def __init__(self):
        self.embeddings = AnthropicEmbeddings(model_name="claude-3-sonnet-20240229")
        self.vector_store = self._create_vector_store()
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
        
        self.tools = [
            Tool(
                name="PokemonTCGKnowledgeBase",
                description="Useful for finding specific information about Pokemon TCG rules, card mechanics, strategy advice, and game tactics",
                func=self._query_knowledge_base,
            )
        ]
        
        self.prompt = ChatPromptTemplate.from_template("""
        You are a master mentor for Pokemon Trading Card Game players. You have deep expertise in all aspects of the game.
        Your role is to advise a player agent who is trying to make decisions in a Pokemon TCG match.
        
        You have access to a knowledge base of Pokemon TCG rules, strategies, and card mechanics.
        Use this knowledge base to provide accurate, strategic advice on game situations.
        
        The current game state is provided as a JSON object:
        {game_state}
        
        The player has asked the following question or is considering the following move:
        {question}
        
        You have access to these tools:
        {tools}
        
        Think step by step about the implications of different moves.
        Consider factors like:
        - Energy management and attachment strategy
        - Board development and bench management
        - Prize card trade efficiency
        - Turn sequencing and multi-turn planning
        - Card advantage and resource management
        
        Use the following format:
        
        Thought: You should always think about what to do
        Action: The action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: Your advice to the player about their question or move, explaining why it's good or bad and suggesting alternatives if appropriate
        
        Begin!
        
        Thought:
        """)
        
    def _create_vector_store(self):
        """Create a vector store from all documents in the text folder"""
        text_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "text")
        documents = []
        
        rules_path = os.path.join(text_dir, "rules.txt")
        if os.path.exists(rules_path):
            with open(rules_path, 'r') as f:
                rules_text = f.read()
            
            chunk_size = 1000
            chunks = [rules_text[i:i+chunk_size] for i in range(0, len(rules_text), chunk_size)]
            
            for i, chunk in enumerate(chunks):
                documents.append({"page_content": chunk, "metadata": {"source": "rules.txt", "chunk": i}})
        
        for filename in os.listdir(text_dir):
            if filename.endswith('.txt') and filename != 'rules.txt':
                file_path = os.path.join(text_dir, filename)
                with open(file_path, 'r') as f:
                    text = f.read()
                
                chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
                
                for i, chunk in enumerate(chunks):
                    documents.append({"page_content": chunk, "metadata": {"source": filename, "chunk": i}})
        
        if documents:
            return FAISS.from_documents(documents, self.embeddings)
        else:
            return FAISS.from_texts(["No Pokemon TCG knowledge base documents found"], self.embeddings)
    
    def _query_knowledge_base(self, query):
        """Query the vector store for relevant information"""
        results = self.retriever.get_relevant_documents(query)
        formatted_results = ""
        for i, doc in enumerate(results):
            formatted_results += f"Source: {doc.metadata.get('source', 'Unknown')}\n"
            formatted_results += f"Content: {doc.page_content}\n\n"
        
        return formatted_results if formatted_results else "No relevant information found."
    
    def create_agent_executor(self):
        """Create and return the agent executor"""
        agent = create_react_agent(
            llm=ANTHROPIC_LLM,
            tools=self.tools,
            prompt=self.prompt
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10
        )
    