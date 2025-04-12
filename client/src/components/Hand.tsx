import { Image } from '@chakra-ui/react';
import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';
import { motion } from 'framer-motion';

const MotionImage = motion(Image);

interface HandProps {
  hand: Card[] | null;
}

const Hand = ({ hand }: HandProps) => {
  return (
    <McFlex gap={1}>
      {hand?.map((card, index) => (
        <MotionImage
          key={index}
          src={card.info.images.large}
          alt={card.info.name}
          height="100px"
          width="auto"
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{
            duration: 0.3,
            delay: index * 0.05,
            type: 'spring',
            stiffness: 300,
          }}
          whileHover={{
            y: -10,
            scale: 1.05,
            transition: { duration: 0.2 },
          }}
          drag
          dragConstraints={{ left: 0, right: 0, top: 0, bottom: 0 }}
          dragElastic={0.2}
        />
      ))}
    </McFlex>
  );
};

export default Hand;
