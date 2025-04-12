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
    
    # Find basic Pokemon for bench
    bench_cards = []
    for card in cards[:]:
        card_info = card_map[card.id]
        if card_info.get('supertype') == 'Pokémon' and 'Basic' in card_info.get('subtypes', []):
            bench_cards.append(card)
            cards.remove(card)
            if len(bench_cards) == 3:  # We want 3 Pokemon on bench
                break
    
    # Find energy cards to attach to bench Pokemon
    energy_cards = []
    for card in cards[:]:
        card_info = card_map[card.id]
        if card_info.get('supertype') == 'Energy':
            energy_cards.append(card)
            cards.remove(card)
            if len(energy_cards) == 3:  # One energy per bench Pokemon
                break
    
    # Attach energy to bench Pokemon
    bench_pokemon = []
    for i, pokemon in enumerate(bench_cards):
        attached_energy = [energy_cards[i]] if i < len(energy_cards) else []
        card_info = card_map[pokemon.id]
        bench_pokemon.append(PokemonInPlay(
            id=pokemon.id,
            hp=int(card_info.get('hp', 0)),
            attachedCards=attached_energy
        ))
    
    # Find a stadium card
    stadium_card = None
    for card in cards[:]:
        card_info = card_map[card.id]
        if card_info.get('supertype') == 'Trainer' and 'Stadium' in card_info.get('subtypes', []):
            stadium_card = card
            cards.remove(card)
            break
    
    # Initialize player state with the organized cards
    player_state = PlayerState(
        hand=cards[:7],  # First 7 cards in hand
        active=PokemonInPlay(
            id=active_card.id, 
            hp=int(card_map[active_card.id].get('hp', 0))
        ) if active_card else None,
        bench=bench_pokemon,
        prizeCards=cards[7:13] if len(cards) > 13 else [],  # Next 6 cards as prize cards
        deck=cards[13:],  # Remaining cards in deck
        discard=[cards[0]] if len(cards) > 0 else [],  # One card in discard
        lostZone=[cards[1]] if len(cards) > 1 else [],  # One card in lost zone
        stadium=stadium_card
    )
    
    # Create board state with same state for both players and include the card map
    return BoardState(
        playerOne=player_state,
        playerTwo=player_state,
        cardMap=card_map
    ) 