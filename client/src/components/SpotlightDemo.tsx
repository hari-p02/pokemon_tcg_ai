import { Button, VStack, HStack, Text, Box } from '@chakra-ui/react';
import { useState } from 'react';
import useSpotlight from '../hooks/useSpotlight';
import { useCardMap } from '../App';

/**
 * Demo component to show how to programmatically spotlight cards
 * This can be used in tutorials, explanations, or any other UI that needs
 * to direct the user's attention to specific cards
 */
const SpotlightDemo = () => {
  const { spotlightCard, clearSpotlight } = useSpotlight();
  const cardMap = useCardMap();
  const [highlightOnly, setHighlightOnly] = useState(false);

  // Get a list of card IDs from the cardMap for testing
  const cardIds = Object.keys(cardMap)
    .map((id) => parseInt(id, 10))
    .slice(0, 5);

  return (
    <Box
      position="absolute"
      bottom="20px"
      right="20px"
      bg="white"
      p={4}
      borderRadius="md"
      boxShadow="lg"
      zIndex={9}
      maxW="300px"
    >
      <VStack spacing={4} align="stretch">
        <Text fontWeight="bold">Spotlight Demo</Text>

        <Button
          size="sm"
          colorScheme="blue"
          onClick={() => setHighlightOnly(!highlightOnly)}
        >
          Mode: {highlightOnly ? 'Highlight Only' : 'Full Spotlight'}
        </Button>

        <Text fontSize="sm">Click to spotlight:</Text>

        <HStack spacing={2} wrap="wrap">
          {cardIds.map((id) => (
            <Button
              key={id}
              size="sm"
              onClick={() => spotlightCard(id, highlightOnly)}
            >
              Card {id}
            </Button>
          ))}
        </HStack>

        <Button size="sm" colorScheme="red" onClick={clearSpotlight}>
          Clear Spotlight
        </Button>

        <Text fontSize="xs" color="gray.500">
          This demo shows how you can programmatically spotlight cards based on
          game state or tutorial steps.
        </Text>
      </VStack>
    </Box>
  );
};

export default SpotlightDemo;
