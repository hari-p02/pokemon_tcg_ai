import { Box, Button, Image, Text, VStack } from '@chakra-ui/react';
import { keyframes } from '@emotion/react';
import axios from 'axios';
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

interface MessageQueueItem {
  agent: string;
  message: string;
  audioUrl?: string;
  isGenerating?: boolean;
  isReadyForAudioGeneration?: boolean;
}

const Agent: FC<AgentProps> = ({ onGameStateUpdated, activePlayer }) => {
  const [fullText, setFullText] = useState('');
  const [displayedText, setDisplayedText] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [currentAgent, setCurrentAgent] = useState('Ash');
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);
  const textBoxRef = useRef<HTMLDivElement>(null);
  const animationRef = useRef<number | null>(null);
  const setActivePlayer = useSetActivePlayer();
  const [messageQueue, setMessageQueue] = useState<MessageQueueItem[]>([]);
  const [isAudioPlaying, setIsAudioPlaying] = useState(false);
  const [audioQueue, setAudioQueue] = useState<MessageQueueItem[]>([]);

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

  // Cleanup function for event source and audio
  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.src = '';
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
                ...prev.map((msg) => ({
                  ...msg,
                  isReadyForAudioGeneration: true,
                })),
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
                  ...prev.map((msg) => ({
                    ...msg,
                    isReadyForAudioGeneration: true,
                  })),
                  { agent: 'Oak', message: '' },
                ]);
              } else if (
                displayText.includes(
                  '-------------PLAYER NODE STARTED-------------------'
                )
              ) {
                setMessageQueue((prev) => [
                  ...prev.map((msg) => ({
                    ...msg,
                    isReadyForAudioGeneration: true,
                  })),
                  { agent: 'Ash', message: '' },
                ]);
              } else if (
                displayText.includes(
                  '-------------REFEREE NODE STARTED-------------------'
                )
              ) {
                setMessageQueue((prev) => [
                  ...prev.map((msg) => ({
                    ...msg,
                    isReadyForAudioGeneration: true,
                  })),
                  { agent: 'Brock', message: '' },
                ]);
              } else if (displayText) {
                setMessageQueue((prev) => {
                  if (prev.length === 0) {
                    return prev;
                  }
                  const lastMessage = prev[prev.length - 1];
                  return [
                    ...prev.slice(0, -1).map((msg) => ({
                      ...msg,
                      isReadyForAudioGeneration: true,
                    })),
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
    } catch (error) {
      console.error('Error during turn:', error);
      setIsLoading(false);
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

  const generateAudio = async (
    agent: string,
    message: string
  ): Promise<string> => {
    const voiceId =
      activePlayer === 1
        ? agent === 'Ash'
          ? 'MF3mGyEYCl7XYWbV9V6O'
          : agent === 'Brock'
            ? 'SOYHLrjzK2X1ezoPC6cr'
            : 'D38z5RcWu1voky8WS1ja'
        : agent === 'Ash'
          ? 'TX3LPaxmHKxFdv7VOQHJ' // Team Rocket voice
          : agent === 'Brock'
            ? '21m00Tcm4TlvDq8ikWAM' // Jessie voice
            : 'zcAOhNBS3c14rBihAFp1'; // Meowth voice

    const apiKey = import.meta.env.VITE_ELEVENLABS_API_KEY as string;
    if (!apiKey) {
      console.error('No ElevenLabs API key found');
      throw new Error('No API key');
    }

    const apiUrl = `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`;

    try {
      const response = await axios({
        method: 'post',
        url: apiUrl,
        data: {
          text: message,
          model_id: 'eleven_turbo_v2',
          output_format: 'mp3',
          voice_settings: {
            stability: 0.5,
            similarity_boost: 0.75,
            speed: 1.2,
            style: 0.0,
            use_speaker_boost: true,
          },
        },
        headers: {
          'Content-Type': 'application/json',
          'xi-api-key': apiKey,
        },
        responseType: 'arraybuffer',
      });

      const blob = new Blob([response.data], { type: 'audio/mpeg' });
      return URL.createObjectURL(blob);
    } catch (error) {
      console.error('Error generating audio:', error);
      throw error;
    }
  };

  // Handle audio generation for messages that are ready
  useEffect(() => {
    const processAudioGeneration = async () => {
      const messagesNeedingAudio = messageQueue.filter(
        (msg) =>
          msg.isReadyForAudioGeneration && !msg.audioUrl && !msg.isGenerating
      );

      for (const message of messagesNeedingAudio) {
        const currentMessage = message;
        try {
          setMessageQueue((prev) =>
            prev.map((msg) =>
              msg === currentMessage ? { ...msg, isGenerating: true } : msg
            )
          );

          const audioUrl = await generateAudio(
            currentMessage.agent,
            currentMessage.message
          );

          setAudioQueue((prev) => [...prev, { ...currentMessage, audioUrl }]);

          setMessageQueue((prev) =>
            prev.map((msg) =>
              msg === currentMessage ? { ...msg, isGenerating: false } : msg
            )
          );
        } catch (error) {
          console.error('Error in audio generation process:', error);
          setMessageQueue((prev) =>
            prev.map((msg) =>
              msg === currentMessage ? { ...msg, isGenerating: false } : msg
            )
          );
        }
      }
    };

    processAudioGeneration();
  }, [messageQueue]);

  useEffect(() => {
    if (audioQueue.length > 0 && !isAudioPlaying) {
      const firstAudio = audioQueue[0];
      if (firstAudio.audioUrl) {
        setIsAudioPlaying(true);
        if (!audioRef.current) {
          audioRef.current = new Audio();
        }
        audioRef.current.src = firstAudio.audioUrl;

        audioRef.current.onended = () => {
          setIsAudioPlaying(false);
          setAudioQueue((prev) => {
            const newQueue = prev.slice(1);
            return newQueue;
          });
          setMessageQueue((prev) => prev.slice(1));
        };
        audioRef.current.play().catch((error) => {
          console.error('Error playing audio:', error);
          setIsAudioPlaying(false);
        });
      }
    }
  }, [audioQueue, isAudioPlaying]);
  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.src = '';
      }
      messageQueue.forEach((item) => {
        if (item.audioUrl) {
          URL.revokeObjectURL(item.audioUrl);
        }
      });
    };
  }, []);

  return (
    <McFlex position="relative" mx="20px" orient="bottom" w="300px" col>
      <VStack spacing={4} width="100%" h="100%" pt="10px">
        <McFlex gap={3} orient="top">
          <Button
            bg="linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%)"
            color="white"
            onClick={() => handlePlayerTurn(1)}
            width="35%"
            size="lg"
            fontWeight="900"
            fontFamily="'Press Start 2P', monospace"
            fontSize="10px"
            letterSpacing="1px"
            textTransform="uppercase"
            transition="all 0.2s"
            boxShadow="0 4px 0 #4C1D95, 0 6px 8px rgba(0, 0, 0, 0.3)"
            border="2px solid #4C1D95"
            borderRadius="8px"
            _hover={{
              transform: 'translateY(-0.5px)',
              boxShadow: '0 6px 0 #4C1D95, 0 8px 12px rgba(0, 0, 0, 0.4)',
              bg: 'linear-gradient(135deg, #9F7AEA 0%, #7C3AED 100%)',
            }}
            _active={{
              transform: 'translateY(2px)',
              boxShadow: '0 2px 0 #4C1D95, 0 4px 6px rgba(0, 0, 0, 0.3)',
            }}
            _disabled={{
              bg: 'gray.400',
              boxShadow: 'none',
              transform: 'none',
              cursor: 'not-allowed',
            }}
          >
            Ash
          </Button>
          <Button
            bg="linear-gradient(135deg, #F87171 0%, #DC2626 100%)"
            color="white"
            onClick={() => handlePlayerTurn(2)}
            width="50%"
            size="lg"
            fontWeight="900"
            fontFamily="'Press Start 2P', monospace"
            fontSize="10px"
            letterSpacing="1px"
            textTransform="uppercase"
            transition="all 0.2s"
            boxShadow="0 4px 0 #991B1B, 0 6px 8px rgba(0, 0, 0, 0.3)"
            border="2px solid #991B1B"
            borderRadius="8px"
            _hover={{
              transform: 'translateY(-0.5px)',
              boxShadow: '0 6px 0 #991B1B, 0 8px 12px rgba(0, 0, 0, 0.4)',
              bg: 'linear-gradient(135deg, #FCA5A5 0%, #EF4444 100%)',
            }}
            _active={{
              transform: 'translateY(2px)',
              boxShadow: '0 2px 0 #991B1B, 0 4px 6px rgba(0, 0, 0, 0.3)',
            }}
            _disabled={{
              bg: 'gray.400',
              boxShadow: 'none',
              transform: 'none',
              cursor: 'not-allowed',
            }}
          >
            Team Rocket
          </Button>
        </McFlex>
        <Box position="relative" mb="20px">
          <Box
            bg="rgba(0, 0, 0, 0.7)"
            borderRadius="8px"
            padding="15px"
            boxShadow="0 4px 0 rgba(0, 0, 0, 0.3), 0 6px 8px rgba(0, 0, 0, 0.4)"
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
            border="2px solid rgba(255, 255, 255, 0.1)"
          >
            <Text
              fontFamily="'Press Start 2P', monospace"
              fontSize="10px"
              color="white"
              whiteSpace="pre-wrap"
              lineHeight="1.8"
              letterSpacing="0.5px"
              textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
              css={{
                fontFeatureSettings: '"tnum"',
                fontVariantNumeric: 'tabular-nums',
                textRendering: 'optimizeLegibility',
                WebkitFontSmoothing: 'antialiased',
                MozOsxFontSmoothing: 'grayscale',
              }}
            >
              {displayedText}
              {isLoading && (
                <Box
                  as="span"
                  borderRight="2px solid white"
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
              bottom="-24px"
              left="50%"
              transform="translateX(-50%)"
              width="0"
              height="0"
              borderLeft="20px solid transparent"
              borderRight="20px solid transparent"
              borderTop="20px solid rgba(0, 0, 0, 0.326)"
            />
          )}
        </Box>

        <McFlex width="300px" autoH>
          <motion.div
            initial={{ opacity: 0, scale: 1 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3, ease: 'easeInOut', delay: 2 }}
          >
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
          </motion.div>
        </McFlex>
      </VStack>
    </McFlex>
  );
};

export default Agent;
