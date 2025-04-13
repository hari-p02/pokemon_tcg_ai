/* eslint-disable react-refresh/only-export-components */
import { Box, Divider, Image, Text, VStack } from '@chakra-ui/react';
import { keyframes } from '@emotion/react';
import { atom, useAtomValue, useSetAtom } from 'jotai';
import { useEffect, useState } from 'react';
import background from './assets/background.jpg';
import michael from './assets/michael.png';
import hari from './assets/hari.jpg';
import Agent from './components/Agent';
import HomePage from './components/HomePage';
import PlayerState from './components/PlayerState';
import Slide from './components/Slide';
import McFlex from './McFlex/McFlex';
import McGrid from './McGrid/McGrid';
import { BoardState, fetchGameState } from './services/api';

const cardMapAtom = atom<Record<number, any>>({});
const scaleFactorAtom = atom<number>(1);
const spotlightCardAtom = atom<{ id: number; img: string } | null>(null);
const highlightedCardIdAtom = atom<number | null>(null);
const activePlayerAtom = atom<1 | 2>(1);

const slideIn = keyframes`
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
`;

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
    'home' | 'slide1' | 'slide2' | 'slide3' | 'slide4' | 'game'
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
        setCurrentView('slide4');
        break;
      case 'slide4':
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
          <Slide onNext={handleNext}>
            <McFlex col>
              <Text
                fontFamily="'Press Start 2P', monospace"
                fontSize="100px"
                fontWeight="900"
                color="white"
                textAlign="center"
                textShadow="6px 6px 0 rgba(0, 0, 0, 0.5)"
                letterSpacing="3px"
                mb="40px"
              >
                POKEPLAY.AI
              </Text>
              <Text
                fontFamily="'Press Start 2P', monospace"
                fontSize="20px"
                fontWeight="900"
                color="white"
                textAlign="center"
                textShadow="6px 6px 0 rgba(0, 0, 0, 0.5)"
                letterSpacing="3px"
                mb="40px"
              >
                Team Kanto
              </Text>
            </McFlex>
          </Slide>
        );
      case 'slide2':
        return (
          <Slide onNext={handleNext}>
            <McFlex col orient="top">
              <Text
                fontFamily="'Press Start 2P', monospace"
                fontSize="100px"
                fontWeight="900"
                color="white"
                textAlign="center"
                textShadow="6px 6px 0 rgba(0, 0, 0, 0.5)"
                letterSpacing="3px"
                my="40px"
              >
                WHO ARE WE?
              </Text>
              <McGrid templateColumns="1fr 1fr" gap={8}>
                <McFlex col>
                  <McFlex
                    col
                    orient="top"
                    animation={`${slideIn} 1s ease-out forwards`}
                  >
                    <Image
                      src={michael}
                      alt="Michael"
                      width="500px"
                      height="500px"
                      objectFit="cover"
                      borderRadius="15px"
                      boxShadow="0 4px 8px rgba(0,0,0,0.2)"
                      mb={4}
                    />
                    <Text
                      fontFamily="'Press Start 2P', monospace"
                      fontSize="24px"
                      fontWeight="900"
                      color="white"
                      textAlign="center"
                      textShadow="4px 4px 0 rgba(0, 0, 0, 0.5)"
                      mb="20px"
                    >
                      Michael
                    </Text>
                    <VStack spacing={2} align="center">
                      <Text
                        fontFamily="'Press Start 2P', monospace"
                        fontSize="14px"
                        color="white"
                        textAlign="center"
                        textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
                      >
                        2-time Pokémon TCG International Champion
                      </Text>
                      <Text
                        fontFamily="'Press Start 2P', monospace"
                        fontSize="14px"
                        color="white"
                        textAlign="center"
                        textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
                      >
                        Former world number one ranked player
                      </Text>
                    </VStack>
                  </McFlex>
                </McFlex>
                <McFlex col>
                  <McFlex
                    col
                    animation={`${slideIn} 1s ease-out forwards`}
                    style={{ animationDelay: '4s' }}
                    opacity={0}
                    orient="top"
                  >
                    <Image
                      src={hari}
                      alt="Hari"
                      width="500px"
                      height="500px"
                      objectFit="cover"
                      borderRadius="15px"
                      boxShadow="0 4px 8px rgba(0,0,0,0.2)"
                      mb={4}
                    />
                    <Text
                      fontFamily="'Press Start 2P', monospace"
                      fontSize="24px"
                      fontWeight="900"
                      color="white"
                      textAlign="center"
                      textShadow="4px 4px 0 rgba(0, 0, 0, 0.5)"
                      mb="20px"
                    >
                      Hari
                    </Text>
                    <Text
                      fontFamily="'Press Start 2P', monospace"
                      fontSize="14px"
                      color="white"
                      textAlign="center"
                      textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
                    >
                      Michael's friend
                    </Text>
                  </McFlex>
                </McFlex>
              </McGrid>
            </McFlex>
          </Slide>
        );
      case 'slide3':
        return (
          <Slide onNext={handleNext}>
            <McFlex col orient="top">
              <Text
                fontFamily="'Press Start 2P', monospace"
                fontSize="100px"
                fontWeight="900"
                color="white"
                textAlign="center"
                textShadow="6px 6px 0 rgba(0, 0, 0, 0.5)"
                letterSpacing="3px"
                my="40px"
              >
                MOTIVATION
              </Text>
            </McFlex>
          </Slide>
        );
      case 'slide4':
        return (
          <Slide onNext={handleNext}>
            <McFlex col orient="top">
              <Text
                fontFamily="'Press Start 2P', monospace"
                fontSize="100px"
                fontWeight="900"
                color="white"
                textAlign="center"
                textShadow="6px 6px 0 rgba(0, 0, 0, 0.5)"
                letterSpacing="3px"
                my="40px"
              >
                THEORY
              </Text>
            </McFlex>
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
