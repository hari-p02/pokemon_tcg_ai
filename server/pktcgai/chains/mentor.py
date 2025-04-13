from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from pktcgai.llm.ai import ANTHROPIC_LLM
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain.schema import AgentAction, AgentFinish
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever
# from langchain_anthropic.embeddings import AnthropicEmbeddings
from langchain_core.runnables import RunnablePassthrough
import os

class Master:
    def __init__(self):
        # self.embeddings = AnthropicEmbeddings(model_name="claude-3-sonnet-20240229")
        # self.vector_store = self._create_vector_store()
        # self.retriever = self.vector_store.as_retriever(
        #     search_type="similarity",
        #     search_kwargs={"k": 5}
        # )
        
        # self.tools = [
        #     Tool(
        #         name="PokemonTCGKnowledgeBase",
        #         description="Useful for finding specific information about Pokemon TCG rules, card mechanics, strategy advice, and game tactics",
        #         func=self._query_knowledge_base,
        #     )
        # ]
        
        self.prompt = ChatPromptTemplate.from_template("""
        You are a master mentor for Pokemon Trading Card Game players. You have deep expertise in all aspects of the game.
        Your role is to advise a player agent who is trying to make decisions in a Pokemon TCG match.
                                                       
        1. Determine if a player's proposed action is legal according to the Pokemon TCG rules
        2. Never propose a move that does not follow the rules of the game
        3. Only assume it's your first turn of the game if you ONLY have a single pokemon card in the active spot and 6 cards in your hand, i.e., the rest of the cards are in the prizes and deck.    
        
        The current game state is provided as a JSON object:
        {game_state}
                                                       
        You will notice that the game state has "id" values for the pokemon card it is referring to. The card for each id is as follows:
        {card_id_to_card_mapping}
    
        Here is an explination on how to interpret the JSON above that represents the game state:
                - The JSON object represents what cards belong with part of the Pokemon Game setup.
                - The JSON shows you all the cards you have in your deck, but this is in no particular order
                - "active": refers to the pokemon ids that your current active pokemon
                    This refers to the Pokémon id that is currently in the Active position on your side of the field. It is the Pokémon id that can attack, retreat, or be affected by effects during your turn or your opponent's turn.
                    The Active Pokémon id is the primary target for your opponent's attacks and abilities.
                - "bench": refers to all the pokemon ids on your bench
                    The Bench is where you place up to five Pokémon to support your Active Pokémon. These Pokémon can evolve, use abilities, or be swapped into the Active position if your Active Pokémon retreats or is knocked out.
                    Bench management is crucial for setting up strategies and preparing backup attackers.
                - "discard": this contains the pokemon ids that you have discarded from previous turns                                 
                    The discard pile contains cards that have been used or removed from play, such as Pokémon that were knocked out, Trainer cards that were played, or Energy cards that were discarded for retreat costs.
                    Some cards and abilities allow you to retrieve cards from the discard pile, making it an important resource in certain strategies.
                - "deck": The remaining pokemon ids yet to be drawed. NOTE THAT THE THE ORDER OF THESE POKEMON IS NOT THE TRUE ORDER, SO THE NEST CARD YOU DRAW IS NOT THE FIRST POKEMON IN THIS KEY
                        The deck contains all the remaining cards you have not yet drawn or played. It includes Pokémon, Trainer cards, and Energy cards that you will draw into during the game. At the start of the game, your deck is shuffled, and you draw your opening hand from it.
                        Managing your deck is crucial because running out of cards in your deck (decking out) means you lose the game. Cards like Professor's Research or Colress's Experiment can help you draw or thin your deck, while others like Energy Recycler or Pal Pad can shuffle cards back into your deck to extend your resources.
                - "lostZone": this contains the pokemon ids that you have put in the lost zone from previous turns
                    The Lost Zone is a special area where cards are permanently removed from the game. Unlike the discard pile, cards in the Lost Zone cannot be retrieved or reused.
                    Some Pokémon cards, like Giratina VSTAR, have effects that interact with the Lost Zone, making it a key mechanic in certain deck archetypes.
                - "hand": these are all the pokemon ids in your current hand that you can play with this turn
                    Your hand contains the cards you currently have available to play, including Pokémon, Trainer cards, and Energy cards. Managing your hand effectively is critical for executing your strategy and maintaining momentum.
                    Cards like Marnie or Judge can disrupt your opponent's hand, while abilities like Crobat V's "Dark Asset" can help you draw more cards.
                - "stadium": refers to the stadium card id in play if there is one
                        The Stadium card in play affects both players and provides unique effects that can alter the game state. Only one Stadium can be in play at a time, and playing a new Stadium replaces the current one.
                        Stadium cards can be used to boost your strategy or disrupt your opponent's plans, depending on the card.
                - "prizeCards": all the pokemon ids currently in your game
                        Prize cards are six cards set aside at the start of the game. Each time you knock out an opponent's Pokémon, you take one of your Prize cards. The goal is to take all six Prize cards to win the game.
                        Managing Prize cards is important, as sometimes key cards may be stuck in your Prize pool, requiring strategies to retrieve them (e.g., using cards like Hisuian Heavy Ball).

        Carefully reason about the cards you have available to play, for example you know what pokemon ids/card are in your deck but you may not have them in your hand so don't play them
                                                       
        You learn more about the id of a pokemon in teh game state through the card id to pokemon mapping above
                                                        
        You and the player have had this conversation for far:
        {mentor_player_conversation}
                                                       
        The player has asked the following question or is considering the following decisions:
        {player_question}
        
        
        
        Think step by step about the implications of different moves.
        Consider factors like:
        - Energy management and attachment strategy
        - Board development and bench management
        - Prize card trade efficiency
        - Turn sequencing and multi-turn planning
        - Card advantage and resource management
                                                       
        Though there may be many different actions that could be taken, you should only recommend one action. 
                                                       
        When referring to card IDs, you MUST use the format ( id: number ), including the parentheses. Any other format will fail. Double check your format before submitting your final decision.

        EXTREMELY IMPORTANT: Your entire response must be no more than 1-2 sentences total. Be direct and concise with your advice.
        
        Do not include any explanations, greetings, or follow-up questions. Just provide a single, precise recommendation in 1-2 sentences.
        """)
        
    # def _create_vector_store(self):
    #     """Create a vector store from all documents in the text folder"""
    #     text_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "text")
    #     documents = []
        
    #     chunk_size = 1000
        # rules_path = os.path.join(text_dir, "rules.txt")
        # if os.path.exists(rules_path):
        #     with open(rules_path, 'r') as f:
        #         rules_text = f.read()
            
        #     chunks = [rules_text[i:i+chunk_size] for i in range(0, len(rules_text), chunk_size)]
            
        #     for i, chunk in enumerate(chunks):
        #         documents.append({"page_content": chunk, "metadata": {"source": "rules.txt", "chunk": i}})
        
        # for filename in os.listdir(text_dir):
        #     if filename.endswith('.txt') and filename != 'rules.txt':
        #         file_path = os.path.join(text_dir, filename)
        #         with open(file_path, 'r') as f:
        #             text = f.read()
                
        #         chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
                
        #         for i, chunk in enumerate(chunks):
        #             documents.append({"page_content": chunk, "metadata": {"source": filename, "chunk": i}})
        
        # if documents:
        #     return FAISS.from_documents(documents, self.embeddings)
        # else:
        #     return FAISS.from_texts(["No Pokemon TCG knowledge base documents found"], self.embeddings)
    
    # def _query_knowledge_base(self, query):
    #     """Query the vector store for relevant information"""
        # results = self.retriever.get_relevant_documents(query)
        # formatted_results = ""
        # for i, doc in enumerate(results):
        #     formatted_results += f"Source: {doc.metadata.get('source', 'Unknown')}\n"
        #     formatted_results += f"Content: {doc.page_content}\n\n"
        
        # return formatted_results if formatted_results else "No relevant information found."
#         return """
#                     # Pokémon Trading Card Game Official Rulebook

# ## Pokémon TCG Basic Concepts

# The Pokémon Trading Card Game (TCG) is a two-player strategy card game where players assume the role of Pokémon Trainers. Using a deck of 60 cards containing Pokémon, Energy, and Trainer cards, players battle by placing Pokémon on the field and attacking their opponent's Pokémon. The game simulates Pokémon battles from the video games and anime series.

# ## How to Win

# There are three ways to win a Pokémon TCG game:
# 1. Take all of your Prize cards (typically 6).
# 2. Knock Out all of your opponent's Pokémon in play.
# 3. If your opponent has no cards left in their deck at the beginning of their turn.

# ## Energy Types

# Energy cards power your Pokémon's attacks. There are 11 Energy types:
# - Grass: Plant/Insect Pokémon (green)
# - Fire: Fire/Volcanic Pokémon (red)
# - Water: Aquatic/Marine Pokémon (blue)
# - Lightning: Electric Pokémon (yellow)
# - Psychic: Psychic/Ghost Pokémon (purple)
# - Fighting: Combat/Rock Pokémon (orange/brown)
# - Darkness: Dark/Evil Pokémon (black)
# - Metal: Steel/Machine Pokémon (gray)
# - Fairy: Fairy/Mythical Pokémon (pink)
# - Dragon: Dragon Pokémon (gold/multicolored)
# - Colorless: Normal/Flying Pokémon (white/clear)

# Most Energy cards provide one Energy of their type. Special Energy cards may provide different types or multiple Energy at once.

# ## Parts of a Pokémon Card

# 1. **Card Name**: Top-left corner
# 2. **HP (Hit Points)**: Top-right corner; shows how much damage a Pokémon can take
# 3. **Stage**: Indicates evolution stage (Basic, Stage 1, or Stage 2)
# 4. **Type**: Energy type icon showing the Pokémon's type
# 5. **Attacks**: Moves the Pokémon can use, their Energy cost, damage, and special effects
# 6. **Weakness**: Takes double damage from this type
# 7. **Resistance**: Takes less damage from this type
# 8. **Retreat Cost**: Energy needed to retreat this Pokémon
# 9. **Card Text/Ability**: Special powers or rules for this card
# 10. **Collector Number**: Card's number in the set
# 11. **Rarity Symbol**: Indicates card rarity (Common, Uncommon, Rare, etc.)

# ## 3 Card Types

# 1. **Pokémon Cards**: The main characters you battle with
#    - Basic Pokémon: Can be played directly to the field
#    - Stage 1: Evolves from a Basic Pokémon
#    - Stage 2: Evolves from a Stage 1 Pokémon
#    - Pokémon V, VMAX, VSTAR, ex, etc.: Special powerful Pokémon with unique rules

# 2. **Energy Cards**: Power Pokémon attacks
#    - Basic Energy: Provides one Energy of its type
#    - Special Energy: Has unique effects or provides multiple/different types of Energy

# 3. **Trainer Cards**: Support cards with various effects
#    - Item: Use and discard; can play multiple per turn
#    - Supporter: Powerful effects; limited to one per turn
#    - Stadium: Affects both players; only one can be in play at a time

# ## Zones of the Pokémon TCG

# 1. **Deck**: Where your undrawn cards are stored; face-down and shuffled
# 2. **Hand**: Cards you have drawn but not yet played
# 3. **Active Spot**: Your main Pokémon currently battling
# 4. **Bench**: Up to 5 Pokémon waiting to battle
# 5. **Discard Pile**: Cards that have been used or knocked out; face-up
# 6. **Prize Cards**: 6 cards set aside at game start; take one when you knock out an opponent's Pokémon
# 7. **Lost Zone**: A special zone where cards are permanently removed from play
# 8. **Play Area**: Contains Active Pokémon, Bench, and Stadium card

# ## Playing the Game

# ### How to Win the Game
# As described earlier, win by taking all Prize cards, knocking out all opponent's Pokémon, or if your opponent cannot draw a card at the start of their turn.

# ### Setting Up to Play
# 1. Shuffle your 60-card deck.
# 2. Place 6 cards face-down as Prize cards.
# 3. Each player draws 7 cards.
# 4. Each player must have at least one Basic Pokémon in their opening hand.
#    - If not, reveal your hand, shuffle it back, and draw 7 new cards.
#    - Your opponent may draw an extra card for each time you do this.
# 5. Place one Basic Pokémon face-down as your Active Pokémon.
# 6. Place up to 5 Basic Pokémon face-down on your Bench.
# 7. Both players flip over all their face-down Pokémon.
# 8. Flip a coin to decide who goes first (winner chooses).
#    - The player going first cannot attack on their first turn.

# ### Parts of a Turn
# Players take alternating turns, with each turn having these parts:
# 1. **Draw a card** from your deck.
# 2. **Do any of the following in any order**:
#    - Put Basic Pokémon from your hand onto your Bench (up to 5 total).
#    - Evolve your Pokémon (except on your first turn or a Pokémon played that turn).
#    - Attach ONE Energy card from your hand to a Pokémon.
#    - Play Trainer cards.
#    - Retreat your Active Pokémon (once per turn).
#    - Use Abilities.
# 3. **Attack** with your Active Pokémon (ending your turn).
# 4. **Check if any Pokémon are Knocked Out**.
# 5. **Take Prize cards** if you knocked out your opponent's Pokémon.

# ### Turn Actions

# #### Playing Basic Pokémon
# - Play directly from your hand to your Bench.
# - You can have a maximum of 5 Pokémon on your Bench.

# #### Evolution
# - Can only evolve a Pokémon that has been in play for one full turn.
# - Place the evolved form on top of the existing Pokémon.
# - Keeps all attached cards, damage counters, and Special Conditions.
# - Cannot evolve a Pokémon more than once per turn.

# #### Attaching Energy
# - Limited to ONE Energy card attachment per turn.
# - Energy stays with a Pokémon when it evolves.

# #### Trainer Cards
# - Follow the instructions on the card.
# - Item: Play as many as you want, then discard.
# - Supporter: Limited to one per turn, then discard.
# - Stadium: Only one can be in play; a new one replaces the old one.

# #### Retreat
# - Pay the retreat cost (discard Energy cards equal to the cost).
# - Move your Active Pokémon to the Bench.
# - Choose a Benched Pokémon to become Active.
# - Limited to once per turn.

# #### Attacking
# - Check Energy requirements for the attack.
# - Apply Weakness and Resistance.
# - Place damage counters on the defending Pokémon.
# - Check if the defending Pokémon is Knocked Out.
# - Your turn ends after attacking.

# ## Special Conditions

# Special Conditions affect Pokémon and last until the Pokémon is removed from play or recovers.

# 1. **Asleep**
#    - Turn the affected Pokémon sideways.
#    - Cannot attack or retreat.
#    - Flip a coin between turns; on heads, the Pokémon wakes up.

# 2. **Burned**
#    - Place a Burn marker on the Pokémon.
#    - Place 2 damage counters between turns.
#    - Flip a coin; on heads, the Pokémon is no longer burned.

# 3. **Confused**
#    - Turn the affected Pokémon upside down.
#    - To attack, flip a coin:
#      - Heads: Attack normally
#      - Tails: Place 3 damage counters on the Confused Pokémon

# 4. **Paralyzed**
#    - Turn the affected Pokémon clockwise 90 degrees.
#    - Cannot attack or retreat.
#    - Condition ends after the player's next turn.

# 5. **Poisoned**
#    - Place a Poison marker on the Pokémon.
#    - Place damage counters between turns (amount depends on poison severity).

# A Pokémon can have only one Special Condition at a time. When a Pokémon evolves or moves to the Bench, all Special Conditions are removed.
#         """
    
    # def create_agent_executor(self):
    #     """Create and return the agent executor"""
    #     agent = create_react_agent(
    #         llm=ANTHROPIC_LLM,
    #         tools=self.tools,
    #         prompt=self.prompt
    #     )
        
    #     return AgentExecutor(
    #         agent=agent,
    #         tools=self.tools,
    #         verbose=False,
    #         handle_parsing_errors=True,
    #         max_iterations=10
    #     )
    def make_chain(self):
        mentor_chain = self.prompt | ANTHROPIC_LLM.with_config({"callbacks": None, "streaming": True})
        return mentor_chain
    