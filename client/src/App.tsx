import { Box } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { fetchGameState, BoardState } from './services/api';
import PlayerState from './components/PlayerState';

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

  console.log(gameState);
  return (
    <Box
      id="AppWrapper"
      w="100%"
      h="100%"
      overflow="hidden"
      position="relative"
      bg="gray.100"
    >
      {gameState && (
        <>
          <PlayerState playerState={gameState.playerOne} />
          <PlayerState playerState={gameState.playerTwo} />
        </>
      )}
    </Box>
  );
}

export default App;
