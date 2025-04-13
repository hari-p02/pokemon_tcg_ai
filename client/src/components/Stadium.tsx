import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';
import { Image } from '@chakra-ui/react';
import { motion } from 'framer-motion';
import { useCardMap } from '../App';
import SpotlightableCard from './SpotlightableCard';

const MotionImage = motion(Image);

interface StadiumProps {
  stadium: Card | null;
  isOpponent?: boolean;
  activePlayer?: number;
}

const Stadium = ({
  stadium,
  isOpponent = false,
  activePlayer,
}: StadiumProps) => {
  const cardMap = useCardMap();

  if (!stadium || !cardMap[stadium.id]) return <McFlex></McFlex>;

  const stadiumInfo = cardMap[stadium.id];
  const cardImage = stadiumInfo.images.large;

  return (
    <McFlex>
      <SpotlightableCard cardId={stadium.id} cardImage={cardImage}>
        <MotionImage
          key={activePlayer}
          src={cardImage}
          alt={stadiumInfo.name || 'Stadium Card'}
          style={{
            width: 'auto',
            height: '100px',
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
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{
            duration: 0.6,
            ease: [0.175, 0.885, 0.32, 1],
          }}
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

export default Stadium;
