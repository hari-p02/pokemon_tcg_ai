import { Box } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { fetchGameState, BoardState } from './services/api';
import PlayerState from './components/PlayerState';
import Agent from './components/Agent';
import McFlex from './McFlex/McFlex';
import McGrid from './McGrid/McGrid';

function App() {
  const [gameState, setGameState] = useState<BoardState | null>(null);

  useEffect(() => {
    const loadGameState = async () => {
      try {
        const state = await fetchGameState();
        setGameState(state);
      } catch (error) {
        console.error('Failed to load game state:', error);
      }
    };

    loadGameState();
  }, []);

  return (
    <Box
      id="AppWrapper"
      w="100%"
      h="100%"
      overflow="hidden"
      position="relative"
      bg="gray.100"
    >
      <McGrid templateColumns="1fr auto">
        <McFlex col>
          {gameState && (
            <>
              <PlayerState
                playerState={gameState.playerTwo}
                style={{ transform: 'rotate(180deg)' }}
              />
              <PlayerState playerState={gameState.playerOne} />
            </>
          )}
        </McFlex>
        <Agent
          agent="Ash"
          message="Hello Trainer! Welcome to the Pokémon Trading Card Game."
        />
      </McGrid>
    </Box>
  );
}

export default App;
