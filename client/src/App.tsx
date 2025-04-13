/* eslint-disable react-refresh/only-export-components */
import { Box, Divider, Image, Text } from '@chakra-ui/react';
import { atom, useAtomValue, useSetAtom } from 'jotai';
import { useEffect, useState } from 'react';
import wallpaper from './assets/wallpaper.jpg';
import background from './assets/background.jpg';
import Agent from './components/Agent';
import HomePage from './components/HomePage';
import PlayerState from './components/PlayerState';
import McFlex from './McFlex/McFlex';
import McGrid from './McGrid/McGrid';
import { BoardState, fetchGameState } from './services/api';
import Slide from './components/Slide';

const cardMapAtom = atom<Record<number, any>>({});
const scaleFactorAtom = atom<number>(1);
const spotlightCardAtom = atom<{ id: number; img: string } | null>(null);
const highlightedCardIdAtom = atom<number | null>(null);
const activePlayerAtom = atom<1 | 2>(1);

// Create custom hooks
export const useCardMap = () => useAtomValue(cardMapAtom);
export const useSetCardMap = () => useSetAtom(cardMapAtom);
export const useScaleFactor = () => useAtomValue(scaleFactorAtom);
export const useSetScaleFactor = () => useSetAtom(scaleFactorAtom);
export const useSpotlightCard = () => useAtomValue(spotlightCardAtom);
export const useSetSpotlightCard = () => useSetAtom(spotlightCardAtom);
export const useHighlightedCardId = () => useAtomValue(highlightedCardIdAtom);
export const useSetHighlightedCardId = () => useSetAtom(highlightedCardIdAtom);
export const useActivePlayer = () => useAtomValue(activePlayerAtom);
export const useSetActivePlayer = () => useSetAtom(activePlayerAtom);

// Default window dimensions for scaling
const desktopWindowWidth = 1300;
const desktopWindowHeight = 750;

function Game() {
  const [gameState, setGameState] = useState<BoardState | null>(null);
  const setCardMapState = useSetAtom(cardMapAtom);
  const scaleFactor = useScaleFactor();
  const setScaleFactor = useSetScaleFactor();
  const spotlightCard = useSpotlightCard();
  const setSpotlightCard = useSetSpotlightCard();
  const setHighlightedCardId = useSetHighlightedCardId();
  const activePlayer = useActivePlayer();

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
    <Box
      id="AppWrapper"
      w="100%"
      h="100%"
      overflow="hidden"
      position="relative"
      bg="gray.100"
    >
      <Image
        // src={wallpaper}
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
                  transformOrigin="center"
                  my="-60px"
                >
                  <PlayerState
                    isInactive={true}
                    playerState={
                      activePlayer === 1
                        ? gameState.playerTwo
                        : gameState.playerOne
                    }
                    style={{ transform: 'rotate(180deg)' }}
                    isPlayerTwo={activePlayer === 1}
                  />
                </Box>
                <Divider
                  borderColor="gray.300"
                  borderWidth="2px"
                  my={3}
                  opacity={0.8}
                />
                <PlayerState
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

function App() {
  const [currentView, setCurrentView] = useState<
    'home' | 'slide1' | 'slide2' | 'slide3' | 'game'
  >('slide1');

  const handleNext = () => {
    switch (currentView) {
      case 'slide1':
        setCurrentView('slide2');
        break;
      case 'slide2':
        setCurrentView('slide3');
        break;
      case 'slide3':
        setCurrentView('home');
        break;
      default:
        break;
    }
  };

  const renderView = () => {
    switch (currentView) {
      case 'home':
        return <HomePage onStartGame={() => setCurrentView('game')} />;
      case 'slide1':
        return (
          <Slide heading="WELCOME TO POKEPLAY.AI" onNext={handleNext}>
            <Text color="white" fontSize="24px" textAlign="center">
              Get ready to experience the future of Pokémon TCG gameplay!
            </Text>
          </Slide>
        );
      case 'slide2':
        return (
          <Slide heading="AI-POWERED GAMEPLAY" onNext={handleNext}>
            <Text color="white" fontSize="24px" textAlign="center">
              Our advanced AI will help you master the game and make strategic
              decisions
            </Text>
          </Slide>
        );
      case 'slide3':
        return (
          <Slide heading="LET'S BEGIN!" onNext={handleNext} isLastSlide>
            <Text color="white" fontSize="24px" textAlign="center">
              Click START GAME to begin your journey
            </Text>
          </Slide>
        );
      case 'game':
        return <Game />;
      default:
        return null;
    }
  };

  return renderView();
}

export default App;
