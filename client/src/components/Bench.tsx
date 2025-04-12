/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import { Image, Box, Flex } from '@chakra-ui/react';
import McFlex from '../McFlex/McFlex';
import { Pokemon } from '../boardState';
import { motion } from 'framer-motion';
import { useCardMap } from '../App';
import SpotlightableCard from './SpotlightableCard';

const MotionBox = motion(Box);
const MotionImage = motion(Image);

interface BenchProps {
  bench: Pokemon[] | null;
  isOpponent?: boolean;
}

const Bench = ({ bench, isOpponent = false }: BenchProps) => {
  const cardMap = useCardMap();

  // Return empty flex when bench is empty or invalid
  if (!bench || bench.length === 0) return <McFlex></McFlex>;

  // Check if the first bench Pokémon exists in the card map
  if (!cardMap[bench[0].id]) return <McFlex></McFlex>;

  return (
    <McFlex gap={1} mb={isOpponent ? '0px' : '80px'}>
      {bench?.map((pokemon, index) => {
        const pokemonInfo = cardMap[pokemon.id];
        const pokemonImage = pokemonInfo.images.large;

        return (
          <MotionBox
            key={index}
            position="relative"
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <SpotlightableCard cardId={pokemon.id} cardImage={pokemonImage}>
              <MotionImage
                src={pokemonImage}
                alt={pokemonInfo.name}
                height="80px"
                width="auto"
                whileHover={{ y: -5 }}
              />
            </SpotlightableCard>

            {pokemon.attachedCards && pokemon.attachedCards.length > 0 && (
              <Flex position="absolute" top="0" right="0" direction="column">
                {pokemon.attachedCards.map((card, cardIndex) => {
                  const attachedCardInfo = cardMap[card.id];
                  const attachedCardImage = attachedCardInfo.images.large;

                  return (
                    <SpotlightableCard
                      key={cardIndex}
                      cardId={card.id}
                      cardImage={attachedCardImage}
                    >
                      <MotionImage
                        src={attachedCardImage}
                        alt={attachedCardInfo.name || 'Attached card'}
                        height="30px"
                        width="auto"
                        transform="rotate(15deg)"
                        border="1px solid white"
                        borderRadius="2px"
                        boxShadow="0px 0px 3px rgba(0,0,0,0.3)"
                        marginTop="-5px"
                        initial={{ scale: 0, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        transition={{
                          duration: 0.2,
                          delay: 0.3 + cardIndex * 0.1,
                        }}
                      />
                    </SpotlightableCard>
                  );
                })}
              </Flex>
            )}
          </MotionBox>
        );
      })}
    </McFlex>
  );
};

export default Bench;
