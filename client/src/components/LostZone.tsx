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
  activePlayer?: number;
}

const LostZone = ({
  lostZone,
  isOpponent = false,
  activePlayer,
}: LostZoneProps) => {
  const cardMap = useCardMap();
  const lastCard =
    lostZone && lostZone.length > 0 ? lostZone[lostZone.length - 1] : null;

  if (!lastCard || !cardMap[lastCard.id]) return <McFlex></McFlex>;

  const cardInfo = cardMap[lastCard.id];

  return (
    <McFlex p={2}>
      <SpotlightableCard cardId={lastCard.id} cardImage={cardInfo.images.large}>
        <MotionImage
          key={activePlayer}
          src={cardInfo.images.large}
          alt={cardInfo.name || 'Lost Zone Card'}
          height="100px"
          width="auto"
          borderRadius="md"
          filter="drop-shadow(0 8px 12px rgba(0,0,0,0.4)) drop-shadow(0 16px 24px rgba(0,0,0,0.25))"
          style={{
            transform: 'perspective(800px) rotateX(10deg)',
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
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          whileHover={{
            scale: 1.08,
            rotateY: 5,
            rotateX: 2,
            filter:
              'drop-shadow(0 16px 32px rgba(0,0,0,0.45)) drop-shadow(0 24px 48px rgba(0,0,0,0.3))',
            boxShadow: '0px 0px 25px rgba(255,215,0,0.7)',
            transition: { duration: 0.2 },
          }}
        />
      </SpotlightableCard>
    </McFlex>
  );
};

export default LostZone;
