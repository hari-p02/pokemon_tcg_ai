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

def get_initial_state(deck_one: List[dict], deck_two: List[dict], isPreset: bool = False) -> BoardState:
    # Create a mapping of card IDs to card info for both decks
    card_map_one = get_card_map(deck_one)
    card_map_two = get_card_map(deck_two)
    
    # Combine both card maps
    card_map = {**card_map_one, **{k + len(deck_one): v for k, v in card_map_two.items()}}
    
    # Convert decks to Card objects with IDs
    cards_one = [Card(id=i) for i in range(len(deck_one))]
    cards_two = [Card(id=i + len(deck_one)) for i in range(len(deck_two))]  # Offset IDs for second deck
    
    if isPreset:
        # Find specific cards for player one's preset state
        zacian_v = None
        battle_vip_pass = None
        psychic_energies = []
        cresselia = None
        gardevoir_ex = None
        ralts = None
        
        for card in cards_one:
            card_info = card_map[card.id]
            if card_info.get('name') == 'Zacian V':
                zacian_v = card
            elif card_info.get('name') == 'Battle VIP Pass':
                battle_vip_pass = card
            elif card_info.get('name') == 'Basic Psychic Energy':
                psychic_energies.append(card)
            elif card_info.get('name') == 'Cresselia':
                cresselia = card
            elif card_info.get('name') == 'Gardevoir ex':
                gardevoir_ex = card
            elif card_info.get('name') == 'Ralts':
                ralts = card
        # Remove preset cards from deck
        preset_cards = [zacian_v, battle_vip_pass, cresselia, gardevoir_ex] + psychic_energies[:2]
        for card in preset_cards:
            if card in cards_one:
                cards_one.remove(card)
        
        # Find specific cards for player two's preset state
        pikachu_ex = None
        pikachu_v = None
        charizard_ex = None
        cheren = None
        lightning_energies = []
        fire_energy = None
        
        for card in cards_two:
            card_info = card_map[card.id]
            if card_info.get('name') == 'Pikachu-EX':
                pikachu_ex = card
            elif card_info.get('name') == 'Pikachu V':
                pikachu_v = card
            elif card_info.get('name') == 'Charizard-EX':
                charizard_ex = card
            elif card_info.get('name') == 'Cheren':
                cheren = card
            elif card_info.get('name') == 'Basic Lightning Energy':
                lightning_energies.append(card)
            elif card_info.get('name') == 'Fire Energy':
                fire_energy = card
        
        # Remove preset cards from deck
        preset_cards = [pikachu_ex, pikachu_v, charizard_ex, cheren] + lightning_energies[:2] + [fire_energy]
        for card in preset_cards:
            if card in cards_two:
                cards_two.remove(card)
        
        # Shuffle remaining cards
        import random
        random.shuffle(cards_one)
        random.shuffle(cards_two)
        
        # Set up player one's preset state
        player_state = PlayerState(
            active=PokemonInPlay(
                id=zacian_v.id,
                hp=int(card_map[zacian_v.id].get('hp', 0))
            ) if zacian_v else None,
            hand=[battle_vip_pass] + psychic_energies[:2] + [cresselia, gardevoir_ex, ralts] if all([battle_vip_pass, cresselia, gardevoir_ex, ralts]) else [],
            prizeCards=cards_one[:6] if len(cards_one) >= 6 else [],
            deck=cards_one[6:],
            bench=[],
            discard=[],
            lostZone=[],
            stadium=None
        )
        
        # Set up player two's preset state
        player_two_state = PlayerState(
            active=PokemonInPlay(
                id=pikachu_ex.id,
                hp=int(card_map[pikachu_ex.id].get('hp', 0))
            ) if pikachu_ex else None,
            hand=[pikachu_v, charizard_ex, cheren] + lightning_energies[:2] + [fire_energy] if all([pikachu_v, charizard_ex, cheren, fire_energy]) else [],
            prizeCards=cards_two[:6] if len(cards_two) >= 6 else [],
            deck=cards_two[6:],
            bench=[],
            discard=[],
            lostZone=[],
            stadium=None
        )
    else:
        # Original random setup logic
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