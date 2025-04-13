/* eslint-disable react-refresh/only-export-components */
import { Image, Text, VStack, Box } from '@chakra-ui/react';
import { keyframes } from '@emotion/react';
import { atom, useAtomValue, useSetAtom } from 'jotai';
import { useState, useEffect, useRef } from 'react';
import hari from './assets/hari.png';
import michael from './assets/michael.png';
import Game from './components/Game';
import HomePage from './components/HomePage';
import Slide from './components/Slide';
import McFlex from './McFlex/McFlex';
import McGrid from './McGrid/McGrid';
import intromusic from './audio/intromusic.mp3';
import battleMusic from './audio/battlemusic.mp3';
import hackdemo from './video/hackdemo.mov';
import diagram from './assets/diagram.jpeg';

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
    'home' | 'slide1' | 'slide2' | 'slide3' | 'slide4' | 'slide5' | 'game'
  >('slide1');
  const [currentAudio, setCurrentAudio] = useState<'intro' | 'battle' | null>(
    null
  );
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [showHari, setShowHari] = useState(false);
  const [showSecondColumn, setShowSecondColumn] = useState(false);

  // Effect to determine which audio should play based on view
  useEffect(() => {
    if (currentView === 'slide2') {
      setCurrentAudio('intro');
    } else if (currentView === 'game') {
      setCurrentAudio('battle');
    } else if (currentView === 'slide5') {
      setCurrentAudio('intro');
    }
  }, [currentView]);

  // Effect to handle actual audio playback
  useEffect(() => {
    if (!currentAudio) {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.currentTime = 0;
      }
      return;
    }

    const newAudio = new Audio(
      currentAudio === 'intro' ? intromusic : battleMusic
    );
    newAudio.loop = true;
    newAudio.volume = currentAudio === 'intro' ? 0.08 : 0.05;
    newAudio.play();
    audioRef.current = newAudio;

    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.currentTime = 0;
      }
    };
  }, [currentAudio]);

  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.key.toLowerCase() === 'h') {
        setShowHari(true);
        setShowSecondColumn(true);
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, []);

  const handleNext = () => {
    setShowSecondColumn(false);
    setShowHari(false);
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
      case 'home':
        setCurrentView('game');
        break;
      case 'game':
        setCurrentView('slide5');
        break;
      case 'slide5':
        setCurrentView('slide1');
        break;
      default:
        break;
    }
  };

  const renderView = () => {
    switch (currentView) {
      case 'home':
        return <HomePage onNext={handleNext} />;
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
                pok
                <Text as="span" fontSize="100px">
                  é
                </Text>
                play
                <Text as="span" fontSize="60px" color="#FFD700">
                  .ai
                </Text>
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
                mt="40px"
                mb="80px"
              >
                WHO ARE WE?
              </Text>
              <McGrid templateColumns="1fr 1fr" gap={8}>
                <McFlex col>
                  <McFlex
                    col
                    orient="top right"
                    pr="75px"
                    animation={`${slideIn} 1s ease-out forwards`}
                  >
                    <Image
                      src={michael}
                      alt="Michael"
                      width="350px"
                      height="350px"
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
                    <VStack spacing={2} align="flex-end">
                      <Text
                        fontFamily="'Press Start 2P', monospace"
                        fontSize="14px"
                        color="white"
                        textAlign="center"
                        textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
                      >
                        2-time Pokémon TCG international champion
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
                  {showHari && (
                    <McFlex
                      col
                      animation={`${slideIn} 1s ease-out forwards`}
                      orient="top left"
                      pl="75px"
                    >
                      <Image
                        src={hari}
                        alt="Hari"
                        width="350px"
                        height="350px"
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
                  )}
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
              <McFlex col>
                <McGrid templateColumns="1fr 1fr" gap={8} px={10} autoH>
                  <McFlex col orient="top left" gap={14}>
                    <McFlex gap={2} auto>
                      <Text
                        fontFamily="'Press Start 2P', monospace"
                        fontSize="16px"
                        color="white"
                        textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
                      >
                        •
                      </Text>
                      <Text
                        fontFamily="'Press Start 2P', monospace"
                        fontSize="16px"
                        color="white"
                        textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
                      >
                        10+ years of Pokémon has changed my life
                      </Text>
                    </McFlex>

                    <McFlex gap={2} auto>
                      <Text
                        fontFamily="'Press Start 2P', monospace"
                        fontSize="16px"
                        color="white"
                        textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
                      >
                        •
                      </Text>
                      <Text
                        fontFamily="'Press Start 2P', monospace"
                        fontSize="16px"
                        color="white"
                        textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
                      >
                        Pokémon is the world's most valuable IP ($90B)
                      </Text>
                    </McFlex>

                    <McFlex gap={2} auto>
                      <Text
                        fontFamily="'Press Start 2P', monospace"
                        fontSize="16px"
                        color="white"
                        textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
                      >
                        •
                      </Text>
                      <Text
                        fontFamily="'Press Start 2P', monospace"
                        fontSize="16px"
                        color="white"
                        textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
                      >
                        Tournament prize pools double annually
                      </Text>
                    </McFlex>
                    <McFlex gap={2} auto>
                      <Text
                        fontFamily="'Press Start 2P', monospace"
                        fontSize="16px"
                        color="#FFD700"
                        textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
                      >
                        •
                      </Text>
                      <Text
                        fontFamily="'Press Start 2P', monospace"
                        fontSize="16px"
                        color="#FFD700"
                        textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
                      >
                        Millions of kids own cards, but few know how to play
                      </Text>
                    </McFlex>
                  </McFlex>
                  <McFlex col>
                    <McFlex col orient="top left" gap={14}>
                      {showSecondColumn && (
                        <>
                          <McFlex
                            gap={2}
                            auto
                            animation={`${slideIn} 1s ease-out forwards`}
                          >
                            <Text
                              fontFamily="'Press Start 2P', monospace"
                              fontSize="16px"
                              color="white"
                              textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
                            >
                              •
                            </Text>
                            <Text
                              fontFamily="'Press Start 2P', monospace"
                              fontSize="16px"
                              color="white"
                              textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
                            >
                              2 player requirement
                            </Text>
                          </McFlex>
                          <McFlex
                            gap={2}
                            auto
                            animation={`${slideIn} 1s ease-out forwards`}
                          >
                            <Text
                              fontFamily="'Press Start 2P', monospace"
                              fontSize="16px"
                              color="#FFD700"
                              textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
                            >
                              •
                            </Text>
                            <Text
                              fontFamily="'Press Start 2P', monospace"
                              fontSize="16px"
                              textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
                              color="#FFD700"
                            >
                              Complex game mechanics create barriers to entry
                            </Text>
                          </McFlex>
                          <McFlex
                            gap={2}
                            auto
                            animation={`${slideIn} 1s ease-out forwards`}
                          >
                            <Text
                              fontFamily="'Press Start 2P', monospace"
                              fontSize="16px"
                              color="white"
                              textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
                            >
                              •
                            </Text>
                            <Text
                              fontFamily="'Press Start 2P', monospace"
                              fontSize="16px"
                              color="white"
                              textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
                            >
                              We want to create an intuitive and accessible way
                              to play
                            </Text>
                          </McFlex>
                        </>
                      )}
                    </McFlex>
                  </McFlex>
                </McGrid>
              </McFlex>
            </McFlex>
          </Slide>
        );
      case 'slide4':
        return (
          <Slide onNext={handleNext}>
            <McFlex col orient="top" overflow="hidden">
              <Text
                fontFamily="'Press Start 2P', monospace"
                fontSize="100px"
                fontWeight="900"
                color="white"
                textAlign="center"
                textShadow="6px 6px 0 rgba(0, 0, 0, 0.5)"
                letterSpacing="3px"
                mt="40px"
              >
                AGENTIC FLOW
              </Text>
              <McFlex col p={8}>
                <Image
                  fit="contain"
                  src={diagram}
                  alt="diagram"
                  width="50%"
                  height="100%"
                />
              </McFlex>
            </McFlex>
          </Slide>
        );
      case 'game':
        return <Game onNext={handleNext} />;
      case 'slide5':
        return (
          <Slide onNext={handleNext}>
            <Box
              position="fixed"
              top="0"
              left="0"
              width="100vw"
              height="100vh"
              zIndex="1"
            >
              <video
                src={hackdemo}
                autoPlay
                muted
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover',
                }}
              />
            </Box>
          </Slide>
        );
      default:
        return null;
    }
  };

  return renderView();
}

export default App;
