import McFlex from '../McFlex/McFlex';
import McGrid from '../McGrid/McGrid';
import { Card } from '../boardState';
import sleeveImage from '../assets/sleeve.png';
import cardBackImage from '../assets/cardback.png';
import { Image } from '@chakra-ui/react';
import { motion } from 'framer-motion';

const MotionImage = motion(Image);

interface PrizeCardsProps {
  prizeCards: Card[] | null;
  isOpponent?: boolean;
}

const PrizeCards = ({ prizeCards, isOpponent = false }: PrizeCardsProps) => {
  return (
    <McFlex orient="top" pt={5}>
      <McGrid templateColumns="1fr 1fr" gap={1} auto>
        {prizeCards?.map((_, index) => (
          <MotionImage
            key={index}
            src={isOpponent ? cardBackImage : sleeveImage}
            alt="Prize Card"
            style={{ width: 'auto', height: '80px' }}
            borderRadius="md"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
              duration: 0.4,
              delay: index * 0.1,
              ease: 'easeOut',
            }}
            whileHover={{
              scale: 1.05,
              rotate: index % 2 === 0 ? 2 : -2,
            }}
          />
        ))}
      </McGrid>
    </McFlex>
  );
};

export default PrizeCards;
