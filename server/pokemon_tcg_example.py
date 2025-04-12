import json
import os
from pktcgai.graph.pokemon_tcg_graph import run_pokemon_tcg_turn, transform_game_state

def load_example_game_state():
    """
    Load an example game state to test the Pokemon TCG agent graph.
    
    In a real application, this would come from your game engine.
    """
    return {"YOUR_HAND": {
            "active": {
                "id": 17,
                "hp": 170,
                "attachedCards": None
            },
        "bench": [
            {
                "id": 1,
                "hp": 70,
                "attachedCards": [
                    {
                        "id": 51
                    }
                ]
            },
            {
                "id": 13,
                "hp": 120,
                "attachedCards": [
                    {
                        "id": 58
                    }
                ]
            },
            {
                "id": 12,
                "hp": 220,
                "attachedCards": [
                    {
                        "id": 56
                    }
                ]
            }
        ],
        "discard": [
            {
                "id": 23
            }
        ],
        "lostZone": [
            {
                "id": 38
            }
        ],
        "deck": [
            {
                "id": 44
            },
            {
                "id": 11
            },
            {
                "id": 40
            },
            {
                "id": 42
            },
            {
                "id": 54
            },
            {
                "id": 26
            },
            {
                "id": 59
            },
            {
                "id": 29
            },
            {
                "id": 9
            },
            {
                "id": 28
            },
            {
                "id": 21
            },
            {
                "id": 36
            },
            {
                "id": 3
            },
            {
                "id": 50
            },
            {
                "id": 25
            },
            {
                "id": 33
            },
            {
                "id": 15
            },
            {
                "id": 30
            },
            {
                "id": 57
            },
            {
                "id": 48
            },
            {
                "id": 7
            },
            {
                "id": 18
            },
            {
                "id": 16
            },
            {
                "id": 0
            },
            {
                "id": 10
            },
            {
                "id": 35
            },
            {
                "id": 47
            },
            {
                "id": 43
            },
            {
                "id": 2
            },
            {
                "id": 8
            },
            {
                "id": 37
            },
            {
                "id": 24
            },
            {
                "id": 5
            },
            {
                "id": 4
            },
            {
                "id": 49
            },
            {
                "id": 6
            },
            {
                "id": 52
            },
            {
                "id": 27
            },
            {
                "id": 14
            }
        ],
        "hand": [
            {
                "id": 23
            },
            {
                "id": 38
            },
            {
                "id": 32
            },
            {
                "id": 55
            },
            {
                "id": 31
            },
            {
                "id": 34
            },
            {
                "id": 45
            }
        ],
        "stadium": {
            "id": 46
        },
        "prizeCards": [
            {
                "id": 39
            },
            {
                "id": 53
            },
            {
                "id": 22
            },
            {
                "id": 20
            },
            {
                "id": 19
            },
            {
                "id": 41
            }
        ]
    },
    "OPPONENT_HAND": {
        "active": {
            "id": 17,
            "hp": 170,
            "attachedCards": None
        },
        "bench": [
            {
                "id": 1,
                "hp": 70,
                "attachedCards": [
                    {
                        "id": 51
                    }
                ]
            },
            {
                "id": 13,
                "hp": 120,
                "attachedCards": [
                    {
                        "id": 58
                    }
                ]
            },
            {
                "id": 12,
                "hp": 220,
                "attachedCards": [
                    {
                        "id": 56
                    }
                ]
            }
        ],
        "discard": [
            {
                "id": 23
            }
        ],
        "lostZone": [
            {
                "id": 38
            }
        ],
        "deck": "40 cards",
        "hand": "5 cards",
        "stadium": {
            "id": 46
        },
        "prizeCards": "6 cards"
    }}

def load_example_card_mapping():
    """
    Load an example card ID to card details mapping.
    
    In a real application, this would come from your game database.
    """
    return {
        "0": {
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
        "1": {
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
        "2": {
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
        "3": {
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
        "4": {
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
        "5": {
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
        "6": {
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
        "7": {
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
        "8": {
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
        "9": {
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
        "10": {
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
        "11": {
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
        "12": {
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
        "13": {
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
        "14": {
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
        "15": {
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
        "16": {
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
        "17": {
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
        "18": {
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
        "19": {
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
        "20": {
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
        "21": {
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
        "22": {
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
        "23": {
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
        "24": {
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
        "25": {
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
        "26": {
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
        "27": {
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
        "28": {
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
        "29": {
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
        "30": {
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
        "31": {
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
        "32": {
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
        "33": {
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
        "34": {
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
        "35": {
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
        "36": {
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
        "37": {
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
        "38": {
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
        "39": {
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
        "40": {
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
        "41": {
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
        "42": {
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
        "43": {
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
        "44": {
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
        "45": {
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
        "46": {
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
        "47": {
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
        "48": {
            "name": "Basic Psychic Energy",
            "supertype": "Energy",
            "subtypes": [
                "Basic"
            ],
            "images": {
                "large": "https://images.pokemontcg.io/sve/5_hires.png"
            }
        },
        "49": {
            "name": "Basic Psychic Energy",
            "supertype": "Energy",
            "subtypes": [
                "Basic"
            ],
            "images": {
                "large": "https://images.pokemontcg.io/sve/5_hires.png"
            }
        },
        "50": {
            "name": "Basic Psychic Energy",
            "supertype": "Energy",
            "subtypes": [
                "Basic"
            ],
            "images": {
                "large": "https://images.pokemontcg.io/sve/5_hires.png"
            }
        },
        "51": {
            "name": "Basic Psychic Energy",
            "supertype": "Energy",
            "subtypes": [
                "Basic"
            ],
            "images": {
                "large": "https://images.pokemontcg.io/sve/5_hires.png"
            }
        },
        "52": {
            "name": "Basic Psychic Energy",
            "supertype": "Energy",
            "subtypes": [
                "Basic"
            ],
            "images": {
                "large": "https://images.pokemontcg.io/sve/5_hires.png"
            }
        },
        "53": {
            "name": "Basic Psychic Energy",
            "supertype": "Energy",
            "subtypes": [
                "Basic"
            ],
            "images": {
                "large": "https://images.pokemontcg.io/sve/5_hires.png"
            }
        },
        "54": {
            "name": "Basic Psychic Energy",
            "supertype": "Energy",
            "subtypes": [
                "Basic"
            ],
            "images": {
                "large": "https://images.pokemontcg.io/sve/5_hires.png"
            }
        },
        "55": {
            "name": "Basic Psychic Energy",
            "supertype": "Energy",
            "subtypes": [
                "Basic"
            ],
            "images": {
                "large": "https://images.pokemontcg.io/sve/5_hires.png"
            }
        },
        "56": {
            "name": "Basic Psychic Energy",
            "supertype": "Energy",
            "subtypes": [
                "Basic"
            ],
            "images": {
                "large": "https://images.pokemontcg.io/sve/5_hires.png"
            }
        },
        "57": {
            "name": "Basic Psychic Energy",
            "supertype": "Energy",
            "subtypes": [
                "Basic"
            ],
            "images": {
                "large": "https://images.pokemontcg.io/sve/5_hires.png"
            }
        },
        "58": {
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
        "59": {
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
    }

def main():
    # Load example game state and card mapping
    game_state = load_example_game_state()
    card_mapping = load_example_card_mapping()
    
    # Demonstrate the game state transformation
    print("=== Game State Transformation Example ===")
    print("\nOriginal Game State (excerpt):")
    # print(json.dumps(game_state["active"], indent=2))
    
    # Transform the game state
    transformed_state = transform_game_state(game_state, card_mapping)
    
    print("\nTransformed Game State (excerpt):")
    # print(json.dumps(transformed_state["active"], indent=2))
    print("\nNotice: 'hp' is removed and card details are expanded")
    
    print("\n" + "="*50)
    
    # Run a single turn of the Pokemon TCG agent workflow
    print("\nStarting Pokemon TCG Agent Turn...")
    result = run_pokemon_tcg_turn(game_state, card_mapping)
    
    # Display the results
    print("\n=== Player's Final Action ===")
    print(result["action"])
    
    print("\n=== Action Legality ===")
    print(f"Legal: {result['is_legal']}")
    print(f"Explanation: {result['explanation']}")
    
    # Check if we hit the iteration limit
    if result.get("hit_iteration_limit", False):
        print("\n⚠️ WARNING: Hit maximum iteration limit - the player kept making illegal moves!")
    
    print("\n=== Conversation with Mentor ===")
    for message in result["conversation"]:
        role = message["role"].capitalize()
        content = message["content"]
        print(f"\n{role}:\n{content}")
    
    # Save the updated game state to a file for inspection
    with open("updated_game_state.json", "w") as f:
        json.dump(result["updated_game_state"], f, indent=2)
    print("\nUpdated game state saved to 'updated_game_state.json'")

if __name__ == "__main__":
    main() 