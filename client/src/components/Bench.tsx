/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import { Image, Box, Flex } from '@chakra-ui/react';
import McFlex from '../McFlex/McFlex';
import { Pokemon } from '../boardState';
import { motion } from 'framer-motion';

const MotionBox = motion(Box);
const MotionImage = motion(Image);

interface BenchProps {
  bench: Pokemon[] | null;
}

const Bench = ({ bench }: BenchProps) => {
  return (
    <McFlex gap={1}>
      {bench?.map((pokemon, index) => (
        <MotionBox
          key={index}
          position="relative"
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.3, delay: index * 0.1 }}
        >
          <MotionImage
            src={pokemon.info.images.large}
            alt={pokemon.info.name}
            height="100px"
            width="auto"
            whileHover={{ y: -5 }}
          />
          {pokemon.attachedCards && pokemon.attachedCards.length > 0 && (
            <Flex position="absolute" top="0" right="0" direction="column">
              {pokemon.attachedCards.map((card, cardIndex) => (
                <MotionImage
                  key={cardIndex}
                  src={card.info.images.large}
                  alt={card.info.name || 'Attached card'}
                  height="30px"
                  width="auto"
                  transform="rotate(15deg)"
                  border="1px solid white"
                  borderRadius="2px"
                  boxShadow="0px 0px 3px rgba(0,0,0,0.3)"
                  marginTop="-5px"
                  initial={{ scale: 0, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ duration: 0.2, delay: 0.3 + cardIndex * 0.1 }}
                />
              ))}
            </Flex>
          )}
        </MotionBox>
      ))}
    </McFlex>
  );
};

export default Bench;
