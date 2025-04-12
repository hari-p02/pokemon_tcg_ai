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
}

const Stadium = ({ stadium, isOpponent = false }: StadiumProps) => {
  const cardMap = useCardMap();

  if (!stadium || !cardMap[stadium.id]) return <McFlex></McFlex>;

  const stadiumInfo = cardMap[stadium.id];
  const cardImage = stadiumInfo.images.large;

  return (
    <McFlex>
      <SpotlightableCard cardId={stadium.id} cardImage={cardImage}>
        <MotionImage
          src={cardImage}
          alt={stadiumInfo.name || 'Stadium Card'}
          style={{ width: 'auto', height: '100px' }}
          borderRadius="md"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{
            duration: 0.6,
            ease: [0.175, 0.885, 0.32, 1],
          }}
          whileHover={{
            rotate: 2,
            boxShadow: '0px 5px 15px rgba(0,0,0,0.2)',
          }}
        />
      </SpotlightableCard>
    </McFlex>
  );
};

export default Stadium;
