from langchain_core.prompts import ChatPromptTemplate
from pktcgai.llm.ai import ANTHROPIC_LLM
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import json
import re

class Referee:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_template("""
        You are a Referee for a Pokemon Trading Card Game match. Your job is to:
        1. Determine if a player's proposed action is legal according to the Pokemon TCG rules
        2. Update the game state based on the action if it is legal

        Here is the current game state as a JSON object:
        {game_state}
                                                       
        You will notice that the game state has "id" values for the pokemon card it is referring to. The card for each id is as follows:
        {card_id_to_card_mapping}

        The player has proposed the following action:
        {player_action}

        
        Then, if the action is legal:
        1. Update the game state JSON to reflect the changes caused by the action
            - For example if the opponent pokemon has 100 hp and the player attacks for 50, the opponent pokemon should be updated to have 50 hp
            - If a prize card is taken, update the game state to reflect the prize card being taken.
            - And so on....
        2. Return the new game state as a valid JSON object

        If the action is illegal:
        1. Do not modify the game state
        2. Explain why the action is not legal
        3. Start your response with "ILLEGAL ACTION:"

        ALWAYS MAINTAIN THE EXACT STRUCTURE OF THE ORIGINAL GAME STATE JSON BUT UPDATE THE RELEVANT VALUES.
        YOU FAIL YOUR TASK IF YOU DO NOT FOLLOW THIS INSTRUCTION.
                                                       
        NEVER OUTPUT THE CARD ID MAPPING IN YOUR RESPONSE, ONLY THE GAME STATE!!!
    
        
        Updated Game State:
        ```json
        {{Updated game state JSON if the action is legal or the original game state if the action is illegal}}
        ```
        
        EXTREMELY IMPORTANT: Your explanation must be only 1-2 sentences maximum. Do not include any thought process, greetings, or verbose explanations.
        
        If the action is legal, only mention that the action was legal NOTHING ELSE, DO NOT SAY WHY ITS LEGAL OR WHY IT MIGHT BE A GOOD MOVE YOU FAIL IF YOU DO.
        If the action is illegal, start with "ILLEGAL ACTION:" followed by a single sentence explaining why.
        """)
    
    def make_chain(self):
        # Use streaming like Player and Mentor classes
        referee_chain = self.prompt | ANTHROPIC_LLM.with_config({"callbacks": None, "streaming": True})
        return referee_chain
    
    def invoke(self, inputs):
        """
        Validates a player's action and updates the game state if legal
        
        Args:
            inputs (dict): Dictionary containing game_state, player_action, and card_id_to_card_mapping
            
        Returns:
            dict: Response containing whether the action was legal and the updated game state
        """
        game_state = inputs.get("game_state", {})
        player_action = inputs.get("player_action", "")
        card_id_to_card_mapping = inputs.get("card_id_to_card_mapping", {})
        
        # Convert to string if needed
        if isinstance(game_state, dict):
            game_state_str = json.dumps(game_state)
        else:
            game_state_str = game_state
        
        if isinstance(card_id_to_card_mapping, dict):
            card_id_to_card_mapping_str = json.dumps(card_id_to_card_mapping)
        else:
            card_id_to_card_mapping_str = card_id_to_card_mapping
        
        # Use streaming chain like other classes
        chain = self.make_chain()
        
        # Print info about the referee's analysis
        # print("--------------REFEREE ANALYZING ACTION-----------------")
        
        try:
            # Get the streaming response
            response_chunks = chain.stream({
                "game_state": game_state_str, 
                "player_action": player_action, 
                "card_id_to_card_mapping": card_id_to_card_mapping_str
            })
            
            # Process and collect streaming chunks
            full_response = ""
            visible_response = ""
            json_content = ""
            in_json_block = False
            
            # Collect chunks and only print non-JSON content
            accumulated_text = ""
            
            # Process each chunk as it comes in
            for chunk in response_chunks:
                chunk_text = chunk.content if hasattr(chunk, 'content') else str(chunk)
                full_response += chunk_text
                
                # Check for JSON markers and accumulate text
                if "json" in chunk_text:
                    # Split the chunk at the JSON marker
                    parts = chunk_text.split("json", 1)
                    
                    # Print any text before the JSON marker
                    # if parts[0]:
                    #     print(parts[0], end="", flush=True)
                    #     visible_response += parts[0]
                    
                    # Start accumulating for JSON content
                    accumulated_text = "json" + (parts[1] if len(parts) > 1 else "")
                    in_json_block = True
                elif in_json_block:
                    # Keep accumulating text while in JSON block
                    accumulated_text += chunk_text
                    
                    # Check if we're exiting the JSON block
                    if "```" in chunk_text:
                        # Find the position of the closing marker
                        parts = accumulated_text.split("```", 1)
                        if len(parts) > 1:
                            # We have text after the closing marker
                            json_block = parts[0]
                            after_json = parts[1]
                            
                            # Store the JSON content without printing
                            json_content += json_block
                            
                            # Print the text after the JSON block
                            # print(after_json, end="", flush=True)
                            visible_response += after_json
                            
                            # Reset accumulation
                            accumulated_text = ""
                            in_json_block = False
                else:
                    # Normal text outside of JSON block, print it
                    print(chunk_text, end="", flush=True)
                    visible_response += chunk_text
            
            # Handle any remaining accumulated text
            if in_json_block:
                # Extract any JSON content without printing
                json_content += accumulated_text
            
            # print()  # Add a newline after the streaming response
            
            # Process the full response after streaming is complete
            return self.process_response(full_response, game_state, visible_response)
            
        except Exception as e:
            print(f"Error in referee invoke method: {e}")
            # Return a fallback response
            return {
                "is_legal": False,
                "explanation": f"Error processing referee response: {str(e)}",
                "updated_state": game_state,
                "raw_response": "Error"
            }
    
    def process_response(self, result, game_state, visible_response):
        """Process the response from the LLM to extract the necessary information"""
        try:
            # print(f"Processing referee response of length: {len(result)}")
            
            # Parse the result to extract the JSON game state
            is_illegal = "ILLEGAL ACTION" in result or (visible_response and "ILLEGAL ACTION" in visible_response)
            
            # Extract the updated game state JSON
            json_match = re.search(r"```json\n(.*?)\n```", result, re.DOTALL)
            updated_state = None
            
            if json_match:
                try:
                    updated_state = json.loads(json_match.group(1))
                    # print("Successfully parsed JSON from referee response")
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error: {e}")
                    print(f"JSON content that failed to parse: {json_match.group(1)[:100]}...")
                    # If there's an error parsing the JSON, return the original state
                    updated_state = game_state if isinstance(game_state, dict) else json.loads(game_state)
            else:
                print("No JSON block found in referee response")
            
            # Use visible_response for explanation if available
            explanation_text = visible_response if visible_response else result
            
            explanation = ""
            if "Explanation:" in explanation_text:
                explanation_pattern = r'Explanation:\s*(.*?)(?=\n\n|$)'
                explanation_match = re.search(explanation_pattern, explanation_text, re.DOTALL)
                if explanation_match:
                    explanation = explanation_match.group(1)#.strip()
                    # print(f"Found explanation: {explanation[:50]}...")
                else:
                    # print("Explanation pattern matched but couldn't extract content")
                    explanation = explanation_text  # Fallback to using the whole visible text
            else:
                # print("No Explanation section found in response")
                explanation = explanation_text  # Use the whole visible text as explanation
            
            return {
                "is_legal": not is_illegal,
                "explanation": explanation,
                "updated_state": updated_state or game_state,
                "raw_response": result
            }
        except Exception as e:
            print(f"Error in process_response: {e}")
            return {
                "is_legal": False,
                "explanation": f"Error processing response: {str(e)}",
                "updated_state": game_state,
                "raw_response": result if isinstance(result, str) else str(result)
            }
