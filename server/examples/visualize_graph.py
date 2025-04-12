import os
from pktcgai.graph.pokemon_tcg_graph import create_pokemon_tcg_graph

def visualize_pokemon_tcg_graph():
    """Visualize the Pokemon TCG agent workflow graph."""
    # Create the graph
    workflow = create_pokemon_tcg_graph()
    
    # Generate the visualization
    os.makedirs("visualizations", exist_ok=True)
    workflow.write_html("visualizations/pokemon_tcg_graph.html")
    
    print("Graph visualization saved to: visualizations/pokemon_tcg_graph.html")
    print("Open this file in a web browser to view the graph.")
    print("\nWorkflow summary:")
    print("1. Player starts by examining the game state")
    print("2. Player can discuss with Mentor until ready to make a final decision")
    print("3. Player's final decision is sent to Referee for validation")
    print("4. If the action is legal, the workflow ends")
    print("5. If the action is illegal, the Player is notified and can try again")

if __name__ == "__main__":
    visualize_pokemon_tcg_graph() 