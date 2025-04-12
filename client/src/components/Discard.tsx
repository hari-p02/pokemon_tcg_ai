import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';
import { Image } from '@chakra-ui/react';
import { motion } from 'framer-motion';

const MotionImage = motion(Image);

interface DiscardProps {
  discard: Card[] | null;
}

const Discard = ({ discard }: DiscardProps) => {
  const lastCard =
    discard && discard.length > 0 ? discard[discard.length - 1] : null;

  if (!lastCard) return <McFlex></McFlex>;

  return (
    <McFlex p={2}>
      <MotionImage
        src={lastCard.info.images.large}
        alt={lastCard.info.name || 'Discard Card'}
        height="100px"
        width="auto"
        borderRadius="md"
        initial={{ scale: 0, opacity: 0, rotate: -10 }}
        animate={{ scale: 1, opacity: 1, rotate: 0 }}
        transition={{ type: 'spring', stiffness: 260, damping: 20 }}
        whileHover={{ scale: 1.05 }}
      />
    </McFlex>
  );
};

export default Discard;
