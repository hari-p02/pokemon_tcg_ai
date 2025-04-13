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
  isPlayerTwo?: boolean;
  activePlayer?: number;
}

const PrizeCards = ({
  prizeCards,
  isOpponent = false,
  isPlayerTwo = false,
  activePlayer,
}: PrizeCardsProps) => {
  return (
    <McFlex
      orient={isOpponent ? 'top left' : 'top'}
      pt={5}
      pl={isOpponent ? '15px' : '0px'}
    >
      <McGrid templateColumns="1fr 1fr" gap={1} auto>
        {prizeCards?.map((_, index) => (
          <MotionImage
            key={`${index}-${activePlayer}`}
            src={isPlayerTwo ? cardBackImage : sleeveImage}
            alt="Prize Card"
            style={{
              width: 'auto',
              height: '80px',
              transform: 'perspective(800px) rotateX(10deg)',
              transformStyle: 'preserve-3d',
            }}
            borderRadius="md"
            filter="drop-shadow(0 8px 12px rgba(0,0,0,0.4)) drop-shadow(0 16px 24px rgba(0,0,0,0.25))"
            _before={{
              content: '""',
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background:
                'linear-gradient(135deg, rgba(255,255,255,0.5) 0%, rgba(255,255,255,0) 50%, rgba(0,0,0,0.15) 100%)',
              pointerEvents: 'none',
              borderRadius: 'md',
              backdropFilter: 'brightness(1.1)',
            }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
              duration: 0.4,
              delay: index * 0.1,
              ease: 'easeOut',
            }}
            whileHover={{
              scale: 1.08,
              rotateY: index % 2 === 0 ? 5 : -5,
              rotateX: 2,
              filter:
                'drop-shadow(0 16px 32px rgba(0,0,0,0.45)) drop-shadow(0 24px 48px rgba(0,0,0,0.3))',
              boxShadow: '0px 0px 20px rgba(255,215,0,0.6)',
              transition: { duration: 0.2 },
            }}
          />
        ))}
      </McGrid>
    </McFlex>
  );
};

export default PrizeCards;
