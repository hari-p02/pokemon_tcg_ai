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
          initial={{ scale: 0, opacity: 0, rotate: -10 }}
          animate={{ scale: 1, opacity: 1, rotate: 0 }}
          transition={{ type: 'spring', stiffness: 260, damping: 20 }}
          whileHover={{ scale: 1.05 }}
        />
      </SpotlightableCard>
    </McFlex>
  );
};

export default Discard;
