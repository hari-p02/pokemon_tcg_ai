import { Box, Image } from '@chakra-ui/react';
import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';
import sleeveImage from '../assets/sleeve.png';
import cardBackImage from '../assets/cardback.png';
import { motion } from 'framer-motion';

const MotionBox = motion(Box);

interface DeckProps {
  deck: Card[] | null;
  isOpponent?: boolean;
  isPlayerTwo?: boolean;
}

const Deck = ({ deck, isOpponent = false, isPlayerTwo = false }: DeckProps) => {
  // Number of visible cards in the stack
  const stackSize = 5;

  return (
    <McFlex p={2} auto>
      <MotionBox
        position="relative"
        width="75px"
        height="100px"
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{
          type: 'spring',
          stiffness: 400,
          damping: 17,
        }}
        whileHover={{
          scale: 1.05,
          rotate: 2,
          transition: { duration: 0.2 },
        }}
      >
        {[...Array(stackSize)].map((_, index) => (
          <Box
            key={index}
            position="absolute"
            top={`${index * 1}px`}
            left={`${index * 1}px`}
            transform={`scale(${1 - index * 0.01})`}
          >
            <Image
              borderRadius="md"
              src={isPlayerTwo ? cardBackImage : sleeveImage}
              alt="Deck"
              width="75px"
              height="100px"
              boxShadow={
                index === 0
                  ? 'lg'
                  : `0 ${2 + index}px ${1 + index}px rgba(0, 0, 0, 0.2)`
              }
            />
          </Box>
        ))}
      </MotionBox>
    </McFlex>
  );
};

export default Deck;
