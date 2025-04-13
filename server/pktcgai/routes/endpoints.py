from fastapi import APIRouter, Response, BackgroundTasks
from fastapi.responses import StreamingResponse
import json
import asyncio
from ..state import get_initial_state, BoardState, PlayerState, PokemonInPlay, Card
from pktcgai.graph.pokemon_tcg_graph import run_pokemon_tcg_turn, transform_game_state
from typing import Dict, List, Any, Optional
from dataclasses import asdict
import io
import sys
import contextlib
import queue
import threading

router = APIRouter()

# Create a thread-safe queue for real-time streaming
stream_queue = queue.Queue()

# Global state that will be updated by player actions
state = None

PIKACHU_DECK = [
  {
    "name": "Flying Pikachu V",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic",
      "V"
    ],
    "hp": "190",
    "types": [
      "Lightning"
    ],
    "attacks": [
      {
        "cost": [
          "Lightning"
        ],
        "name": "Thunder Shock",
        "damage": "20",
        "text": "Flip a coin. If heads, your opponent's Active Pokémon is now Paralyzed.",
        "convertedEnergyCost": 1
      },
      {
        "cost": [
          "Colorless",
          "Colorless",
          "Colorless"
        ],
        "name": "Fly",
        "damage": "120",
        "text": "Flip a coin. If tails, this attack does nothing. If heads, during your opponent's next turn, prevent all damage from and effects of attacks done to this Pokémon.",
        "convertedEnergyCost": 3
      }
    ],
    "weaknesses": [
      {
        "type": "Lightning",
        "value": "×2"
      }
    ],
    "evolvesTo": [
      "Raichu"
    ],
    "rules": [
      "V rule: When your Pokémon V is Knocked Out, your opponent takes 2 Prize cards."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/cel25/6_hires.png"
    }
  },
  {
    "name": "Pikachu V",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic",
      "V"
    ],
    "hp": "190",
    "types": [
      "Lightning"
    ],
    "attacks": [
      {
        "name": "Charge",
        "cost": [
          "Lightning"
        ],
        "convertedEnergyCost": 1,
        "damage": "",
        "text": "Search your deck for up to 2 Lightning Energy cards and attach them to this Pokémon. Then, shuffle your deck."
      },
      {
        "name": "Thunderbolt",
        "cost": [
          "Lightning",
          "Lightning",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "200",
        "text": "Discard all Energy from this Pokémon."
      }
    ],
    "weaknesses": [
      {
        "type": "Fighting",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "evolvesTo": [
      "Raichu"
    ],
    "rules": [
      "V rule: When your Pokémon V is Knocked Out, your opponent takes 2 Prize cards."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swshp/SWSH061_hires.png"
    }
  },
  {
    "name": "Pikachu V",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic",
      "V"
    ],
    "hp": "190",
    "types": [
      "Lightning"
    ],
    "attacks": [
      {
        "name": "Charge",
        "cost": [
          "Lightning"
        ],
        "convertedEnergyCost": 1,
        "damage": "",
        "text": "Search your deck for up to 2 Lightning Energy cards and attach them to this Pokémon. Then, shuffle your deck."
      },
      {
        "name": "Thunderbolt",
        "cost": [
          "Lightning",
          "Lightning",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "200",
        "text": "Discard all Energy from this Pokémon."
      }
    ],
    "weaknesses": [
      {
        "type": "Fighting",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "evolvesTo": [
      "Raichu"
    ],
    "rules": [
      "V rule: When your Pokémon V is Knocked Out, your opponent takes 2 Prize cards."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh4/43_hires.png"
    }
  },
  {
    "name": "Pikachu V",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic",
      "V"
    ],
    "hp": "200",
    "types": [
      "Lightning"
    ],
    "attacks": [
      {
        "name": "Tail Whap",
        "cost": [
          "Colorless"
        ],
        "convertedEnergyCost": 1,
        "damage": "20",
        "text": ""
      },
      {
        "name": "Thunderbolt",
        "cost": [
          "Lightning",
          "Colorless",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "100",
        "text": ""
      }
    ],
    "weaknesses": [
      {
        "type": "Fighting",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "evolvesTo": [
      "Raichu"
    ],
    "rules": [
      "V rule: When your Pokémon V is Knocked Out, your opponent takes 2 Prize cards."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh8/86_hires.png"
    }
  },
  {
    "name": "Pikachu-EX",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic",
      "EX"
    ],
    "hp": "130",
    "types": [
      "Lightning"
    ],
    "attacks": [
      {
        "name": "Thunder Shock",
        "cost": [
          "Lightning",
          "Colorless"
        ],
        "convertedEnergyCost": 2,
        "damage": "30",
        "text": "Flip a coin. If heads your opponent's Active Pokémon is now Paralyzed."
      },
      {
        "name": "Mega Thunderbolt",
        "cost": [
          "Lightning",
          "Lightning",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "160",
        "text": "Discard all Energy attached to this Pokémon."
      }
    ],
    "weaknesses": [
      {
        "type": "Fighting",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "evolvesTo": [
      "Raichu"
    ],
    "rules": [
      "Pokémon-EX rule: When a Pokémon-EX has been Knocked Out, your opponent takes 2 Prize cards."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/xyp/XY174_hires.png"
    }
  },
  {
    "name": "Basic Lightning Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv1/257_hires.png"
    }
  },
  {
    "name": "Basic Lightning Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv1/257_hires.png"
    }
  },
  {
    "name": "Basic Lightning Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv1/257_hires.png"
    }
  },
  {
    "name": "Basic Lightning Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv1/257_hires.png"
    }
  },
  {
    "name": "Basic Lightning Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv1/257_hires.png"
    }
  },
  {
    "name": "Basic Lightning Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv1/257_hires.png"
    }
  },
  {
    "name": "Cheren",
    "supertype": "Trainer",
    "subtypes": [
      "Supporter"
    ],
    "rules": [
      "Draw 3 cards.",
      "You may play only 1 Supporter card during your turn (before your attack)."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/bw5/91_hires.png"
    }
  },
  {
    "name": "Cheren",
    "supertype": "Trainer",
    "subtypes": [
      "Supporter"
    ],
    "rules": [
      "Draw 3 cards.",
      "You may play only 1 Supporter card during your turn (before your attack)."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/bw5/91_hires.png"
    }
  },
  {
    "name": "Cheren",
    "supertype": "Trainer",
    "subtypes": [
      "Supporter"
    ],
    "rules": [
      "Draw 3 cards.",
      "You may play only 1 Supporter card during your turn (before your attack)."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/bw5/91_hires.png"
    }
  },
  {
    "name": "Cheren",
    "supertype": "Trainer",
    "subtypes": [
      "Supporter"
    ],
    "rules": [
      "Draw 3 cards.",
      "You may play only 1 Supporter card during your turn (before your attack)."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/bw5/91_hires.png"
    }
  },
  {
    "name": "Nest Ball",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Search your deck for a Basic Pokémon and put it onto your Bench. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv4pt5/84_hires.png"
    }
  },
  {
    "name": "Nest Ball",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Search your deck for a Basic Pokémon and put it onto your Bench. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv4pt5/84_hires.png"
    }
  },
  {
    "name": "Nest Ball",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Search your deck for a Basic Pokémon and put it onto your Bench. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv4pt5/84_hires.png"
    }
  },
  {
    "name": "Nest Ball",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Search your deck for a Basic Pokémon and put it onto your Bench. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv4pt5/84_hires.png"
    }
  },
  {
    "name": "Flash Energy",
    "supertype": "Energy",
    "subtypes": [
      "Special"
    ],
    "rules": [
      "This card can only be attached to Lightning Pokémon. This card provides Lightning Energy only while this card is attached to a Lightning Pokémon.",
      "The Lightning Pokémon this card is attached to has no Weakness.",
      "(If this card is attached to anything other than a Lightning Pokémon, discard this card.)"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/xy7/83_hires.png"
    }
  },
  {
    "name": "Flash Energy",
    "supertype": "Energy",
    "subtypes": [
      "Special"
    ],
    "rules": [
      "This card can only be attached to Lightning Pokémon. This card provides Lightning Energy only while this card is attached to a Lightning Pokémon.",
      "The Lightning Pokémon this card is attached to has no Weakness.",
      "(If this card is attached to anything other than a Lightning Pokémon, discard this card.)"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/xy7/83_hires.png"
    }
  },
  {
    "name": "Flash Energy",
    "supertype": "Energy",
    "subtypes": [
      "Special"
    ],
    "rules": [
      "This card can only be attached to Lightning Pokémon. This card provides Lightning Energy only while this card is attached to a Lightning Pokémon.",
      "The Lightning Pokémon this card is attached to has no Weakness.",
      "(If this card is attached to anything other than a Lightning Pokémon, discard this card.)"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/xy7/83_hires.png"
    }
  },
  {
    "name": "Charmander",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic"
    ],
    "hp": "70",
    "types": [
      "Fire"
    ],
    "attacks": [
      {
        "name": "Gnaw",
        "cost": [
          "Fire"
        ],
        "convertedEnergyCost": 1,
        "damage": "10",
        "text": ""
      },
      {
        "name": "Flare",
        "cost": [
          "Fire",
          "Colorless"
        ],
        "convertedEnergyCost": 2,
        "damage": "20",
        "text": ""
      }
    ],
    "weaknesses": [
      {
        "type": "Water",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "evolvesTo": [
      "Charmeleon"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sm115/7_hires.png"
    }
  },
  {
    "name": "Charmander",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic"
    ],
    "hp": "70",
    "types": [
      "Fire"
    ],
    "attacks": [
      {
        "name": "Gnaw",
        "cost": [
          "Fire"
        ],
        "convertedEnergyCost": 1,
        "damage": "10",
        "text": ""
      },
      {
        "name": "Flare",
        "cost": [
          "Fire",
          "Colorless"
        ],
        "convertedEnergyCost": 2,
        "damage": "20",
        "text": ""
      }
    ],
    "weaknesses": [
      {
        "type": "Water",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "evolvesTo": [
      "Charmeleon"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sm115/7_hires.png"
    }
  },
  {
    "name": "Charmander",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic"
    ],
    "hp": "70",
    "types": [
      "Fire"
    ],
    "attacks": [
      {
        "name": "Gnaw",
        "cost": [
          "Fire"
        ],
        "convertedEnergyCost": 1,
        "damage": "10",
        "text": ""
      },
      {
        "name": "Flare",
        "cost": [
          "Fire",
          "Colorless"
        ],
        "convertedEnergyCost": 2,
        "damage": "20",
        "text": ""
      }
    ],
    "weaknesses": [
      {
        "type": "Water",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "evolvesTo": [
      "Charmeleon"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sm115/7_hires.png"
    }
  },
  {
    "name": "Charmander",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic"
    ],
    "hp": "70",
    "types": [
      "Fire"
    ],
    "attacks": [
      {
        "name": "Gnaw",
        "cost": [
          "Fire"
        ],
        "convertedEnergyCost": 1,
        "damage": "10",
        "text": ""
      },
      {
        "name": "Flare",
        "cost": [
          "Fire",
          "Colorless"
        ],
        "convertedEnergyCost": 2,
        "damage": "20",
        "text": ""
      }
    ],
    "weaknesses": [
      {
        "type": "Water",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "evolvesTo": [
      "Charmeleon"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sm115/7_hires.png"
    }
  },
  {
    "name": "Charmander",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic"
    ],
    "hp": "70",
    "types": [
      "Fire"
    ],
    "attacks": [
      {
        "name": "Gnaw",
        "cost": [
          "Fire"
        ],
        "convertedEnergyCost": 1,
        "damage": "10",
        "text": ""
      },
      {
        "name": "Flare",
        "cost": [
          "Fire",
          "Colorless"
        ],
        "convertedEnergyCost": 2,
        "damage": "20",
        "text": ""
      }
    ],
    "weaknesses": [
      {
        "type": "Water",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "evolvesTo": [
      "Charmeleon"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sm115/7_hires.png"
    }
  },
  {
    "name": "Fire Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh12pt5/153_hires.png"
    }
  },
  {
    "name": "Fire Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh12pt5/153_hires.png"
    }
  },
  {
    "name": "Fire Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh12pt5/153_hires.png"
    }
  },
  {
    "name": "Fire Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh12pt5/153_hires.png"
    }
  },
  {
    "name": "Hau",
    "supertype": "Trainer",
    "subtypes": [
      "Supporter"
    ],
    "rules": [
      "Draw 3 cards.",
      "You may play only 1 Supporter card during your turn (before your attack)."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sm7/132_hires.png"
    }
  },
  {
    "name": "Hau",
    "supertype": "Trainer",
    "subtypes": [
      "Supporter"
    ],
    "rules": [
      "Draw 3 cards.",
      "You may play only 1 Supporter card during your turn (before your attack)."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sm7/132_hires.png"
    }
  },
  {
    "name": "Hau",
    "supertype": "Trainer",
    "subtypes": [
      "Supporter"
    ],
    "rules": [
      "Draw 3 cards.",
      "You may play only 1 Supporter card during your turn (before your attack)."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sm7/132_hires.png"
    }
  },
  {
    "name": "Hau",
    "supertype": "Trainer",
    "subtypes": [
      "Supporter"
    ],
    "rules": [
      "Draw 3 cards.",
      "You may play only 1 Supporter card during your turn (before your attack)."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sm7/132_hires.png"
    }
  },
  {
    "name": "Quick Ball",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "You can play this card only if you discard another card from your hand.",
      "Search your deck for a Basic Pokémon, reveal it, and put it into your hand. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh1/179_hires.png"
    }
  },
  {
    "name": "Quick Ball",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "You can play this card only if you discard another card from your hand.",
      "Search your deck for a Basic Pokémon, reveal it, and put it into your hand. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh1/179_hires.png"
    }
  },
  {
    "name": "Quick Ball",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "You can play this card only if you discard another card from your hand.",
      "Search your deck for a Basic Pokémon, reveal it, and put it into your hand. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh1/179_hires.png"
    }
  },
  {
    "name": "Quick Ball",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "You can play this card only if you discard another card from your hand.",
      "Search your deck for a Basic Pokémon, reveal it, and put it into your hand. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh1/179_hires.png"
    }
  },
  {
    "name": "Flying Pikachu V",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic",
      "V"
    ],
    "hp": "190",
    "types": [
      "Lightning"
    ],
    "attacks": [
      {
        "cost": [
          "Lightning"
        ],
        "name": "Thunder Shock",
        "damage": "20",
        "text": "Flip a coin. If heads, your opponent's Active Pokémon is now Paralyzed.",
        "convertedEnergyCost": 1
      },
      {
        "cost": [
          "Colorless",
          "Colorless",
          "Colorless"
        ],
        "name": "Fly",
        "damage": "120",
        "text": "Flip a coin. If tails, this attack does nothing. If heads, during your opponent's next turn, prevent all damage from and effects of attacks done to this Pokémon.",
        "convertedEnergyCost": 3
      }
    ],
    "weaknesses": [
      {
        "type": "Lightning",
        "value": "×2"
      }
    ],
    "evolvesTo": [
      "Raichu"
    ],
    "rules": [
      "V rule: When your Pokémon V is Knocked Out, your opponent takes 2 Prize cards."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/cel25/6_hires.png"
    }
  },
  {
    "name": "Flying Pikachu V",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic",
      "V"
    ],
    "hp": "190",
    "types": [
      "Lightning"
    ],
    "attacks": [
      {
        "cost": [
          "Lightning"
        ],
        "name": "Thunder Shock",
        "damage": "20",
        "text": "Flip a coin. If heads, your opponent's Active Pokémon is now Paralyzed.",
        "convertedEnergyCost": 1
      },
      {
        "cost": [
          "Colorless",
          "Colorless",
          "Colorless"
        ],
        "name": "Fly",
        "damage": "120",
        "text": "Flip a coin. If tails, this attack does nothing. If heads, during your opponent's next turn, prevent all damage from and effects of attacks done to this Pokémon.",
        "convertedEnergyCost": 3
      }
    ],
    "weaknesses": [
      {
        "type": "Lightning",
        "value": "×2"
      }
    ],
    "evolvesTo": [
      "Raichu"
    ],
    "rules": [
      "V rule: When your Pokémon V is Knocked Out, your opponent takes 2 Prize cards."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/cel25/6_hires.png"
    }
  },
  {
    "name": "Pikachu V",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic",
      "V"
    ],
    "hp": "200",
    "types": [
      "Lightning"
    ],
    "attacks": [
      {
        "name": "Tail Whap",
        "cost": [
          "Colorless"
        ],
        "convertedEnergyCost": 1,
        "damage": "20",
        "text": ""
      },
      {
        "name": "Thunderbolt",
        "cost": [
          "Lightning",
          "Colorless",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "100",
        "text": ""
      }
    ],
    "weaknesses": [
      {
        "type": "Fighting",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "evolvesTo": [
      "Raichu"
    ],
    "rules": [
      "V rule: When your Pokémon V is Knocked Out, your opponent takes 2 Prize cards."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh8/86_hires.png"
    }
  },
  {
    "name": "Pikachu V",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic",
      "V"
    ],
    "hp": "190",
    "types": [
      "Lightning"
    ],
    "attacks": [
      {
        "name": "Charge",
        "cost": [
          "Lightning"
        ],
        "convertedEnergyCost": 1,
        "damage": "",
        "text": "Search your deck for up to 2 Lightning Energy cards and attach them to this Pokémon. Then, shuffle your deck."
      },
      {
        "name": "Thunderbolt",
        "cost": [
          "Lightning",
          "Lightning",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "200",
        "text": "Discard all Energy from this Pokémon."
      }
    ],
    "weaknesses": [
      {
        "type": "Fighting",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "evolvesTo": [
      "Raichu"
    ],
    "rules": [
      "V rule: When your Pokémon V is Knocked Out, your opponent takes 2 Prize cards."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh4/43_hires.png"
    }
  },
  {
    "name": "Pikachu-EX",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic",
      "EX"
    ],
    "hp": "130",
    "types": [
      "Lightning"
    ],
    "attacks": [
      {
        "name": "Thunder Shock",
        "cost": [
          "Lightning",
          "Colorless"
        ],
        "convertedEnergyCost": 2,
        "damage": "30",
        "text": "Flip a coin. If heads your opponent's Active Pokémon is now Paralyzed."
      },
      {
        "name": "Mega Thunderbolt",
        "cost": [
          "Lightning",
          "Lightning",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "160",
        "text": "Discard all Energy attached to this Pokémon."
      }
    ],
    "weaknesses": [
      {
        "type": "Fighting",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "evolvesTo": [
      "Raichu"
    ],
    "rules": [
      "Pokémon-EX rule: When a Pokémon-EX has been Knocked Out, your opponent takes 2 Prize cards."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/xyp/XY174_hires.png"
    }
  },
  {
    "name": "Potion",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Heal 30 damage from 1 of your Pokémon.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh12pt5/139_hires.png"
    }
  },
  {
    "name": "Potion",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Heal 30 damage from 1 of your Pokémon.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh12pt5/139_hires.png"
    }
  },
  {
    "name": "Potion",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Heal 30 damage from 1 of your Pokémon.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh12pt5/139_hires.png"
    }
  },
  {
    "name": "Potion",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Heal 30 damage from 1 of your Pokémon.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh12pt5/139_hires.png"
    }
  },
  {
    "name": "Super Potion",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Heal 60 damage from 1 of your Pokémon. If you do, discard an Energy attached to that Pokémon.",
      "You may play as many Item cards as you like during your turn (before your attack)."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/xy1/128_hires.png"
    }
  },
  {
    "name": "Super Potion",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Heal 60 damage from 1 of your Pokémon. If you do, discard an Energy attached to that Pokémon.",
      "You may play as many Item cards as you like during your turn (before your attack)."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/xy1/128_hires.png"
    }
  },
  {
    "name": "Super Potion",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Heal 60 damage from 1 of your Pokémon. If you do, discard an Energy attached to that Pokémon.",
      "You may play as many Item cards as you like during your turn (before your attack)."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/xy1/128_hires.png"
    }
  },
  {
    "name": "Charizard V",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic",
      "V"
    ],
    "hp": "220",
    "types": [
      "Fire"
    ],
    "attacks": [
      {
        "name": "Incinerate",
        "cost": [
          "Fire",
          "Fire",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "90",
        "text": "Before doing damage, discard all Pokémon Tools from your opponent's Active Pokémon."
      },
      {
        "name": "Heat Blast",
        "cost": [
          "Fire",
          "Fire",
          "Fire",
          "Colorless"
        ],
        "convertedEnergyCost": 4,
        "damage": "180",
        "text": ""
      }
    ],
    "weaknesses": [
      {
        "type": "Water",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless",
      "Colorless"
    ],
    "convertedRetreatCost": 2,
    "rules": [
      "V rule: When your Pokémon V is Knocked Out, your opponent takes 2 Prize cards."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh12pt5/18_hires.png"
    }
  },
  {
    "name": "Charizard V",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic",
      "V"
    ],
    "hp": "220",
    "types": [
      "Fire"
    ],
    "attacks": [
      {
        "name": "Incinerate",
        "cost": [
          "Fire",
          "Fire",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "90",
        "text": "Before doing damage, discard all Pokémon Tools from your opponent's Active Pokémon."
      },
      {
        "name": "Heat Blast",
        "cost": [
          "Fire",
          "Fire",
          "Fire",
          "Colorless"
        ],
        "convertedEnergyCost": 4,
        "damage": "180",
        "text": ""
      }
    ],
    "weaknesses": [
      {
        "type": "Water",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless",
      "Colorless"
    ],
    "convertedRetreatCost": 2,
    "rules": [
      "V rule: When your Pokémon V is Knocked Out, your opponent takes 2 Prize cards."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh12pt5/18_hires.png"
    }
  },
  {
    "name": "Charizard V",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic",
      "V"
    ],
    "hp": "220",
    "types": [
      "Fire"
    ],
    "attacks": [
      {
        "name": "Incinerate",
        "cost": [
          "Fire",
          "Fire",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "90",
        "text": "Before doing damage, discard all Pokémon Tools from your opponent's Active Pokémon."
      },
      {
        "name": "Heat Blast",
        "cost": [
          "Fire",
          "Fire",
          "Fire",
          "Colorless"
        ],
        "convertedEnergyCost": 4,
        "damage": "180",
        "text": ""
      }
    ],
    "weaknesses": [
      {
        "type": "Water",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless",
      "Colorless"
    ],
    "convertedRetreatCost": 2,
    "rules": [
      "V rule: When your Pokémon V is Knocked Out, your opponent takes 2 Prize cards."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh12pt5/18_hires.png"
    }
  },
  {
    "name": "Charizard-EX",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic",
      "EX"
    ],
    "hp": "180",
    "types": [
      "Fire"
    ],
    "attacks": [
      {
        "name": "Wing Attack",
        "cost": [
          "Colorless",
          "Colorless",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "60",
        "text": ""
      },
      {
        "name": "Combustion Blast",
        "cost": [
          "Fire",
          "Fire",
          "Colorless",
          "Colorless"
        ],
        "convertedEnergyCost": 4,
        "damage": "150",
        "text": "This Pokémon can't use Combustion Blast during your next turn."
      }
    ],
    "weaknesses": [
      {
        "type": "Water",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless",
      "Colorless"
    ],
    "convertedRetreatCost": 2,
    "evolvesTo": [
      "M Charizard-EX"
    ],
    "rules": [
      "Pokémon-EX rule: When a Pokémon-EX has been Knocked Out, your opponent takes 2 Prize cards."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/xy2/12_hires.png"
    }
  },
  {
    "name": "Charizard-EX",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic",
      "EX"
    ],
    "hp": "180",
    "types": [
      "Fire"
    ],
    "attacks": [
      {
        "name": "Wing Attack",
        "cost": [
          "Colorless",
          "Colorless",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "60",
        "text": ""
      },
      {
        "name": "Combustion Blast",
        "cost": [
          "Fire",
          "Fire",
          "Colorless",
          "Colorless"
        ],
        "convertedEnergyCost": 4,
        "damage": "150",
        "text": "This Pokémon can't use Combustion Blast during your next turn."
      }
    ],
    "weaknesses": [
      {
        "type": "Water",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless",
      "Colorless"
    ],
    "convertedRetreatCost": 2,
    "evolvesTo": [
      "M Charizard-EX"
    ],
    "rules": [
      "Pokémon-EX rule: When a Pokémon-EX has been Knocked Out, your opponent takes 2 Prize cards."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/xy2/12_hires.png"
    }
  },
  {
    "name": "Charizard-EX",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic",
      "EX"
    ],
    "hp": "180",
    "types": [
      "Fire"
    ],
    "attacks": [
      {
        "name": "Wing Attack",
        "cost": [
          "Colorless",
          "Colorless",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "60",
        "text": ""
      },
      {
        "name": "Combustion Blast",
        "cost": [
          "Fire",
          "Fire",
          "Colorless",
          "Colorless"
        ],
        "convertedEnergyCost": 4,
        "damage": "150",
        "text": "This Pokémon can't use Combustion Blast during your next turn."
      }
    ],
    "weaknesses": [
      {
        "type": "Water",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless",
      "Colorless"
    ],
    "convertedRetreatCost": 2,
    "evolvesTo": [
      "M Charizard-EX"
    ],
    "rules": [
      "Pokémon-EX rule: When a Pokémon-EX has been Knocked Out, your opponent takes 2 Prize cards."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/xy2/12_hires.png"
    }
  },
  {
    "name": "Fire Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh12pt5/153_hires.png"
    }
  },
  {
    "name": "Fire Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh12pt5/153_hires.png"
    }
  },
  {
    "name": "Fire Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh12pt5/153_hires.png"
    }
  }
]

GARDEVOIR_DECK = [
  {
    "name": "Ralts",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic"
    ],
    "hp": "70",
    "types": [
      "Psychic"
    ],
    "attacks": [
      {
        "name": "Teleportation Burst",
        "cost": [
          "Psychic"
        ],
        "convertedEnergyCost": 1,
        "damage": "10",
        "text": "Switch this Pokémon with 1 of your Benched Pokémon."
      }
    ],
    "weaknesses": [
      {
        "type": "Darkness",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "evolvesTo": [
      "Kirlia"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh10/60_hires.png"
    }
  },
  {
    "name": "Ralts",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic"
    ],
    "hp": "70",
    "types": [
      "Psychic"
    ],
    "attacks": [
      {
        "name": "Teleportation Burst",
        "cost": [
          "Psychic"
        ],
        "convertedEnergyCost": 1,
        "damage": "10",
        "text": "Switch this Pokémon with 1 of your Benched Pokémon."
      }
    ],
    "weaknesses": [
      {
        "type": "Darkness",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "evolvesTo": [
      "Kirlia"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh10/60_hires.png"
    }
  },
  {
    "name": "Ralts",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic"
    ],
    "hp": "70",
    "types": [
      "Psychic"
    ],
    "attacks": [
      {
        "name": "Teleportation Burst",
        "cost": [
          "Psychic"
        ],
        "convertedEnergyCost": 1,
        "damage": "10",
        "text": "Switch this Pokémon with 1 of your Benched Pokémon."
      }
    ],
    "weaknesses": [
      {
        "type": "Darkness",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "evolvesTo": [
      "Kirlia"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh10/60_hires.png"
    }
  },
  {
    "name": "Ralts",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic"
    ],
    "hp": "60",
    "types": [
      "Psychic"
    ],
    "attacks": [
      {
        "name": "Memory Skip",
        "cost": [
          "Psychic"
        ],
        "convertedEnergyCost": 1,
        "damage": "10",
        "text": "Choose 1 of your opponent's Active Pokémon's attacks. During your opponent's next turn, that Pokémon can't use that attack."
      }
    ],
    "weaknesses": [
      {
        "type": "Metal",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "evolvesTo": [
      "Kirlia"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh12/67_hires.png"
    }
  },
  {
    "name": "Kirlia",
    "supertype": "Pokémon",
    "subtypes": [
      "Stage 1"
    ],
    "hp": "80",
    "types": [
      "Psychic"
    ],
    "attacks": [
      {
        "name": "Slap",
        "cost": [
          "Psychic",
          "Colorless"
        ],
        "convertedEnergyCost": 2,
        "damage": "30",
        "text": ""
      }
    ],
    "weaknesses": [
      {
        "type": "Metal",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless",
      "Colorless"
    ],
    "convertedRetreatCost": 2,
    "evolvesFrom": "Ralts",
    "evolvesTo": [
      "Gardevoir",
      "Gallade"
    ],
    "abilities": [
      {
        "name": "Refinement",
        "text": "You must discard a card from your hand in order to use this Ability. Once during your turn, you may draw 2 cards.",
        "type": "Ability"
      }
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh12/68_hires.png"
    }
  },
  {
    "name": "Kirlia",
    "supertype": "Pokémon",
    "subtypes": [
      "Stage 1"
    ],
    "hp": "80",
    "types": [
      "Psychic"
    ],
    "attacks": [
      {
        "name": "Slap",
        "cost": [
          "Psychic",
          "Colorless"
        ],
        "convertedEnergyCost": 2,
        "damage": "30",
        "text": ""
      }
    ],
    "weaknesses": [
      {
        "type": "Metal",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless",
      "Colorless"
    ],
    "convertedRetreatCost": 2,
    "evolvesFrom": "Ralts",
    "evolvesTo": [
      "Gardevoir",
      "Gallade"
    ],
    "abilities": [
      {
        "name": "Refinement",
        "text": "You must discard a card from your hand in order to use this Ability. Once during your turn, you may draw 2 cards.",
        "type": "Ability"
      }
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh12/68_hires.png"
    }
  },
  {
    "name": "Kirlia",
    "supertype": "Pokémon",
    "subtypes": [
      "Stage 1"
    ],
    "hp": "80",
    "types": [
      "Psychic"
    ],
    "attacks": [
      {
        "name": "Slap",
        "cost": [
          "Psychic",
          "Colorless"
        ],
        "convertedEnergyCost": 2,
        "damage": "30",
        "text": ""
      }
    ],
    "weaknesses": [
      {
        "type": "Metal",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless",
      "Colorless"
    ],
    "convertedRetreatCost": 2,
    "evolvesFrom": "Ralts",
    "evolvesTo": [
      "Gardevoir",
      "Gallade"
    ],
    "abilities": [
      {
        "name": "Refinement",
        "text": "You must discard a card from your hand in order to use this Ability. Once during your turn, you may draw 2 cards.",
        "type": "Ability"
      }
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh12/68_hires.png"
    }
  },
  {
    "name": "Kirlia",
    "supertype": "Pokémon",
    "subtypes": [
      "Stage 1"
    ],
    "hp": "80",
    "types": [
      "Psychic"
    ],
    "attacks": [
      {
        "name": "Mirage Step",
        "cost": [
          "Psychic"
        ],
        "convertedEnergyCost": 1,
        "damage": "",
        "text": "Search your deck for up to 3 Kirlia and put them onto your Bench. Then, shuffle your deck."
      }
    ],
    "weaknesses": [
      {
        "type": "Metal",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "evolvesFrom": "Ralts",
    "evolvesTo": [
      "Gardevoir",
      "Gallade"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh6/60_hires.png"
    }
  },
  {
    "name": "Gardevoir ex",
    "supertype": "Pokémon",
    "subtypes": [
      "Stage 2",
      "ex"
    ],
    "hp": "310",
    "types": [
      "Psychic"
    ],
    "attacks": [
      {
        "name": "Miracle Force",
        "cost": [
          "Psychic",
          "Psychic",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "190",
        "text": "This Pokémon recovers from all Special Conditions."
      }
    ],
    "weaknesses": [
      {
        "type": "Darkness",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless",
      "Colorless"
    ],
    "convertedRetreatCost": 2,
    "evolvesFrom": "Kirlia",
    "rules": [
      "Pokémon ex rule: When your Pokémon ex is Knocked Out, your opponent takes 2 Prize cards."
    ],
    "abilities": [
      {
        "name": "Psychic Embrace",
        "text": "As often as you like during your turn, you may attach a Basic Psychic Energy card from your discard pile to 1 of your Psychic Pokémon. If you attached Energy to a Pokémon in this way, put 2 damage counters on that Pokémon. You can't use this Ability on a Pokémon that would be Knocked Out.",
        "type": "Ability"
      }
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv4pt5/29_hires.png"
    }
  },
  {
    "name": "Gardevoir ex",
    "supertype": "Pokémon",
    "subtypes": [
      "Stage 2",
      "ex"
    ],
    "hp": "310",
    "types": [
      "Psychic"
    ],
    "attacks": [
      {
        "name": "Miracle Force",
        "cost": [
          "Psychic",
          "Psychic",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "190",
        "text": "This Pokémon recovers from all Special Conditions."
      }
    ],
    "weaknesses": [
      {
        "type": "Darkness",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless",
      "Colorless"
    ],
    "convertedRetreatCost": 2,
    "evolvesFrom": "Kirlia",
    "rules": [
      "Pokémon ex rule: When your Pokémon ex is Knocked Out, your opponent takes 2 Prize cards."
    ],
    "abilities": [
      {
        "name": "Psychic Embrace",
        "text": "As often as you like during your turn, you may attach a Basic Psychic Energy card from your discard pile to 1 of your Psychic Pokémon. If you attached Energy to a Pokémon in this way, put 2 damage counters on that Pokémon. You can't use this Ability on a Pokémon that would be Knocked Out.",
        "type": "Ability"
      }
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv4pt5/29_hires.png"
    }
  },
  {
    "name": "Gardevoir",
    "supertype": "Pokémon",
    "subtypes": [
      "Stage 2"
    ],
    "hp": "140",
    "types": [
      "Psychic"
    ],
    "attacks": [
      {
        "name": "Brainwave",
        "cost": [
          "Colorless",
          "Colorless",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "60+",
        "text": "This attack does 30 more damage for each Psychic Energy attached to this Pokémon."
      }
    ],
    "weaknesses": [
      {
        "type": "Metal",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless",
      "Colorless"
    ],
    "convertedRetreatCost": 2,
    "evolvesFrom": "Kirlia",
    "abilities": [
      {
        "name": "Shining Arcana",
        "text": "Once during your turn, you may look at the top 2 cards of your deck and attach any number of basic Energy cards you find there to your Pokémon in any way you like. Put the other cards into your hand.",
        "type": "Ability"
      }
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh6/61_hires.png"
    }
  },
  {
    "name": "Gardevoir",
    "supertype": "Pokémon",
    "subtypes": [
      "Stage 2"
    ],
    "hp": "140",
    "types": [
      "Psychic"
    ],
    "attacks": [
      {
        "name": "Brainwave",
        "cost": [
          "Colorless",
          "Colorless",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "60+",
        "text": "This attack does 30 more damage for each Psychic Energy attached to this Pokémon."
      }
    ],
    "weaknesses": [
      {
        "type": "Metal",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless",
      "Colorless"
    ],
    "convertedRetreatCost": 2,
    "evolvesFrom": "Kirlia",
    "abilities": [
      {
        "name": "Shining Arcana",
        "text": "Once during your turn, you may look at the top 2 cards of your deck and attach any number of basic Energy cards you find there to your Pokémon in any way you like. Put the other cards into your hand.",
        "type": "Ability"
      }
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh6/61_hires.png"
    }
  },
  {
    "name": "Zacian V",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic",
      "V"
    ],
    "hp": "220",
    "types": [
      "Psychic"
    ],
    "attacks": [
      {
        "cost": [
          "Colorless",
          "Colorless",
          "Colorless"
        ],
        "name": "Storm Slash",
        "damage": "60+",
        "text": "This attack does 30 more damage for each Psychic Energy attached to this Pokémon.",
        "convertedEnergyCost": 3
      }
    ],
    "weaknesses": [
      {
        "type": "Metal",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless",
      "Colorless"
    ],
    "convertedRetreatCost": 2,
    "rules": [
      "V rule: When your Pokémon V is Knocked Out, your opponent takes 2 Prize cards."
    ],
    "abilities": [
      {
        "type": "Ability",
        "name": "Roar of the Sword",
        "text": "Once during your turn, you may search your deck for a Psychic Energy card and attach it to 1 of your Pokémon. Then, shuffle your deck. If you use this Ability, your turn ends."
      }
    ],
    "images": {
      "large": "https://images.pokemontcg.io/cel25/16_hires.png"
    }
  },
  {
    "name": "Cresselia",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic"
    ],
    "hp": "120",
    "types": [
      "Psychic"
    ],
    "attacks": [
      {
        "name": "Moonglow Reverse",
        "cost": [
          "Psychic"
        ],
        "convertedEnergyCost": 1,
        "damage": "",
        "text": "Move 2 damage counters from each of your Pokémon to 1 of your opponent's Pokémon."
      },
      {
        "name": "Lunar Blast",
        "cost": [
          "Psychic",
          "Psychic",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "110",
        "text": ""
      }
    ],
    "weaknesses": [
      {
        "type": "Darkness",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "images": {
      "large": "https://images.pokemontcg.io/swsh11/74_hires.png"
    }
  },
  {
    "name": "Mew",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic"
    ],
    "hp": "60",
    "types": [
      "Psychic"
    ],
    "attacks": [
      {
        "cost": [
          "Psychic",
          "Colorless"
        ],
        "name": "Psyshot",
        "damage": "30",
        "text": "",
        "convertedEnergyCost": 2
      }
    ],
    "weaknesses": [
      {
        "type": "Darkness",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "abilities": [
      {
        "type": "Ability",
        "name": "Mysterious Tail",
        "text": "Once during your turn, if this Pokémon is in the Active Spot, you may look at the top 6 cards of your deck, reveal an Item card you find there, and put it into your hand. Shuffle the other cards back into your deck."
      }
    ],
    "images": {
      "large": "https://images.pokemontcg.io/cel25/11_hires.png"
    }
  },
  {
    "name": "Radiant Greninja",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic",
      "Radiant"
    ],
    "hp": "130",
    "types": [
      "Water"
    ],
    "attacks": [
      {
        "name": "Moonlight Shuriken",
        "cost": [
          "Water",
          "Water",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "",
        "text": "Discard 2 Energy from this Pokémon. This attack does 90 damage to 2 of your opponent's Pokémon. (Don't apply Weakness and Resistance for Benched Pokémon.)"
      }
    ],
    "weaknesses": [
      {
        "type": "Lightning",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "rules": [
      "Radiant Pokémon Rule: You can't have more than 1 Radiant Pokémon in your deck."
    ],
    "abilities": [
      {
        "name": "Concealed Cards",
        "text": "You must discard an Energy card from your hand in order to use this Ability. Once during your turn, you may draw 2 cards.",
        "type": "Ability"
      }
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh10/46_hires.png"
    }
  },
  {
    "name": "Manaphy",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic"
    ],
    "hp": "70",
    "types": [
      "Water"
    ],
    "attacks": [
      {
        "name": "Rain Splash",
        "cost": [
          "Water"
        ],
        "convertedEnergyCost": 1,
        "damage": "20",
        "text": ""
      }
    ],
    "weaknesses": [
      {
        "type": "Lightning",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "abilities": [
      {
        "name": "Wave Veil",
        "text": "Prevent all damage done to your Benched Pokémon by attacks from your opponent's Pokémon.",
        "type": "Ability"
      }
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh9/41_hires.png"
    }
  },
  {
    "name": "Lumineon V",
    "supertype": "Pokémon",
    "subtypes": [
      "Basic",
      "V"
    ],
    "hp": "170",
    "types": [
      "Water"
    ],
    "attacks": [
      {
        "name": "Aqua Return",
        "cost": [
          "Water",
          "Colorless",
          "Colorless"
        ],
        "convertedEnergyCost": 3,
        "damage": "120",
        "text": "Shuffle this Pokémon and all attached cards into your deck."
      }
    ],
    "weaknesses": [
      {
        "type": "Lightning",
        "value": "×2"
      }
    ],
    "retreatCost": [
      "Colorless"
    ],
    "convertedRetreatCost": 1,
    "rules": [
      "V rule: When your Pokémon V is Knocked Out, your opponent takes 2 Prize cards."
    ],
    "abilities": [
      {
        "name": "Luminous Sign",
        "text": "When you play this Pokémon from your hand onto your Bench during your turn, you may search your deck for a Supporter card, reveal it, and put it into your hand. Then, shuffle your deck.",
        "type": "Ability"
      }
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh9/40_hires.png"
    }
  },
  {
    "name": "Iono",
    "supertype": "Trainer",
    "subtypes": [
      "Supporter"
    ],
    "rules": [
      "Each player shuffles their hand and puts it on the bottom of their deck. If either player put any cards on the bottom of their deck in this way, each player draws a card for each of their remaining Prize cards.",
      "You may play only 1 Supporter card during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv4pt5/80_hires.png"
    }
  },
  {
    "name": "Iono",
    "supertype": "Trainer",
    "subtypes": [
      "Supporter"
    ],
    "rules": [
      "Each player shuffles their hand and puts it on the bottom of their deck. If either player put any cards on the bottom of their deck in this way, each player draws a card for each of their remaining Prize cards.",
      "You may play only 1 Supporter card during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv4pt5/80_hires.png"
    }
  },
  {
    "name": "Iono",
    "supertype": "Trainer",
    "subtypes": [
      "Supporter"
    ],
    "rules": [
      "Each player shuffles their hand and puts it on the bottom of their deck. If either player put any cards on the bottom of their deck in this way, each player draws a card for each of their remaining Prize cards.",
      "You may play only 1 Supporter card during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv4pt5/80_hires.png"
    }
  },
  {
    "name": "Professor's Research",
    "supertype": "Trainer",
    "subtypes": [
      "Supporter"
    ],
    "rules": [
      "Discard your hand and draw 7 cards.",
      "You may play only 1 Supporter card during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv4pt5/87_hires.png"
    }
  },
  {
    "name": "Professor's Research",
    "supertype": "Trainer",
    "subtypes": [
      "Supporter"
    ],
    "rules": [
      "Discard your hand and draw 7 cards.",
      "You may play only 1 Supporter card during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv4pt5/87_hires.png"
    }
  },
  {
    "name": "Boss's Orders (Ghetsis)",
    "supertype": "Trainer",
    "subtypes": [
      "Supporter"
    ],
    "rules": [
      "Switch in 1 of your opponent's Benched Pokémon to the Active Spot.",
      "You may play only 1 Supporter card during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv2/172_hires.png"
    }
  },
  {
    "name": "Boss's Orders (Ghetsis)",
    "supertype": "Trainer",
    "subtypes": [
      "Supporter"
    ],
    "rules": [
      "Switch in 1 of your opponent's Benched Pokémon to the Active Spot.",
      "You may play only 1 Supporter card during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv2/172_hires.png"
    }
  },
  {
    "name": "Battle VIP Pass",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "You can use this card only during your first turn.",
      "Search your deck for up to 2 Basic Pokémon and put them onto your Bench. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh8/225_hires.png"
    }
  },
  {
    "name": "Battle VIP Pass",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "You can use this card only during your first turn.",
      "Search your deck for up to 2 Basic Pokémon and put them onto your Bench. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh8/225_hires.png"
    }
  },
  {
    "name": "Battle VIP Pass",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "You can use this card only during your first turn.",
      "Search your deck for up to 2 Basic Pokémon and put them onto your Bench. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh8/225_hires.png"
    }
  },
  {
    "name": "Battle VIP Pass",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "You can use this card only during your first turn.",
      "Search your deck for up to 2 Basic Pokémon and put them onto your Bench. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh8/225_hires.png"
    }
  },
  {
    "name": "Level Ball",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Search your deck for a Pokémon with 90 HP or less, reveal it, and put it into your hand. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh5/129_hires.png"
    }
  },
  {
    "name": "Level Ball",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Search your deck for a Pokémon with 90 HP or less, reveal it, and put it into your hand. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh5/129_hires.png"
    }
  },
  {
    "name": "Level Ball",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Search your deck for a Pokémon with 90 HP or less, reveal it, and put it into your hand. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh5/129_hires.png"
    }
  },
  {
    "name": "Level Ball",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Search your deck for a Pokémon with 90 HP or less, reveal it, and put it into your hand. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh5/129_hires.png"
    }
  },
  {
    "name": "Ultra Ball",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "You can use this card only if you discard 2 other cards from your hand. Search your deck for a Pokémon, reveal it, and put it into your hand. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv1/196_hires.png"
    }
  },
  {
    "name": "Ultra Ball",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "You can use this card only if you discard 2 other cards from your hand. Search your deck for a Pokémon, reveal it, and put it into your hand. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv1/196_hires.png"
    }
  },
  {
    "name": "Ultra Ball",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "You can use this card only if you discard 2 other cards from your hand. Search your deck for a Pokémon, reveal it, and put it into your hand. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv1/196_hires.png"
    }
  },
  {
    "name": "Rare Candy",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Choose 1 of your Basic Pokémon in play. If you have a Stage 2 card in your hand that evolves from that Pokémon, put that card onto the Basic Pokémon to evolve it, skipping the Stage 1. You can't use this card during your first turn or on a Basic Pokémon that was put into play this turn.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv1/191_hires.png"
    }
  },
  {
    "name": "Rare Candy",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Choose 1 of your Basic Pokémon in play. If you have a Stage 2 card in your hand that evolves from that Pokémon, put that card onto the Basic Pokémon to evolve it, skipping the Stage 1. You can't use this card during your first turn or on a Basic Pokémon that was put into play this turn.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv1/191_hires.png"
    }
  },
  {
    "name": "Rare Candy",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Choose 1 of your Basic Pokémon in play. If you have a Stage 2 card in your hand that evolves from that Pokémon, put that card onto the Basic Pokémon to evolve it, skipping the Stage 1. You can't use this card during your first turn or on a Basic Pokémon that was put into play this turn.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv1/191_hires.png"
    }
  },
  {
    "name": "Fog Crystal",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Search your deck for a Psychic Energy card or a Basic Psychic Pokémon, reveal it, and put it into your hand. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh6/140_hires.png"
    }
  },
  {
    "name": "Fog Crystal",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Search your deck for a Psychic Energy card or a Basic Psychic Pokémon, reveal it, and put it into your hand. Then, shuffle your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh6/140_hires.png"
    }
  },
  {
    "name": "Super Rod",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Shuffle up to 3 in any combination of Pokémon and Basic Energy cards from your discard pile into your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv2/188_hires.png"
    }
  },
  {
    "name": "Super Rod",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Shuffle up to 3 in any combination of Pokémon and Basic Energy cards from your discard pile into your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv2/188_hires.png"
    }
  },
  {
    "name": "Lost Vacuum",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "You can use this card only if you put another card from your hand in the Lost Zone. Choose a Pokémon Tool attached to any Pokémon, or any Stadium in play, and put it in the Lost Zone.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh11/162_hires.png"
    }
  },
  {
    "name": "Pal Pad",
    "supertype": "Trainer",
    "subtypes": [
      "Item"
    ],
    "rules": [
      "Shuffle up to 2 Supporter cards from your discard pile into your deck.",
      "You may play any number of Item cards during your turn."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv1/182_hires.png"
    }
  },
  {
    "name": "Forest Seal Stone",
    "supertype": "Trainer",
    "subtypes": [
      "Item",
      "Pokémon Tool"
    ],
    "rules": [
      "The Pokémon V this card is attached to can use the VSTAR Power on this card.",
      "You may play any number of Item cards during your turn.",
      "Attach a Pokémon Tool to 1 of your Pokémon that doesn't already have a Pokémon Tool attached."
    ],
    "abilities": [
      {
        "name": "Star Alchemy",
        "text": "During your turn, you may search your deck for a card and put it into your hand. Then, shuffle your deck. (You can't use more than 1 VSTAR Power in a game.)",
        "type": "Ability"
      }
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh12/156_hires.png"
    }
  },
  {
    "name": "Artazon",
    "supertype": "Trainer",
    "subtypes": [
      "Stadium"
    ],
    "rules": [
      "Once during each player's turn, that player may search their deck for a Basic Pokémon that doesn't have a Rule Box and put it onto their Bench. Then, that player shuffles their deck. (Pokémon ex, Pokémon V, etc. have Rule Boxes.)",
      "You may play only 1 Stadium card during your turn. Put it next to the Active Spot, and discard it if another Stadium comes into play. A Stadium with the same name can't be played."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv4pt5/76_hires.png"
    }
  },
  {
    "name": "Collapsed Stadium",
    "supertype": "Trainer",
    "subtypes": [
      "Stadium"
    ],
    "rules": [
      "Each player can't have more than 4 Benched Pokémon. If a player has 5 or more Benched Pokémon, they discard Benched Pokémon until they have 4 Pokémon on the Bench. The player who played this card discards first. If more than one effect changes the number of Benched Pokémon allowed, use the smaller number."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/swsh9/137_hires.png"
    }
  },
  {
    "name": "Basic Psychic Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sve/5_hires.png"
    }
  },
  {
    "name": "Basic Psychic Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sve/5_hires.png"
    }
  },
  {
    "name": "Basic Psychic Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sve/5_hires.png"
    }
  },
  {
    "name": "Basic Psychic Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sve/5_hires.png"
    }
  },
  {
    "name": "Basic Psychic Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sve/5_hires.png"
    }
  },
  {
    "name": "Basic Psychic Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sve/5_hires.png"
    }
  },
  {
    "name": "Basic Psychic Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sve/5_hires.png"
    }
  },
  {
    "name": "Basic Psychic Energy",
    "supertype": "Energy",
    "subtypes": [
      "Basic"
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sve/5_hires.png"
    }
  },
  {
    "name": "Reversal Energy",
    "supertype": "Energy",
    "subtypes": [
      "Special"
    ],
    "rules": [
      "As long as this card is attached to a Pokémon, it provides Colorless Energy.If you have more Prize cards remaining than your opponent, and if this card is attached to an Evolution Pokémon that doesn't have a Rule Box (Pokémon ex, Pokémon V, etc. have Rule Boxes), this card provides every type of Energy but provides only 3 Energy at a time."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv2/192_hires.png"
    }
  },
  {
    "name": "Reversal Energy",
    "supertype": "Energy",
    "subtypes": [
      "Special"
    ],
    "rules": [
      "As long as this card is attached to a Pokémon, it provides Colorless Energy.If you have more Prize cards remaining than your opponent, and if this card is attached to an Evolution Pokémon that doesn't have a Rule Box (Pokémon ex, Pokémon V, etc. have Rule Boxes), this card provides every type of Energy but provides only 3 Energy at a time."
    ],
    "images": {
      "large": "https://images.pokemontcg.io/sv2/192_hires.png"
    }
  }
]

def dataclass_to_dict(obj):
    """Convert a dataclass instance to a dictionary recursively."""
    if hasattr(obj, "__dataclass_fields__"):
        # For dataclass instances
        result = {}
        for field in obj.__dataclass_fields__:
            value = getattr(obj, field)
            result[field] = dataclass_to_dict(value)
        return result
    elif isinstance(obj, list):
        # For lists
        return [dataclass_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        # For dictionaries
        return {key: dataclass_to_dict(value) for key, value in obj.items()}
    else:
        # For primitive types
        return obj

def prepare_game_state_for_player(current_state: BoardState, player_number: int):
    """
    Prepare the game state for the specified player.
    
    For player1, this means seeing player1's full hand and player2's limited information.
    For player2, this means seeing player2's full hand and player1's limited information.
    """
    game_state = {"YOUR_HAND": {}, "OPPONENT_HAND": {}}
    
    # Convert BoardState to dictionary for easier manipulation
    state_dict = dataclass_to_dict(current_state)
    
    if player_number == 1:
        # Player1 sees their full hand
        game_state["YOUR_HAND"] = state_dict["playerOne"]
        
        # Player1 sees limited information about player2
        opponent_state = state_dict["playerTwo"]
        game_state["OPPONENT_HAND"] = {
            "active": opponent_state["active"],
            "bench": opponent_state["bench"],
            "discard": opponent_state["discard"],
            "lostZone": opponent_state["lostZone"],
            "deck": f"{len(opponent_state['deck'])} cards",
            "hand": f"{len(opponent_state['hand'])} cards",
            "stadium": opponent_state["stadium"],
            "prizeCards": f"{len(opponent_state['prizeCards'])} cards"
        }
    else:
        # Player2 sees their full hand
        game_state["YOUR_HAND"] = state_dict["playerTwo"]
        
        # Player2 sees limited information about player1
        opponent_state = state_dict["playerOne"]
        game_state["OPPONENT_HAND"] = {
            "active": opponent_state["active"],
            "bench": opponent_state["bench"],
            "discard": opponent_state["discard"],
            "lostZone": opponent_state["lostZone"],
            "deck": f"{len(opponent_state['deck'])} cards",
            "hand": f"{len(opponent_state['hand'])} cards",
            "stadium": opponent_state["stadium"],
            "prizeCards": f"{len(opponent_state['prizeCards'])} cards"
        }
    
    # Include the card mapping
    game_state["card_mapping"] = state_dict["cardMap"]
    
    return game_state

def dict_to_player_state(player_dict: Dict) -> PlayerState:
    """Convert a dictionary to a PlayerState object."""
    # Convert active Pokemon
    active = None
    if player_dict.get("active"):
        active_dict = player_dict["active"]
        attached_cards = None
        if active_dict.get("attachedCards"):
            attached_cards = [Card(id=card["id"]) for card in active_dict["attachedCards"]]
        active = PokemonInPlay(
            id=active_dict["id"],
            hp=active_dict.get("hp", 0),
            attachedCards=attached_cards
        )
    
    # Convert bench Pokemon
    bench = []
    for pokemon_dict in player_dict.get("bench", []):
        attached_cards = None
        if pokemon_dict.get("attachedCards"):
            attached_cards = [Card(id=card["id"]) for card in pokemon_dict["attachedCards"]]
        bench.append(PokemonInPlay(
            id=pokemon_dict["id"],
            hp=pokemon_dict.get("hp", 0),
            attachedCards=attached_cards
        ))
    
    # Convert other card lists
    discard = [Card(id=card["id"]) for card in player_dict.get("discard", [])]
    lost_zone = [Card(id=card["id"]) for card in player_dict.get("lostZone", [])]
    deck = [Card(id=card["id"]) for card in player_dict.get("deck", [])]
    hand = [Card(id=card["id"]) for card in player_dict.get("hand", [])]
    prize_cards = [Card(id=card["id"]) for card in player_dict.get("prizeCards", [])]
    
    # Convert stadium
    stadium = None
    if player_dict.get("stadium") and isinstance(player_dict["stadium"], dict):
        stadium = Card(id=player_dict["stadium"]["id"])
    
    return PlayerState(
        active=active,
        bench=bench,
        discard=discard,
        lostZone=lost_zone,
        deck=deck,
        hand=hand,
        stadium=stadium,
        prizeCards=prize_cards
    )

def dict_to_pokemon_card(card_dict: Dict):
    """Convert dictionary representation of a card back to a proper Pokemon card object."""
    if card_dict is None:
        return None
    
    # For active and bench Pokemon (those with hp or attachedCards)
    if isinstance(card_dict, dict) and "id" in card_dict and ("hp" in card_dict or "attachedCards" in card_dict):
        attached_cards = None
        if card_dict.get("attachedCards"):
            attached_cards = [Card(id=card["id"]) for card in card_dict["attachedCards"]]
        
        return PokemonInPlay(
            id=card_dict["id"],
            hp=card_dict.get("hp", 0),
            attachedCards=attached_cards
        )
    # For stadium and other simple cards, create a Card object
    elif isinstance(card_dict, dict) and "id" in card_dict:
        return Card(id=card_dict["id"])
    
    # Fallback for unknown card types
    return None

def update_global_state(updated_game_state: Dict, player_number: int):
    """Update the global state with the changes from a player's turn."""
    global state
    print("THIS IS THE UPDATED GAME STATE", type(updated_game_state), updated_game_state)

    if isinstance(updated_game_state, str):
        updated_game_state = json.loads(updated_game_state)
        print("THIS IS THE UPDATED GAME STATE AFTER PARSING", type(updated_game_state), updated_game_state)

    # Extract the relevant parts from the updated game state
    your_hand = updated_game_state.get("YOUR_HAND", {})
    opponent_hand = updated_game_state.get("OPPONENT_HAND", {})
    print("THIS IS THE YOUR HAND", your_hand)
    
    # Convert dictionary back to PlayerState
    player_state = dict_to_player_state(your_hand)
    print("THIS IS THE PLAYER STATE", player_state)
    
    # Update the appropriate player state
    if player_number == 1:
        state.playerOne = player_state
        
        # Update opponent's visible information (player 2)
        # Only update what's visible to player 1 (active, bench, discard, etc.)
        if opponent_hand.get("active"):
            state.playerTwo.active = dict_to_pokemon_card(opponent_hand["active"])
        if opponent_hand.get("bench"):
            state.playerTwo.bench = [dict_to_pokemon_card(card) for card in opponent_hand["bench"]]
        if opponent_hand.get("discard"):
            state.playerTwo.discard = [dict_to_pokemon_card(card) for card in opponent_hand["discard"]]
        if opponent_hand.get("lostZone"):
            state.playerTwo.lostZone = [dict_to_pokemon_card(card) for card in opponent_hand["lostZone"]]
        if opponent_hand.get("stadium") and opponent_hand["stadium"] is not None:
            state.playerTwo.stadium = dict_to_pokemon_card(opponent_hand["stadium"])
        elif opponent_hand.get("stadium") is None:
            state.playerTwo.stadium = None
    else:
        state.playerTwo = player_state
        
        # Update opponent's visible information (player 1)
        # Only update what's visible to player 2 (active, bench, discard, etc.)
        if opponent_hand.get("active"):
            state.playerOne.active = dict_to_pokemon_card(opponent_hand["active"])
        if opponent_hand.get("bench"):
            state.playerOne.bench = [dict_to_pokemon_card(card) for card in opponent_hand["bench"]]
        if opponent_hand.get("discard"):
            state.playerOne.discard = [dict_to_pokemon_card(card) for card in opponent_hand["discard"]]
        if opponent_hand.get("lostZone"):
            state.playerOne.lostZone = [dict_to_pokemon_card(card) for card in opponent_hand["lostZone"]]
        if opponent_hand.get("stadium") and opponent_hand["stadium"] is not None:
            state.playerOne.stadium = dict_to_pokemon_card(opponent_hand["stadium"])
        elif opponent_hand.get("stadium") is None:
            state.playerOne.stadium = None

# Modify stdout to stream output in real-time
class StreamingStdout:
    def __init__(self):
        self.buffer = io.StringIO()
        
    def write(self, text):
        # Write to buffer for capturing
        self.buffer.write(text)
        # Add to stream queue for real-time updates
        # if text.strip():
        stream_queue.put(text)
    
    def flush(self):
        pass
    
    def getvalue(self):
        return self.buffer.getvalue()

@contextlib.contextmanager
def capture_stdout():
    """Capture stdout and return it as a string while streaming in real-time."""
    stdout_buffer = StreamingStdout()
    original_stdout = sys.stdout
    sys.stdout = stdout_buffer
    try:
        yield stdout_buffer
    finally:
        sys.stdout = original_stdout

async def process_player_turn(player_number: int):
    """Process a player's turn and yield updates as they occur."""
    global state, stream_queue
    
    # Clear any previous messages in the queue
    while not stream_queue.empty():
        try:
            stream_queue.get_nowait()
        except queue.Empty:
            break
    
    # Prepare game state for the specified player
    game_state = prepare_game_state_for_player(state, player_number)
    
    # Draw a card from the deck to the player's hand at the beginning of turn (classic Pokémon TCG rule)
    card_drawn = False
    try:
        # Identify which player's state to update
        player_state = state.playerOne if player_number == 1 else state.playerTwo
        
        # Check if the deck has cards to draw
        if player_state.deck and len(player_state.deck) > 0:
            # Draw the top card from the deck
            top_card = player_state.deck.pop(0)
            # Add the card to the player's hand
            if player_state.hand is None:
                player_state.hand = []
            player_state.hand.append(top_card)
            card_drawn = True
            
            # Display message about card being drawn
            card_id = top_card.id
            card_info = state.cardMap.get(card_id, {})
            card_name = card_info.get("name", f"Card ID: {card_id}")
            yield f"data: Drew {card_name} from the deck at the beginning of the turn.\n\n"
            
            # Update the game state to reflect the drawn card
            game_state = prepare_game_state_for_player(state, player_number)
        else:
            yield f"data: Cannot draw a card: deck is empty.\n\n"
    except Exception as e:
        print(f"Error drawing card at turn start: {e}")
        yield f"data: Error drawing card: {str(e)}\n\n"
    
    # If we successfully drew a card, send a state update event to trigger the frontend to refresh
    if card_drawn:
        # Send the current state as a special event
        current_state = dataclass_to_dict(state)
        yield f"event: state_update\ndata: {json.dumps(current_state)}\n\n"
        # Add a small delay to ensure the frontend can process the state update
        await asyncio.sleep(0.1)
    
    # Run the player's turn
    # yield "data: Starting turn processing...\n\n"
    
    # Create a synchronization event to signal when processing is complete
    processing_complete = threading.Event()
    result_container = {"result": None}
    
    # Start a background thread to run the turn
    def run_turn():
        try:
            # Use a context manager to capture stdout
            with capture_stdout() as stdout:
                # Run the turn and get the results - this will fill the stream_queue
                result_container["result"] = run_pokemon_tcg_turn(game_state, state.cardMap)
            # Signal completion
            stream_queue.put(None)
        except Exception as e:
            print(f"Error in background thread: {e}")
            stream_queue.put(f"ERROR: {str(e)}")
            stream_queue.put(None)
        finally:
            # Set the event to signal that processing is complete
            processing_complete.set()
    
    # Start the background thread
    thread = threading.Thread(target=run_turn)
    thread.daemon = True  # Make thread a daemon so it doesn't block program exit
    thread.start()
    
    # Stream real-time updates from the queue
    while True:
        try:
            # Try to get a message from the queue with timeout
            message = await asyncio.to_thread(stream_queue.get, timeout=0.1)
            
            # None signals the end of the stream
            if message is None:
                break
                
            # Send the message as SSE
            if isinstance(message, str):
                # Track if we're inside brackets and build filtered message
                inside_brackets = False
                filtered_message = []
                current_chunk = []
                
                for i, char in enumerate(message):
                    if char == '(':
                        # If we see an opening bracket, mark as inside brackets
                        # and don't include the opening bracket
                        inside_brackets = True
                        if current_chunk:
                            filtered_message.extend(current_chunk)
                            current_chunk = []
                    elif char == ')':
                        # If we see a closing bracket, mark as outside brackets
                        # and don't include the closing bracket or the following space
                        inside_brackets = False
                        current_chunk = []
                        # Skip the next character if it's a space
                        if i + 1 < len(message) and message[i + 1] == ' ':
                            continue
                    elif not inside_brackets:
                        # Only add characters when we're not inside brackets
                        current_chunk.append(char)
                
                # Add any remaining non-bracketed content
                if current_chunk:
                    filtered_message.extend(current_chunk)
                
                # Only yield if we have content to stream
                if filtered_message:
                    yield f"data: {''.join(filtered_message)}\n\n"
        except queue.Empty:
            # No messages in queue, continue waiting
            await asyncio.sleep(0.01)
        except Exception as e:
            # Handle any other exceptions
            print(f"Error streaming: {e}")
            yield f"data: ERROR: {str(e)}\n\n"
    
    # Wait for the processing to complete before continuing
    await asyncio.to_thread(processing_complete.wait)
    
    # Get the result from the container
    result = result_container["result"]
    
    # Make sure result is not None before proceeding
    if result is None:
        yield "data: Error: Processing failed to produce a result\n\n"
        yield "event: close\ndata: stream_complete\n\n"
        return
    
    # Now that we have the result, continue with the rest of the processing
    if result["is_legal"]:
        # yield f"data: Legal action: {result['action']}\n\n"
        
        # Update the global state with the changes
        update_global_state(result["updated_game_state"], player_number)
        # yield "data: Game state updated.\n\n"
    else:
        # yield f"data: Illegal action: {result['explanation']}\n\n"
        ...
    
    # Return the conversation history one message at a time
    for message in result["conversation"]:
        role = message["role"].capitalize()
        content = message["content"]
        yield f"data: \n{role}:\n{content}\n\n"
        # Add a small delay between messages
        await asyncio.sleep(0.05)
    
    yield "data: \nTurn completed.\n\n"
    
    # Send close event to signal the end of the stream
    yield "event: close\ndata: stream_complete\n\n"

@router.get("/state")
async def get_state():
    global state
    
    # Initialize state if it hasn't been initialized yet
    if state is None:
        state = get_initial_state(GARDEVOIR_DECK, PIKACHU_DECK)
    
    return dataclass_to_dict(state)

@router.get("/player1/turn")
async def player1_turn():
    """
    Endpoint for player1 to take their turn.
    Returns a streaming response with updates.
    """
    global state
    
    # Initialize state if it hasn't been initialized yet
    if state is None:
        state = get_initial_state(GARDEVOIR_DECK, PIKACHU_DECK)
    
    return StreamingResponse(
        process_player_turn(1), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )

@router.get("/player2/turn")
async def player2_turn():
    """
    Endpoint for player2 to take their turn.
    Returns a streaming response with updates.
    """
    global state
    
    # Initialize state if it hasn't been initialized yet
    if state is None:
        state = get_initial_state(GARDEVOIR_DECK, PIKACHU_DECK)
    
    return StreamingResponse(
        process_player_turn(2), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )

@router.get("/refresh_state")
async def refresh_state():
    """
    Endpoint to refresh the game state.
    This can be called by the frontend after a card is drawn or when state changes.
    """
    global state
    
    # Initialize state if it hasn't been initialized yet
    if state is None:
        state = get_initial_state(GARDEVOIR_DECK, PIKACHU_DECK)
    
    return dataclass_to_dict(state)