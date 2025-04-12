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
    <McFlex gap={4} mb={isOpponent ? '0px' : '80px'}>
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
                borderRadius="md"
                filter="drop-shadow(0 8px 12px rgba(0,0,0,0.45)) drop-shadow(0 16px 24px rgba(0,0,0,0.3))"
                style={{
                  transform: 'perspective(800px) rotateX(10deg)',
                  transformStyle: 'preserve-3d',
                }}
                _before={{
                  content: '""',
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  right: 0,
                  bottom: 0,
                  background:
                    'linear-gradient(135deg, rgba(255,255,255,0.5) 0%, rgba(255,255,255,0) 50%, rgba(0,0,0,0.2) 100%)',
                  pointerEvents: 'none',
                  borderRadius: 'md',
                  backdropFilter: 'brightness(1.1)',
                }}
                whileHover={{
                  scale: 1.1,
                  rotateY: 5,
                  rotateX: 3,
                  y: -5,
                  filter:
                    'drop-shadow(0 16px 32px rgba(0,0,0,0.5)) drop-shadow(0 24px 48px rgba(0,0,0,0.35))',
                  boxShadow: '0px 0px 20px rgba(255,215,0,0.7)',
                  transition: { duration: 0.2 },
                }}
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
