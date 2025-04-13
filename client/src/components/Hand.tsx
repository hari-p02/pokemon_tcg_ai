import { Image } from '@chakra-ui/react';
import { motion } from 'framer-motion';
import { useCardMap } from '../App';
import McFlex from '../McFlex/McFlex';
import cardBackImage from '../assets/cardback.png';
import sleeveImage from '../assets/sleeve.png';
import { Card } from '../boardState';
import SpotlightableCard from './SpotlightableCard';

const MotionImage = motion(Image);

interface HandProps {
  hand: Card[] | null;
  isOpponent?: boolean;
  isPlayerTwo?: boolean;
}

const Hand = ({ hand, isOpponent = false, isPlayerTwo = false }: HandProps) => {
  const cardMap = useCardMap();

  if (!hand || hand.length === 0 || !cardMap[hand[0].id])
    return <McFlex h="40px"></McFlex>;

  return (
    <McFlex gap={2} bg="rgba(128, 128, 128, 0.3)" p={2} borderRadius="md">
      {hand?.map((card, index) => {
        const cardInfo = cardMap[card.id];
        const cardImage = isOpponent
          ? isPlayerTwo
            ? cardBackImage
            : sleeveImage
          : cardInfo.images.large;

        return (
          <SpotlightableCard key={index} cardId={card.id} cardImage={cardImage}>
            <MotionImage
              src={cardImage}
              alt={isPlayerTwo ? 'Card Back' : cardInfo.name}
              height="100px"
              borderRadius="md"
              width="auto"
              filter="drop-shadow(0 8px 12px rgba(0,0,0,0.4)) drop-shadow(0 16px 24px rgba(0,0,0,0.25))"
              style={{
                transform: 'perspective(800px) rotateX(8deg)',
                transformStyle: 'preserve-3d',
              }}
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
              initial={{ scale: 0, y: 20 }}
              animate={{
                scale: 1,
                y: 0,
                transition: {
                  type: 'spring',
                  damping: 15,
                  stiffness: 200,
                  delay: index * 0.2,
                },
              }}
              whileHover={{
                y: -10,
                scale: 1.08,
                rotateY: index % 2 === 0 ? 5 : -5,
                rotateX: 2,
                filter:
                  'drop-shadow(0 16px 32px rgba(0,0,0,0.45)) drop-shadow(0 24px 48px rgba(0,0,0,0.3))',
                boxShadow: '0px 0px 25px rgba(255,215,0,0.7)',
                transition: { duration: 0.2 },
              }}
            />
          </SpotlightableCard>
        );
      })}
    </McFlex>
  );
};

export default Hand;
