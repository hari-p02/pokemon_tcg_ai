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

def get_initial_state(deck: List[dict]) -> BoardState:
    # Create a mapping of card IDs to card info
    card_map = get_card_map(deck)

    # Convert deck to Card objects with IDs
    cards = [Card(id=i) for i in range(len(deck))]
    
    # Shuffle the deck
    import random
    random.shuffle(cards)
    
    # Find a basic Pokemon for active
    active_card = None
    for card in cards:
        card_info = card_map[card.id]
        if card_info.get('supertype') == 'Pokémon' and 'Basic' in card_info.get('subtypes', []):
            active_card = card
            cards.remove(card)
            break
    
    # If we didn't find a basic Pokemon, just use the first card (this is just for testing)
    if active_card is None and cards:
        active_card = cards[0]
        cards.remove(active_card)
    
    # Initialize player state with simplified structure
    player_state = PlayerState(
        active=PokemonInPlay(
            id=active_card.id, 
            hp=int(card_map[active_card.id].get('hp', 0))
        ) if active_card else None,
        hand=cards[:6],  # First 6 cards in hand
        prizeCards=cards[6:12] if len(cards) >= 12 else [],  # Next 6 cards as prize cards
        deck=cards[12:],  # Remaining cards in deck
        bench=[],  # Empty bench
        discard=[],  # Empty discard pile
        lostZone=[],  # Empty lost zone
        stadium=None  # No stadium card
    )
    
    # Create player two state with a different shuffle
    player_two_cards = [Card(id=i) for i in range(len(deck))]
    random.shuffle(player_two_cards)
    
    # Find a basic Pokemon for active for player two
    active_card_two = None
    for card in player_two_cards:
        card_info = card_map[card.id]
        if card_info.get('supertype') == 'Pokémon' and 'Basic' in card_info.get('subtypes', []):
            active_card_two = card
            player_two_cards.remove(card)
            break
    
    # If we didn't find a basic Pokemon, just use the first card (this is just for testing)
    if active_card_two is None and player_two_cards:
        active_card_two = player_two_cards[0]
        player_two_cards.remove(active_card_two)
    
    # Initialize player two state with simplified structure
    player_two_state = PlayerState(
        active=PokemonInPlay(
            id=active_card_two.id, 
            hp=int(card_map[active_card_two.id].get('hp', 0))
        ) if active_card_two else None,
        hand=player_two_cards[:6],  # First 6 cards in hand
        prizeCards=player_two_cards[6:12] if len(player_two_cards) >= 12 else [],  # Next 6 cards as prize cards
        deck=player_two_cards[12:],  # Remaining cards in deck
        bench=[],  # Empty bench
        discard=[],  # Empty discard pile
        lostZone=[],  # Empty lost zone
        stadium=None  # No stadium card
    )
    
    # Create board state with both player states and include the card map
    return BoardState(
        playerOne=player_state,
        playerTwo=player_two_state,
        cardMap=card_map
    ) 