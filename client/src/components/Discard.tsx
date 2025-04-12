import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';
import { Image } from '@chakra-ui/react';
import { motion } from 'framer-motion';
import { useCardMap } from '../App';
import SpotlightableCard from './SpotlightableCard';

const MotionImage = motion(Image);

interface DiscardProps {
  discard: Card[] | null;
  isOpponent?: boolean;
}

const Discard = ({ discard, isOpponent = false }: DiscardProps) => {
  const cardMap = useCardMap();
  const lastCard =
    discard && discard.length > 0 ? discard[discard.length - 1] : null;

  if (!lastCard || !cardMap[lastCard.id]) return <McFlex></McFlex>;

  const cardInfo = cardMap[lastCard.id];
  const cardImage = cardInfo.images.large;

  return (
    <McFlex p={2} auto>
      <SpotlightableCard cardId={lastCard.id} cardImage={cardImage}>
        <MotionImage
          src={cardImage}
          alt={cardInfo.name || 'Discard Card'}
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
          initial={{ scale: 0, opacity: 0, rotate: -10 }}
          animate={{ scale: 1, opacity: 1, rotate: 0 }}
          transition={{ type: 'spring', stiffness: 260, damping: 20 }}
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

export default Discard;
