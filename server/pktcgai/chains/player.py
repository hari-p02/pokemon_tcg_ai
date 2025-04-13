from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from pktcgai.llm.ai import ANTHROPIC_LLM

class Player:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_template("""
            You are a Pokémon player, who is very knowledgeable about the Pokemon Trading card game battle mechanics.
            You are given a deck of Pokémon cards which is represented through the following JSON:
            {game_state}
                                                       
            Here is an explination on how to interpret the JSON above that represents the game state:
                - The JSON object represents what cards belong with part of the Pokemon Game setup.
                - The JSON shows you all the cards you have in your deck, but this is in no particular order
                - "active": refers to the pokemon that your current active pokemon
                    This refers to the Pokémon that is currently in the Active position on your side of the field. It is the Pokémon that can attack, retreat, or be affected by effects during your turn or your opponent's turn.
                    The Active Pokémon is the primary target for your opponent's attacks and abilities.
                - "bench": refers to all the pokemon on your bench
                    The Bench is where you place up to five Pokémon to support your Active Pokémon. These Pokémon can evolve, use abilities, or be swapped into the Active position if your Active Pokémon retreats or is knocked out.
                    Bench management is crucial for setting up strategies and preparing backup attackers.
                - "discard": this contains the pokemon cards that you have discarded from previous turns                                 
                    The discard pile contains cards that have been used or removed from play, such as Pokémon that were knocked out, Trainer cards that were played, or Energy cards that were discarded for retreat costs.
                    Some cards and abilities allow you to retrieve cards from the discard pile, making it an important resource in certain strategies.
                - "deck": The remaining pokemon cards yet to be drawed. NOTE THAT THE THE ORDER OF THESE POKEMON IS NOT THE TRUE ORDER, SO THE NEST CARD YOU DRAW IS NOT THE FIRST POKEMON IN THIS KEY
                        The deck contains all the remaining cards you have not yet drawn or played. It includes Pokémon, Trainer cards, and Energy cards that you will draw into during the game. At the start of the game, your deck is shuffled, and you draw your opening hand from it.
                        Managing your deck is crucial because running out of cards in your deck (decking out) means you lose the game. Cards like Professor's Research or Colress's Experiment can help you draw or thin your deck, while others like Energy Recycler or Pal Pad can shuffle cards back into your deck to extend your resources.
                - "lostZone": this contains the pokemon cards that you have put in the lost zone from previous turns
                    The Lost Zone is a special area where cards are permanently removed from the game. Unlike the discard pile, cards in the Lost Zone cannot be retrieved or reused.
                    Some Pokémon cards, like Giratina VSTAR, have effects that interact with the Lost Zone, making it a key mechanic in certain deck archetypes.
                - "hand": these are all the pokemon cads in your current hand
                    Your hand contains the cards you currently have available to play, including Pokémon, Trainer cards, and Energy cards. Managing your hand effectively is critical for executing your strategy and maintaining momentum.
                    Cards like Marnie or Judge can disrupt your opponent's hand, while abilities like Crobat V's "Dark Asset" can help you draw more cards.
                - "stadium": refers to the stadium in play if there is one
                        The Stadium card in play affects both players and provides unique effects that can alter the game state. Only one Stadium can be in play at a time, and playing a new Stadium replaces the current one.
                        Stadium cards can be used to boost your strategy or disrupt your opponent's plans, depending on the card.
                - "prizeCards": all the pokemon cards currently in your game
                        Prize cards are six cards set aside at the start of the game. Each time you knock out an opponent's Pokémon, you take one of your Prize cards. The goal is to take all six Prize cards to win the game.
                        Managing Prize cards is important, as sometimes key cards may be stuck in your Prize pool, requiring strategies to retrieve them (e.g., using cards like Hisuian Heavy Ball).

            You task is to describe an action you want to take on the state. Any action is valid as long as it respects the rule of the Pokemon TCG game. 
                                                       
            BUT, before you decide on an action know that you have access to a mentor. The mentor specializes in the Pokemon TCG card battle game and is better than you at the game. 
            You are allowed to talk with your mentor my asking any questions you have. You can even ask if for feedback on your moves, and anything else.
            However, YOU CAN ONLY INTERACT WITH THE MENTOR ONCE and ONLY ONCE!!!
            
            Here is your current conversation with your mentor:
            {mentor_player_conversation}
                                                       
            When you propose your next move. If you're ready to make a final decision, include the phrase: FINAL DECISION: <your move here>.
            YOU MUST INCLUDE "FINAL DECISION" IN YOUR ANSWER IF AND ONLY IF YOU NO LONGER WANT TO TALK TO THE MENTOR.
            Without "FINAL DECISION" it will be assumed anything you ask will be directed to the mentor for their feedback
                                                       
            Also you may want to do multiple moves in a row. However you MUST ONLY CHOOSE ONE MOVE TO DO. You FAIL IF YOU DO MULTIPLE MOVES.
                                                       
            EXTREMELY IMPORTANT: Keep your responses to 1-2 sentences max. When asking the mentor a question, use a single clear sentence. When making a final decision, state only the exact action in 1-2 direct sentences.
            
            Do not include any explanations, greetings, or verbose descriptions. Just state your question or decision clearly and concisely.

            When referring to card IDs, you MUST use the format ( id: number ), including the parentheses. Any other format will fail. Double check your format before submitting your final decision.
        """)

    def make_chain(self):
        player_chain = self.prompt | ANTHROPIC_LLM.with_config({"callbacks": None, "streaming": True})
        return player_chain
    