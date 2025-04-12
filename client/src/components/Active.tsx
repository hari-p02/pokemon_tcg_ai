import { Image } from '@chakra-ui/react';
import McFlex from '../McFlex/McFlex';
import { Pokemon } from '../boardState';
import { motion } from 'framer-motion';
import { useCardMap } from '../App';
import SpotlightableCard from './SpotlightableCard';

const MotionImage = motion(Image);

interface ActiveProps {
  active: Pokemon | null;
  isOpponent?: boolean;
}

const Active = ({ active, isOpponent = false }: ActiveProps) => {
  const cardMap = useCardMap();

  if (!active || !cardMap[active.id]) return <McFlex></McFlex>;

  const cardInfo = cardMap[active.id];
  const cardImage = cardInfo.images.large;

  return (
    <McFlex>
      {active && (
        <SpotlightableCard cardId={active.id} cardImage={cardImage}>
          <MotionImage
            src={cardImage}
            alt={cardInfo.name}
            height="150px"
            width="auto"
            initial={{ scale: 0 }}
            animate={{
              scale: 1,
              transition: {
                type: 'spring',
                damping: 15,
                stiffness: 200,
              },
            }}
            whileHover={{
              scale: 1.05,
              boxShadow: '0px 0px 8px rgba(255,215,0,0.6)',
            }}
          />
        </SpotlightableCard>
      )}
    </McFlex>
  );
};

export default Active;
