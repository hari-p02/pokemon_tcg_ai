import McFlex from '../McFlex/McFlex';
import McGrid from '../McGrid/McGrid';
import { Card } from '../boardState';
import sleeveImage from '../assets/sleeve.png';
import { Image } from '@chakra-ui/react';
import { motion } from 'framer-motion';

const MotionImage = motion(Image);

interface PrizeCardsProps {
  prizeCards: Card[] | null;
}

const PrizeCards = ({ prizeCards }: PrizeCardsProps) => {
  return (
    <McFlex>
      <McGrid templateColumns="1fr 1fr" gap={1} auto>
        {prizeCards?.map((_, index) => (
          <MotionImage
            key={index}
            src={sleeveImage}
            alt="Prize Card"
            style={{ width: 'auto', height: '100px' }}
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
