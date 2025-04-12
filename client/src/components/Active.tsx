import { Image } from '@chakra-ui/react';
import McFlex from '../McFlex/McFlex';
import { Pokemon } from '../boardState';
import { motion } from 'framer-motion';

const MotionImage = motion(Image);

interface ActiveProps {
  active: Pokemon | null;
}

const Active = ({ active }: ActiveProps) => {
  return (
    <McFlex>
      {active && (
        <MotionImage
          src={active.info.images.large}
          alt={active.info.name}
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
      )}
    </McFlex>
  );
};

export default Active;
