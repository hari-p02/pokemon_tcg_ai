from typing import Dict, List, Any, TypedDict, Annotated, Literal, Union
import json
from enum import Enum

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from pktcgai.chains.player import Player
from pktcgai.chains.mentor import Master as Mentor
from pktcgai.chains.referee import Referee


class ConversationState(TypedDict):
    """State for the Pokemon TCG agent conversation flow."""
    game_state: Dict[str, Any]
    card_id_to_card_mapping: Dict[str, Any]
    player_action: str
    mentor_player_conversation: List[Dict[str, str]]
    current_node: str
    final_decision: bool
    decision_is_legal: bool
    decision_explanation: str
    updated_game_state: Dict[str, Any]


def transform_game_state(game_state, card_id_to_card_mapping):
    """
    Transform the game state by:
    1. Removing all 'hp' keys
    2. Replacing 'id' references with full card details from the mapping
    
    Args:
        game_state: The original game state
        card_id_to_card_mapping: Mapping of card IDs to card details
        
    Returns:
        Transformed game state
    """
    # Create a deep copy of the game state to avoid modifying the original
    transformed_game_state = json.loads(json.dumps(game_state))
    # print(f"Card mapping keys: {list(card_id_to_card_mapping.keys())[:5]}...")
    # print(f"Number of cards in mapping: {len(card_id_to_card_mapping)}")
    
    # Helper function to recursively process the game state
    def process_game_state(obj):
        if isinstance(obj, dict):
            # Remove 'hp' keys
            if 'hp' in obj:
                del obj['hp']
            
            # Replace 'id' with card details
            if 'id' in obj and str(obj['id']) in card_id_to_card_mapping:
                # Get card details
                card_id = str(obj['id'])
                # print(f"Found card ID: {card_id} in mapping")
                card_details = card_id_to_card_mapping[card_id]
                # Merge card details into the object
                for key, value in card_details.items():
                    if key != 'hp':  # Skip adding hp back
                        obj[key] = value
            elif 'id' in obj and obj['id'] not in card_id_to_card_mapping:
                print(f"Card ID not found in mapping: {obj['id']}")
                
            # Process nested dictionaries
            for key, value in list(obj.items()):
                obj[key] = process_game_state(value)
            
        elif isinstance(obj, list):
            # Process items in lists
            return [process_game_state(item) for item in obj]
        
        return obj
    
    # Apply transformations and return the processed state
    transformed_game_state = process_game_state(transformed_game_state)
    return transformed_game_state


def create_pokemon_tcg_graph():
    """Create and return the Pokemon TCG agent workflow graph."""
    
    player_agent = Player().make_chain()
    mentor_agent = Mentor().make_chain()
    referee_agent = Referee()  # Use the full Referee instance, not just the chain
    
    workflow = StateGraph(ConversationState)
    
    
    def player_node(state: ConversationState) -> ConversationState:
        # print("IN THE PLAYER NODE")
        print("-------------PLAYER NODE STARTED-------------------")
        formatted_conversation = ""
        for message in state["mentor_player_conversation"]:
            if message["role"] == "player":
                formatted_conversation += f"Player: {message['content']}\n"
            else:
                formatted_conversation += f"Mentor: {message['content']}\n"
        
        additional_context = ""
        if not state["decision_is_legal"] and state["decision_explanation"]:
            additional_context = f"\n\nYour previous action: '{state['player_action']}' was ILLEGAL: {state['decision_explanation']}\nPlease reconsider your action."
            state["final_decision"] = False

        # Transform the game state for the player
        transformed_game_state = transform_game_state(
            state["game_state"], 
            state["card_id_to_card_mapping"]
        )

        # print()
        # print("THIS IS THE TRANSFORMED STATE", transformed_game_state)
        # print()
        
        # Get streaming response
        response_chunks = player_agent.stream({
            "game_state": json.dumps(transformed_game_state),
            "mentor_player_conversation": formatted_conversation + additional_context
        })
        
        # Process and collect streaming chunks
        full_response = ""
        # Print each chunk as it comes in for real-time display
        for chunk in response_chunks:
            # AIMessageChunk objects have a .content attribute to get the text
            chunk_text = chunk.content if hasattr(chunk, 'content') else str(chunk)
            print(chunk_text, end="", flush=True)
            full_response += chunk_text
        print()  # Add a newline after the streaming response
        
        if "FINAL DECISION:" in full_response:
            # decision_parts = full_response.split("FINAL DECISION:")
            # player_action = decision_parts[1].strip()
            player_action = full_response
            
            state["player_action"] = player_action
            state["final_decision"] = True
            
            state["mentor_player_conversation"].append({
                "role": "player",
                "content": full_response
            })
        else:
            state["mentor_player_conversation"].append({
                "role": "player",
                "content": full_response
            })
            state["final_decision"] = False
        # print("IN PLAYER NODE STATE CONVERSATIONS", state["mentor_player_conversation"])
        return state
    
    def mentor_node(state: ConversationState) -> ConversationState:
        # print("IN THE MENTOR NODE")
        print("-------------MASTER NODE STARTED-------------------")
        latest_player_message = next(
            (msg["content"] for msg in reversed(state["mentor_player_conversation"]) 
             if msg["role"] == "player"), 
            ""
        )
        
        # Transform the game state for the mentor
        transformed_game_state = transform_game_state(
            state["game_state"], 
            state["card_id_to_card_mapping"]
        )

        formatted_conversation = ""
        for message in state["mentor_player_conversation"]:
            if message["role"] == "player":
                formatted_conversation += f"Player: {message['content']}\n"
            else:
                formatted_conversation += f"Mentor: {message['content']}\n"
        
        # Get streaming response
        response_chunks = mentor_agent.stream({
            "game_state": json.dumps(transformed_game_state),
            "mentor_player_conversation": formatted_conversation,
            "player_question": latest_player_message
        })
        
        # Process and collect streaming chunks
        full_response = ""
        # Print each chunk as it comes in for real-time display
        for chunk in response_chunks:
            # AIMessageChunk objects have a .content attribute to get the text
            chunk_text = chunk.content if hasattr(chunk, 'content') else str(chunk)
            print(chunk_text, end="", flush=True)
            full_response += chunk_text
        print()  # Add a newline after the streaming response
        
        # print("IN MASTER NODE RESPONSE", response.keys(), type(response))
        state["mentor_player_conversation"].append({
            "role": "mentor",
            "content": full_response
        })
        # print("IN MASTER NODE STATE CONVERSATIONS", state["mentor_player_conversation"])
        return state
    
    def referee_node(state: ConversationState) -> ConversationState:
        print("-------------REFEREE NODE STARTED-------------------")
        
        # Convert game state and card mapping to strings if needed
        game_state_str = json.dumps(state["game_state"]) if isinstance(state["game_state"], dict) else state["game_state"]
        card_mapping_str = json.dumps(state["card_id_to_card_mapping"]) if isinstance(state["card_id_to_card_mapping"], dict) else state["card_id_to_card_mapping"]
        
        # Use referee's invoke method which handles JSON filtering
        try:
            result = referee_agent.invoke({
                "game_state": game_state_str,
                "player_action": state["player_action"],
                "card_id_to_card_mapping": card_mapping_str
            })
            
            # Use the processed result from the invoke method
            state["decision_is_legal"] = result["is_legal"]
            state["decision_explanation"] = result["explanation"]
            state["updated_game_state"] = result["updated_state"]
            
        except Exception as e:
            print(f"Error in referee node: {e}")
            state["decision_is_legal"] = False
            state["decision_explanation"] = f"Error processing action: {str(e)}"
            state["updated_game_state"] = state["game_state"]
        
        return state
    
    workflow.add_node("player", player_node)
    workflow.add_node("mentor", mentor_node)
    workflow.add_node("referee", referee_node)
    
    
    workflow.add_conditional_edges(
        "player",
        # Condition function to determine next node
        lambda state: "referee" if state["final_decision"] else "mentor",
        {
            "referee": "referee",
            "mentor": "mentor"
        }
    )
    
    workflow.add_edge("mentor", "player")
    
    workflow.add_conditional_edges(
        "referee",
        # If action is legal, end the workflow. If illegal, go back to player.
        lambda state: "end" if state["decision_is_legal"] else "player",
        {
            "end": END,
            "player": "player"
        }
    )
    
    workflow.set_entry_point("player")
    
    return workflow


def initialize_game_state(game_data, card_mapping) -> ConversationState:
    """Initialize the game state for the Pokemon TCG agent workflow."""
    return {
        "game_state": game_data,
        "card_id_to_card_mapping": card_mapping,
        "player_action": "",
        "mentor_player_conversation": [],
        "current_node": "player",
        "final_decision": False,
        "decision_is_legal": False,
        "decision_explanation": "",
        "updated_game_state": {}
    }


def run_pokemon_tcg_turn(game_data, card_mapping, max_iterations=500) -> Dict[str, Any]:
    """
    Run a single turn of the Pokemon TCG agent workflow.
    
    Args:
        game_data: The current game state
        card_mapping: Mapping of card IDs to card details
        max_iterations: Maximum number of iterations to prevent infinite loops
        
    Returns:
        Dict containing the action, legality status, explanation, updated game state,
        and the conversation history
    """
    initial_state = initialize_game_state(game_data, card_mapping)
    
    workflow = create_pokemon_tcg_graph()
    
    app = workflow.compile()

    # print("THIS IS THE INITIAL STATE", initial_state)
    
    # Run the workflow with a maximum number of iterations to prevent infinite loops
    # in case the player keeps making illegal actions
    final_state = app.invoke(initial_state, {"recursion_limit": max_iterations})
    
    # Check if we hit the recursion limit - this means we had too many illegal actions
    hit_limit = False
    if not final_state["decision_is_legal"] and final_state["decision_explanation"]:
        hit_limit = True
    
    return {
        "action": final_state["player_action"],
        "is_legal": final_state["decision_is_legal"],
        "explanation": final_state["decision_explanation"],
        "updated_game_state": final_state["updated_game_state"],
        "conversation": final_state["mentor_player_conversation"],
        "hit_iteration_limit": hit_limit
    } 