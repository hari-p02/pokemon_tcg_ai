import { Image } from '@chakra-ui/react';
import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';
import sleeveImage from '../assets/sleeve.png';
import { motion } from 'framer-motion';

const MotionImage = motion(Image);

interface DeckProps {
  deck: Card[] | null;
}

const Deck = ({ deck }: DeckProps) => {
  return (
    <McFlex p={2}>
      <MotionImage
        borderRadius="md"
        src={sleeveImage}
        alt="Deck"
        height="100px"
        width="auto"
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
      />
    </McFlex>
  );
};

export default Deck;
