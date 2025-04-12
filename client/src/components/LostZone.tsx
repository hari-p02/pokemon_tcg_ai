import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';
import { Image } from '@chakra-ui/react';
import { motion } from 'framer-motion';
import { useCardMap } from '../App';
import SpotlightableCard from './SpotlightableCard';

const MotionImage = motion(Image);

interface LostZoneProps {
  lostZone: Card[] | null;
  isOpponent?: boolean;
}

const LostZone = ({ lostZone, isOpponent = false }: LostZoneProps) => {
  const cardMap = useCardMap();
  const lastCard =
    lostZone && lostZone.length > 0 ? lostZone[lostZone.length - 1] : null;

  if (!lastCard || !cardMap[lastCard.id]) return <McFlex></McFlex>;

  const cardInfo = cardMap[lastCard.id];

  return (
    <McFlex p={2}>
      <SpotlightableCard cardId={lastCard.id} cardImage={cardInfo.images.large}>
        <MotionImage
          src={cardInfo.images.large}
          alt={cardInfo.name || 'Lost Zone Card'}
          height="100px"
          width="auto"
          borderRadius="md"
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          whileHover={{ scale: 1.05, filter: 'brightness(1.1)' }}
        />
      </SpotlightableCard>
    </McFlex>
  );
};

export default LostZone;
