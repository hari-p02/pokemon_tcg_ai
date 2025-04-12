import { Box, Image, Text } from '@chakra-ui/react';
import { keyframes } from '@emotion/react';
import axios from 'axios';
import { FC, useEffect, useRef, useState } from 'react';
import ashImage from '../assets/ash.png';
import brockImage from '../assets/brock.png';
import oakImage from '../assets/oak.png';
import McFlex from '../McFlex/McFlex';
import mistImage from '../assets/misty.png';

interface AgentProps {
  agent: string;
  message: string;
}

const Agent: FC<AgentProps> = ({ agent, message }) => {
  const [displayedText, setDisplayedText] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    // Reset animation when message changes
    setDisplayedText('');
    setCurrentIndex(0);

    if (message) {
      // Generate audio when message changes
      const voiceId =
        agent === 'Ash'
          ? // ? 'AZnzlk1XvdvUeBnXmlld'
            'MF3mGyEYCl7XYWbV9V6O'
          : agent === 'Brock'
            ? 'SOYHLrjzK2X1ezoPC6cr'
            : agent === 'Misty'
              ? 'jBpfuIE2acCO8z3wKNLl'
              : 'D38z5RcWu1voky8WS1ja';

      // Create audio element if it doesn't exist
      if (!audioRef.current) {
        audioRef.current = new Audio();
      }

      // Direct API call to ElevenLabs
      const apiKey = import.meta.env.VITE_ELEVENLABS_API_KEY;
      const apiUrl = `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`;

      // Make the API call
      axios({
        method: 'post',
        url: apiUrl,
        data: {
          text: message,
          model_id: 'eleven_turbo_v2',
          output_format: 'mp3',
        },
        headers: {
          'Content-Type': 'application/json',
          'xi-api-key': apiKey,
        },
        responseType: 'arraybuffer',
      })
        .then((response) => {
          // Convert array buffer to blob
          const blob = new Blob([response.data], { type: 'audio/mpeg' });
          const url = URL.createObjectURL(blob);

          if (audioRef.current) {
            audioRef.current.src = url;
            audioRef.current
              .play()
              .catch((err) => console.error('Error playing audio:', err));
          }
        })
        .catch((error) => {
          console.error('Error generating audio:', error);
        });

      // Clean up audio on unmount
      return () => {
        if (audioRef.current) {
          audioRef.current.pause();
          audioRef.current.src = '';
        }
      };
    }
  }, [message, agent]);

  useEffect(() => {
    if (currentIndex < message.length) {
      const typingTimer = setTimeout(() => {
        setDisplayedText((prev) => prev + message[currentIndex]);
        setCurrentIndex(currentIndex + 1);
      }, 30); // Typing speed (milliseconds per character)

      return () => clearTimeout(typingTimer);
    }
  }, [currentIndex, message]);

  const blinkAnimation = keyframes`
    from, to { border-color: transparent }
    50% { border-color: black }
  `;

  return (
    <McFlex position="relative" mx="20px" orient="bottom" w="300px" col>
      <Box
        bg="white"
        borderRadius="20px"
        padding="15px"
        boxShadow="md"
        width="250px"
        minHeight="80px"
        mb="20px"
        position="relative"
        _after={{
          content: '""',
          position: 'absolute',
          bottom: '-20px',
          left: '50%',
          transform: 'translateX(-50%)',
          width: '0',
          height: '0',
          borderLeft: '20px solid transparent',
          borderRight: '20px solid transparent',
          borderTop: '20px solid white',
        }}
      >
        <Text fontFamily="monospace" fontSize="md" color="black">
          {displayedText}
          <Box
            as="span"
            borderRight="2px solid black"
            display="inline-block"
            sx={{
              animation:
                currentIndex < message.length
                  ? `${blinkAnimation} 0.75s step-end infinite`
                  : 'none',
            }}
          />
        </Text>
      </Box>

      <McFlex width="300px" autoH>
        <Image
          src={
            agent === 'Ash'
              ? ashImage
              : agent === 'Brock'
                ? brockImage
                : agent === 'Misty'
                  ? mistImage
                  : oakImage
          }
          w="100%"
          alt={agent}
        />
      </McFlex>
    </McFlex>
  );
};

export default Agent;
