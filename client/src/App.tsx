/* eslint-disable react-refresh/only-export-components */
import { Image, Text, VStack } from '@chakra-ui/react';
import { keyframes } from '@emotion/react';
import { atom, useAtomValue, useSetAtom } from 'jotai';
import { useState } from 'react';
import hari from './assets/hari.jpg';
import michael from './assets/michael.png';
import Game from './components/Game';
import HomePage from './components/HomePage';
import Slide from './components/Slide';
import McFlex from './McFlex/McFlex';
import McGrid from './McGrid/McGrid';

// Export atoms
export const cardMapAtom = atom<Record<number, any>>({});
export const scaleFactorAtom = atom<number>(1);
export const spotlightCardAtom = atom<{ id: number; img: string } | null>(null);
export const highlightedCardIdAtom = atom<number | null>(null);
export const activePlayerAtom = atom<1 | 2>(1);

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

function App() {
  const [currentView, setCurrentView] = useState<
    'home' | 'slide1' | 'slide2' | 'slide3' | 'slide4' | 'game'
  >('game');

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
