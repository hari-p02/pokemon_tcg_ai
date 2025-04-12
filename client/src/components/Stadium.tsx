import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';
import { Image } from '@chakra-ui/react';
import { motion } from 'framer-motion';

const MotionImage = motion(Image);

interface StadiumProps {
  stadium: Card | null;
}

const Stadium = ({ stadium }: StadiumProps) => {
  if (!stadium) return <McFlex></McFlex>;

  return (
    <McFlex>
      <MotionImage
        src={stadium.info.images.large}
        alt={stadium.info.name || 'Stadium Card'}
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
    </McFlex>
  );
};

export default Stadium;
