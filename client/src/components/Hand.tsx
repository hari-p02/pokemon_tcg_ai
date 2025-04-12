import { Image } from '@chakra-ui/react';
import { motion } from 'framer-motion';
import { useCardMap } from '../App';
import McFlex from '../McFlex/McFlex';
import cardBackImage from '../assets/cardback.png';
import { Card } from '../boardState';
import SpotlightableCard from './SpotlightableCard';

const MotionImage = motion(Image);

interface HandProps {
  hand: Card[] | null;
  isOpponent?: boolean;
}

const Hand = ({ hand, isOpponent = false }: HandProps) => {
  const cardMap = useCardMap();

  if (!hand || !cardMap[hand[0].id]) return <McFlex></McFlex>;

  return (
    <McFlex gap={1} bg="rgba(128, 128, 128, 0.3)" p={2} borderRadius="md">
      {hand?.map((card, index) => {
        const cardInfo = cardMap[card.id];
        const cardImage = isOpponent ? cardBackImage : cardInfo.images.large;

        return (
          <SpotlightableCard key={index} cardId={card.id} cardImage={cardImage}>
            <MotionImage
              src={cardImage}
              alt={isOpponent ? 'Card Back' : cardInfo.name}
              height="100px"
              borderRadius="md"
              width="auto"
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{
                duration: 0.3,
                delay: index * 0.05,
                type: 'spring',
                stiffness: 300,
              }}
              whileHover={{
                y: -10,
                scale: 1.05,
                transition: { duration: 0.2 },
              }}
              drag
              dragConstraints={{ left: 0, right: 0, top: 0, bottom: 0 }}
              dragElastic={0.2}
            />
          </SpotlightableCard>
        );
      })}
    </McFlex>
  );
};

export default Hand;
