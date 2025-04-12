/* eslint-disable react-refresh/only-export-components */
import { Box, Image } from '@chakra-ui/react';
import { atom, useAtomValue, useSetAtom } from 'jotai';
import { useEffect, useState } from 'react';
import Agent from './components/Agent';
import PlayerState from './components/PlayerState';
import TurnConsole from './components/TurnConsole';
import McFlex from './McFlex/McFlex';
import McGrid from './McGrid/McGrid';
import { BoardState, fetchGameState } from './services/api';
import wallpaper from './assets/wallpaper.jpg';

const cardMapAtom = atom<Record<number, any>>({});
const scaleFactorAtom = atom<number>(1);
const spotlightCardAtom = atom<{ id: number; img: string } | null>(null);
const highlightedCardIdAtom = atom<number | null>(null);

// Create custom hooks
export const useCardMap = () => useAtomValue(cardMapAtom);
export const useSetCardMap = () => useSetAtom(cardMapAtom);
export const useScaleFactor = () => useAtomValue(scaleFactorAtom);
export const useSetScaleFactor = () => useSetAtom(scaleFactorAtom);
export const useSpotlightCard = () => useAtomValue(spotlightCardAtom);
export const useSetSpotlightCard = () => useSetAtom(spotlightCardAtom);
export const useHighlightedCardId = () => useAtomValue(highlightedCardIdAtom);
export const useSetHighlightedCardId = () => useSetAtom(highlightedCardIdAtom);

// Default window dimensions for scaling
const desktopWindowWidth = 1300;
const desktopWindowHeight = 720;

function App() {
  const [gameState, setGameState] = useState<BoardState | null>(null);
  const setCardMapState = useSetAtom(cardMapAtom);
  const scaleFactor = useScaleFactor();
  const setScaleFactor = useSetScaleFactor();
  const spotlightCard = useSpotlightCard();
  const setSpotlightCard = useSetSpotlightCard();
  const setHighlightedCardId = useSetHighlightedCardId();

  const calculateScaleFactor = () => {
    const appWrapper = document.getElementById('AppWrapper');
    if (appWrapper) {
      const appWrapperWidth = appWrapper.offsetWidth;
      const appWrapperHeight = appWrapper.offsetHeight;

      // Calculate the scaling factor based on the minimum ratio
      const widthRatio = appWrapperWidth / desktopWindowWidth;
      const heightRatio = appWrapperHeight / desktopWindowHeight;
      const minRatio = Math.min(widthRatio, heightRatio);

      setScaleFactor(minRatio);
    }
  };

  useEffect(() => {
    calculateScaleFactor();
    window.addEventListener('resize', calculateScaleFactor);
    return () => {
      window.removeEventListener('resize', calculateScaleFactor);
    };
  }, []);

  // Function to load game state
  const loadGameState = async () => {
    try {
      const state = await fetchGameState();
      setGameState(state);

      // Set the card map atom with the data from the state
      if (state.cardMap) {
        setCardMapState(state.cardMap);
      }

      // Handle highlighted card from backend
      if (state.highlightedCard && state.cardMap[state.highlightedCard]) {
        const cardInfo = state.cardMap[state.highlightedCard];
        setHighlightedCardId(state.highlightedCard);
        setSpotlightCard({
          id: state.highlightedCard,
          img: cardInfo.images.large,
        });
      } else if (state.highlightedCard === null) {
        // If explicitly set to null, clear the spotlight
        setHighlightedCardId(null);
        setSpotlightCard(null);
      }
    } catch (error) {
      console.error('Failed to load game state:', error);
    }
  };

  // Load game state on component mount
  useEffect(() => {
    loadGameState();
  }, []);

  return (
    <>
      <Box
        id="AppWrapper"
        w="100%"
        h="100%"
        overflow="hidden"
        position="relative"
        bg="gray.100"
      >
        <Image
          src={wallpaper}
          alt="Wallpaper"
          position="absolute"
          top="0"
          left="0"
          width="100%"
          height="100%"
          objectFit="cover"
          opacity={0.15}
        />
        <Box
          position="absolute"
          top="50%"
          left="50%"
          transform={`translate(-50%, -50%) scale(${scaleFactor})`}
          width={`${desktopWindowWidth}px`}
          height={`${desktopWindowHeight}px`}
        >
          <McGrid templateColumns="1fr auto" position="relative">
            <McFlex col position="relative">
              {gameState && (
                <>
                  {spotlightCard && (
                    <Box
                      position="absolute"
                      top="-300"
                      left="-150"
                      right="0"
                      bottom="-300"
                      bg="rgba(0, 0, 0, 0.7)"
                      zIndex="10"
                      display="flex"
                      alignItems="center"
                      justifyContent="center"
                      onClick={() => setSpotlightCard(null)}
                      animation="fadeIn 0.3s ease-in-out"
                    >
                      <Box onClick={(e) => e.stopPropagation()}>
                        <Image
                          h="400px"
                          src={spotlightCard.img}
                          alt="Spotlighted Card"
                          boxShadow="0 0 30px rgba(255, 255, 255, 0.5)"
                          borderRadius="lg"
                          animation="cardZoomIn 0.3s ease-out forwards"
                        />
                      </Box>
                    </Box>
                  )}
                  <Box
                    width="175%"
                    transform="scale(0.6)"
                    transformOrigin="center"
                    my="-70px"
                  >
                    <PlayerState
                      isOpponent={true}
                      playerState={gameState.playerTwo}
                      style={{ transform: 'rotate(180deg)' }}
                    />
                  </Box>
                  <PlayerState playerState={gameState.playerOne} />
                  {/* <Box mt={4} width="100%">
                    <TurnConsole onGameStateUpdated={loadGameState} />
                  </Box> */}
                </>
              )}
            </McFlex>
            <Agent onGameStateUpdated={loadGameState} />
          </McGrid>
        </Box>
      </Box>
    </>
  );
}

export default App;
