# Pokemon TCG AI Agent System

This project implements an AI agent system for playing the Pokemon Trading Card Game using LangChain and LangGraph.

## Architecture

The system consists of three primary agents:

1. **Player Agent**: Makes decisions about game actions
2. **Mentor Agent**: Provides strategic advice using a knowledge base
3. **Referee Agent**: Validates moves and updates game state

The agents are orchestrated using a LangGraph workflow that enables conversation between the Player and Mentor before the Player makes a final decision, which is then validated by the Referee.

## Game State Transformation

Before passing the game state to the Player and Mentor agents, the system applies these transformations:

1. **HP Removal**: All "hp" keys are removed from the game state to simplify the representation.
2. **Card Detail Expansion**: Card IDs are expanded with their full details from the card mapping data, making it easier for the agents to reason about cards without needing to look up references.

These transformations improve the agents' understanding of the game state while maintaining the original structure for the Referee.

## LangGraph Workflow

```
Player ←→ Mentor
  ↓
Referee
  ↓   ↑
 End  |
     ↙
 (if illegal)
```

- The Player agent can discuss strategy with the Mentor agent
- When the Player makes a final decision, it's sent to the Referee
- The Referee validates the action and updates the game state
- If the action is illegal, the workflow routes back to the Player with an explanation
- Only legal actions complete the workflow

## Setup

1. Install dependencies:

```bash
cd ./server
uv sync
```

2. Set up environment variables:

```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

To run the example:

```bash
python examples/pokemon_tcg_example.py
```

To visualize the LangGraph workflow:

```bash
python examples/visualize_graph.py
```

## Directory Structure (in server)

- `pktcgai/chains/`: Individual agent implementations
  - `player.py`: Player agent
  - `mentor.py`: Mentor agent
  - `referee.py`: Referee agent
- `pktcgai/graph/`: LangGraph implementation
  - `pokemon_tcg_graph.py`: Graph definition and state flow
- `examples/`: Example usage scripts
