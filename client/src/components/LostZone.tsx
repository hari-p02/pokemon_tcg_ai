import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';
import { Image } from '@chakra-ui/react';
import { motion } from 'framer-motion';

const MotionImage = motion(Image);

interface LostZoneProps {
  lostZone: Card[] | null;
}

const LostZone = ({ lostZone }: LostZoneProps) => {
  const lastCard =
    lostZone && lostZone.length > 0 ? lostZone[lostZone.length - 1] : null;

  if (!lastCard) return <McFlex></McFlex>;

  return (
    <McFlex p={2}>
      <MotionImage
        src={lastCard.info.images.large}
        alt={lastCard.info.name || 'Lost Zone Card'}
        height="100px"
        width="auto"
        borderRadius="md"
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
        whileHover={{ scale: 1.05, filter: 'brightness(1.1)' }}
      />
    </McFlex>
  );
};

export default LostZone;
