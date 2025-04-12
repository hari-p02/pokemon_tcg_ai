import { Box, Button, Image, Text, VStack, useToast } from '@chakra-ui/react';
import { keyframes } from '@emotion/react';
import { AnimatePresence, motion } from 'framer-motion';
import { FC, useEffect, useRef, useState } from 'react';
import { useSetActivePlayer } from '../App';
import ashImage from '../assets/ash.png';
import brockImage from '../assets/brock.png';
import jessieImage from '../assets/jessie.png';
import meowthImage from '../assets/meowth.png';
import oakImage from '../assets/oak.png';
import rocketImage from '../assets/rocket.png';
import McFlex from '../McFlex/McFlex';
import { fetchGameState } from '../services/api';

interface AgentProps {
  onGameStateUpdated: () => void;
  activePlayer: 1 | 2;
}

const Agent: FC<AgentProps> = ({ onGameStateUpdated, activePlayer }) => {
  const [fullText, setFullText] = useState('');
  const [displayedText, setDisplayedText] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [currentAgent, setCurrentAgent] = useState('Ash');
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const toast = useToast();
  const eventSourceRef = useRef<EventSource | null>(null);
  const textBoxRef = useRef<HTMLDivElement>(null);
  const animationRef = useRef<number | null>(null);
  const setActivePlayer = useSetActivePlayer();
  const [messageQueue, setMessageQueue] = useState<
    {
      agent: string;
      message: string;
    }[]
  >([]);

  useEffect(() => {
    if (messageQueue.length <= 0) {
      return;
    }
    if (messageQueue[0].agent === 'close') {
      const handleClose = async () => {
        try {
          await fetchGameState();
          onGameStateUpdated();
          setIsLoading(false);
        } catch (error) {
          console.error('Error fetching final state:', error);
          setIsLoading(false);
        }
      };
      handleClose();
      return;
    }
    setCurrentAgent(messageQueue[0].agent);
    setFullText(messageQueue[0].message);
  }, [messageQueue]);

  useEffect(() => {
    setDisplayedText('');
    setCurrentIndex(0);
  }, [currentAgent]);

  useEffect(() => {
    if (messageQueue.length <= 1) {
      return;
    }
    if (displayedText === messageQueue[0].message && displayedText !== '') {
      console.log('message finished. starting next message in 5 seconds');
      setTimeout(() => {
        setMessageQueue((prev) => prev.slice(1));
      }, 5000);
    }
  }, [displayedText]);

  // Auto-scroll to bottom when text changes
  useEffect(() => {
    if (textBoxRef.current) {
      textBoxRef.current.scrollTop = textBoxRef.current.scrollHeight;
    }
  }, [displayedText]);

  // Typewriter animation effect
  useEffect(() => {
    if (currentIndex < fullText.length) {
      animationRef.current = window.setTimeout(() => {
        setDisplayedText(fullText.substring(0, currentIndex + 1));
        setCurrentIndex(currentIndex + 1);
      }, 20);
    }

    return () => {
      if (animationRef.current) {
        window.clearTimeout(animationRef.current);
      }
    };
  }, [currentIndex, fullText]);

  // Cleanup function for event source
  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);

  const handlePlayerTurn = async (playerNumber: 1 | 2) => {
    // Clean up any existing EventSource
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }
    setMessageQueue([]);
    setIsLoading(true);
    setFullText('');
    setDisplayedText('');
    setCurrentIndex(0);
    setActivePlayer(playerNumber);

    try {
      const response = await fetch(
        `http://localhost:8000/player${playerNumber}/turn`
      );

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      if (!response.body) {
        throw new Error('Response has no body');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          break;
        }

        const text = decoder.decode(value, { stream: true });
        buffer += text;

        let startIndex = 0;
        let endIndex;

        while ((endIndex = buffer.indexOf('\n\n', startIndex)) !== -1) {
          const message = buffer.substring(startIndex, endIndex);
          const dataMatch = message.match(/^data: (.*)$/m);

          if (dataMatch) {
            const data = dataMatch[1];

            if (message.includes('event: close')) {
              setMessageQueue((prev) => [
                ...prev,
                { agent: 'close', message: '' },
              ]);
            } else {
              const displayText = data;

              if (
                displayText.includes(
                  '-------------MASTER NODE STARTED-------------------'
                )
              ) {
                setMessageQueue((prev) => [
                  ...prev,
                  { agent: 'Oak', message: '' },
                ]);
              } else if (
                displayText.includes(
                  '-------------PLAYER NODE STARTED-------------------'
                )
              ) {
                setMessageQueue((prev) => [
                  ...prev,
                  { agent: 'Ash', message: '' },
                ]);
              } else if (
                displayText.includes(
                  '-------------REFEREE NODE STARTED-------------------'
                )
              ) {
                setMessageQueue((prev) => [
                  ...prev,
                  { agent: 'Brock', message: '' },
                ]);
              } else if (displayText) {
                setMessageQueue((prev) => {
                  if (prev.length === 0) {
                    return prev;
                  }
                  const lastMessage = prev[prev.length - 1];
                  return [
                    ...prev.slice(0, -1),
                    {
                      ...lastMessage,
                      message: lastMessage.message + displayText,
                    },
                  ];
                });
              }
            }
          }

          startIndex = endIndex + 2;
        }

        buffer = buffer.substring(startIndex);
      }

      setIsLoading(false);

      toast({
        title: 'Turn completed',
        status: 'success',
        duration: 2000,
        isClosable: true,
      });
    } catch (error) {
      console.error('Error during turn:', error);
      setIsLoading(false);

      toast({
        title: 'Error',
        description: 'Failed to process turn',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const blinkAnimation = keyframes`
    from, to { border-color: transparent }
    50% { border-color: black }
  `;

  // Update agent image based on current agent and active player
  const getAgentImage = () => {
    if (activePlayer === 1) {
      switch (currentAgent) {
        case 'Ash':
          return ashImage;
        case 'Oak':
          return oakImage;
        case 'Brock':
          return brockImage;
        default:
          return oakImage;
      }
    } else {
      switch (currentAgent) {
        case 'Ash':
          return rocketImage;
        case 'Oak':
          return meowthImage;
        case 'Brock':
          return jessieImage;
        default:
          return meowthImage;
      }
    }
  };

  return (
    <McFlex position="relative" mx="20px" orient="bottom" w="300px" col>
      <VStack spacing={4} width="100%" h="100%" pt="10px">
        <McFlex gap={3} orient="top">
          <Button
            bg="purple.500"
            color="white"
            onClick={() => handlePlayerTurn(1)}
            isDisabled={isLoading}
            width="35%"
            size="lg"
            fontWeight="bold"
            transition="all 0.2s"
            boxShadow="0 4px 8px rgba(0, 0, 0, 0.2)"
            _hover={{
              transform: 'scale(1.02)',
              bg: 'purple.600',
              boxShadow: '0 8px 12px rgba(0, 0, 0, 0.25)',
            }}
          >
            Ash
          </Button>
          <Button
            bg="red.400"
            color="black"
            onClick={() => handlePlayerTurn(2)}
            isDisabled={isLoading}
            width="50%"
            size="lg"
            fontWeight="bold"
            transition="all 0.2s"
            boxShadow="0 4px 8px rgba(0, 0, 0, 0.2)"
            _hover={{
              transform: 'scale(1.02)',
              bg: 'red.500',
              boxShadow: '0 8px 12px rgba(0, 0, 0, 0.25)',
            }}
          >
            Team Rocket
          </Button>
        </McFlex>
        <Box position="relative" mb="20px">
          <Box
            bg="white"
            borderRadius="20px"
            padding="15px"
            boxShadow="md"
            width="250px"
            maxHeight="240px"
            overflowY="auto"
            ref={textBoxRef}
            css={{
              '&::-webkit-scrollbar': {
                display: 'none',
              },
              '&': {
                scrollbarWidth: 'none',
                msOverflowStyle: 'none',
              },
            }}
            display={displayedText ? 'block' : 'none'}
          >
            <Text
              fontFamily="monospace"
              fontSize="md"
              color="black"
              whiteSpace="pre-wrap"
            >
              {displayedText}
              {isLoading && (
                <Box
                  as="span"
                  borderRight="2px solid black"
                  display="inline-block"
                  sx={{
                    animation: `${blinkAnimation} 0.75s step-end infinite`,
                  }}
                />
              )}
            </Text>
          </Box>
          {displayedText && (
            <Box
              position="absolute"
              zIndex="10"
              bottom="-15px"
              left="50%"
              transform="translateX(-50%)"
              width="0"
              height="0"
              borderLeft="20px solid transparent"
              borderRight="20px solid transparent"
              borderTop="20px solid white"
            />
          )}
        </Box>

        <McFlex width="300px" autoH>
          <AnimatePresence mode="wait">
            <motion.div
              key={`${currentAgent}-${activePlayer}`}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              transition={{ duration: 0.3, ease: 'easeInOut' }}
            >
              <Image src={getAgentImage()} w="100%" alt={currentAgent} />
            </motion.div>
          </AnimatePresence>
        </McFlex>
      </VStack>
    </McFlex>
  );
};

export default Agent;
