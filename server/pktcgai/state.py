from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Card:
    info: dict

@dataclass
class PokemonInPlay:
    info: dict
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

def get_initial_state(deck: List[dict]) -> BoardState:
    # Convert deck to Card objects
    cards = [Card(info=card) for card in deck]
    
    # Shuffle the deck
    import random
    random.shuffle(cards)
    
    # Initialize player state
    player_state = PlayerState(
        hand=cards[:7],  # First 7 cards in hand
        active=PokemonInPlay(info=cards[7].info, hp=int(cards[7].info.get('hp', 0))) if len(cards) > 7 else None,  # 8th card as active
        bench=[PokemonInPlay(info=card.info, hp=int(card.info.get('hp', 0))) for card in cards[8:11]] if len(cards) > 11 else [],  # Next 3 cards on bench
        prizeCards=cards[11:17] if len(cards) > 17 else [],  # Next 6 cards as prize cards
        deck=cards[17:] if len(cards) > 17 else [],  # Remaining cards in deck
        discard=[],
        lostZone=[],
        stadium=None
    )
    
    # Create board state with same state for both players
    return BoardState(
        playerOne=player_state,
        playerTwo=player_state
    ) 