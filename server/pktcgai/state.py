from typing import List, Optional, Dict, Any
from dataclasses import dataclass

# Global card mapping dictionary
CARD_MAP: Dict[int, dict] = {}

@dataclass
class Card:
    id: int

@dataclass
class PokemonInPlay:
    id: int
    hp: int
    attachedCards: Optional[List[Card]] = None

@dataclass
class PlayerState:
    active: Optional[PokemonInPlay] = None
    bench: Optional[List[PokemonInPlay]] = None
    discard: Optional[List[Card]] = None
    lostZone: Optional[List[Card]] = None
    deck: Optional[List[Card]] = None
    hand: Optional[List[Card]] = None
    stadium: Optional[Card] = None
    prizeCards: Optional[List[Card]] = None

@dataclass
class BoardState:
    playerOne: PlayerState
    playerTwo: PlayerState
    cardMap: Dict[int, dict]  # Include the card map in the board state

def get_card_map(deck: List[dict]) -> Dict[int, dict]:
    card_map = {}
    for i, card_info in enumerate(deck):
        card_map[i] = card_info
    return card_map

def get_initial_state(deck_one: List[dict], deck_two: List[dict]) -> BoardState:
    # Create a mapping of card IDs to card info for both decks
    card_map_one = get_card_map(deck_one)
    card_map_two = get_card_map(deck_two)
    
    # Combine both card maps
    card_map = {**card_map_one, **{k + len(deck_one): v for k, v in card_map_two.items()}}
    
    # Convert decks to Card objects with IDs
    cards_one = [Card(id=i) for i in range(len(deck_one))]
    cards_two = [Card(id=i + len(deck_one)) for i in range(len(deck_two))]  # Offset IDs for second deck
    
    # Shuffle the decks
    import random
    random.shuffle(cards_one)
    random.shuffle(cards_two)
    
    # Find a basic Pokemon for active for player one
    active_card_one = None
    for card in cards_one:
        card_info = card_map[card.id]
        if card_info.get('supertype') == 'Pokémon' and 'Basic' in card_info.get('subtypes', []):
            active_card_one = card
            cards_one.remove(card)
            break
    
    # If we didn't find a basic Pokemon, just use the first card (this is just for testing)
    if active_card_one is None and cards_one:
        active_card_one = cards_one[0]
        cards_one.remove(active_card_one)
    
    # Initialize player one state with simplified structure
    player_state = PlayerState(
        active=PokemonInPlay(
            id=active_card_one.id, 
            hp=int(card_map[active_card_one.id].get('hp', 0))
        ) if active_card_one else None,
        hand=cards_one[:6],  # First 6 cards in hand
        prizeCards=cards_one[6:12] if len(cards_one) >= 12 else [],  # Next 6 cards as prize cards
        deck=cards_one[12:],  # Remaining cards in deck
        bench=[],  # Empty bench
        discard=[],  # Empty discard pile
        lostZone=[],  # Empty lost zone
        stadium=None  # No stadium card
    )
    
    # Find a basic Pokemon for active for player two
    active_card_two = None
    for card in cards_two:
        card_info = card_map[card.id]
        if card_info.get('supertype') == 'Pokémon' and 'Basic' in card_info.get('subtypes', []):
            active_card_two = card
            cards_two.remove(card)
            break
    
    # If we didn't find a basic Pokemon, just use the first card (this is just for testing)
    if active_card_two is None and cards_two:
        active_card_two = cards_two[0]
        cards_two.remove(active_card_two)
    
    # Initialize player two state with simplified structure
    player_two_state = PlayerState(
        active=PokemonInPlay(
            id=active_card_two.id, 
            hp=int(card_map[active_card_two.id].get('hp', 0))
        ) if active_card_two else None,
        hand=cards_two[:6],  # First 6 cards in hand
        prizeCards=cards_two[6:12] if len(cards_two) >= 12 else [],  # Next 6 cards as prize cards
        deck=cards_two[12:],  # Remaining cards in deck
        bench=[],  # Empty bench
        discard=[],  # Empty discard pile
        lostZone=[],  # Empty lost zone
        stadium=None  # No stadium card
    )
    
    # Create board state with both player states and include the combined card map
    return BoardState(
        playerOne=player_state,
        playerTwo=player_two_state,
        cardMap=card_map
    ) 