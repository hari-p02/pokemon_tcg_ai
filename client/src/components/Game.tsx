import { Box, Divider, Image } from '@chakra-ui/react';
import { useAtomValue, useSetAtom } from 'jotai';
import { useEffect, useState } from 'react';
import background from '../assets/background.jpg';
import Agent from './Agent';
import PlayerState from './PlayerState';
import McFlex from '../McFlex/McFlex';
import McGrid from '../McGrid/McGrid';
import { BoardState, fetchGameState } from '../services/api';
import {
  cardMapAtom,
  scaleFactorAtom,
  spotlightCardAtom,
  highlightedCardIdAtom,
  activePlayerAtom,
} from '../App';

function Game() {
  // Load game state on component mount
  useEffect(() => {
    const isPreset = true;
    loadGameState(isPreset);
  }, []);

  const [gameState, setGameState] = useState<BoardState | null>(null);
  const setCardMapState = useSetAtom(cardMapAtom);
  const scaleFactor = useAtomValue(scaleFactorAtom);
  const setScaleFactor = useSetAtom(scaleFactorAtom);
  const spotlightCard = useAtomValue(spotlightCardAtom);
  const setSpotlightCard = useSetAtom(spotlightCardAtom);
  const setHighlightedCardId = useSetAtom(highlightedCardIdAtom);
  const activePlayer = useAtomValue(activePlayerAtom);

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
  const loadGameState = async (isPreset: boolean = false) => {
    try {
      const state = await fetchGameState(isPreset);
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

  return (
    <Box
      id="AppWrapper"
      w="100%"
      h="100%"
      overflow="hidden"
      position="relative"
      bg="gray.100"
    >
      <Image
        src={background}
        alt="Wallpaper"
        position="absolute"
        top="0"
        left="0"
        width="100%"
        height="100%"
        objectFit="cover"
        opacity={0.5}
      />
      <Box
        position="absolute"
        bottom="0"
        left="50%"
        transform={`translate(-50%, 0) scale(${scaleFactor})`}
        transformOrigin="bottom center"
        width={`${desktopWindowWidth}px`}
        height={`${desktopWindowHeight}px`}
      >
        <McGrid templateColumns="1fr auto" position="relative">
          <McFlex col position="relative" ml="10px">
            {gameState && (
              <>
                {spotlightCard && (
                  <Box
                    position="absolute"
                    top="-300"
                    left="-150"
                    right="0"
                    bottom="-300"
                    bg="rgba(0, 0, 0, 0.3)"
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
                  width="167%"
                  transform="scale(0.6)"
                  transformOrigin="bottom center"
                  mt="-140px"
                >
                  <PlayerState
                    isInactive={true}
                    playerState={
                      activePlayer === 1
                        ? gameState.playerTwo
                        : gameState.playerOne
                    }
                    activePlayer={activePlayer}
                    style={{ transform: 'rotate(180deg)' }}
                    isPlayerTwo={activePlayer === 1}
                  />
                </Box>
                <Box position="relative" w="100%">
                  <Divider
                    borderColor="gray.300"
                    borderWidth="2px"
                    borderRadius="full"
                    my={3}
                    opacity={0.4}
                  />
                  <Box
                    position="absolute"
                    top="50%"
                    left="50%"
                    transform="translate(-50%, -50%)"
                    w="12px"
                    h="12px"
                    borderRadius="full"
                    bg="gray.300"
                    opacity={0.7}
                  />
                </Box>
                <PlayerState
                  activePlayer={activePlayer}
                  playerState={
                    activePlayer === 1
                      ? gameState.playerOne
                      : gameState.playerTwo
                  }
                  isPlayerTwo={activePlayer === 2}
                />
              </>
            )}
          </McFlex>
          <Agent
            onGameStateUpdated={loadGameState}
            activePlayer={activePlayer}
          />
        </McGrid>
      </Box>
    </Box>
  );
}

// Default window dimensions for scaling
const desktopWindowWidth = 1300;
const desktopWindowHeight = 750;

export default Game;
