import { Box, Text, Image } from '@chakra-ui/react';
import { FC, useEffect, useState } from 'react';
import ashImage from '../assets/ash.png';

// Define the blinking animation
const blinkAnimation = `
  @keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0; }
    100% { opacity: 1; }
  }
`;

interface AgentProps {
  agent?: string;
  message?: string;
}

const Agent: FC<AgentProps> = ({ agent = 'Ash', message = '' }) => {
  const [displayedText, setDisplayedText] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    // Reset animation when message changes
    setDisplayedText('');
    setCurrentIndex(0);
  }, [message]);

  useEffect(() => {
    if (message && currentIndex < message.length) {
      const timeout = setTimeout(() => {
        setDisplayedText((prev) => prev + message[currentIndex]);
        setCurrentIndex((prev) => prev + 1);
      }, 50); // Speed of text animation

      return () => clearTimeout(timeout);
    }
  }, [message, currentIndex]);

  return (
    <Box position="relative" width="300px" height="400px" padding="10px">
      {/* Add the blink animation to the component */}
      <style>{blinkAnimation}</style>

      {/* Speech bubble */}
      <Box
        position="absolute"
        top="10px"
        left="50%"
        transform="translateX(-50%)"
        bg="white"
        borderRadius="20px"
        padding="15px"
        boxShadow="md"
        width="250px"
        minHeight="100px"
        zIndex="1"
        _after={{
          content: '""',
          position: 'absolute',
          bottom: '-15px',
          left: '50%',
          transform: 'translateX(-50%)',
          borderWidth: '15px',
          borderStyle: 'solid',
          borderColor: 'white transparent transparent transparent',
        }}
      >
        <Text fontFamily="monospace" fontSize="md">
          {displayedText}
          {currentIndex < (message?.length || 0) && (
            <Box
              as="span"
              sx={{
                display: 'inline-block',
                animation: 'blink 1s infinite',
                marginLeft: '2px',
              }}
            >
              _
            </Box>
          )}
        </Text>
      </Box>

      {/* Agent image */}
      <Box
        position="absolute"
        bottom="0"
        left="50%"
        transform="translateX(-50%)"
        width="200px"
      >
        <Image src={ashImage} alt={agent} />
      </Box>
    </Box>
  );
};

export default Agent;
