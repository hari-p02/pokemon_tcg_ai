import { Image, Box, Flex } from '@chakra-ui/react';
import McFlex from '../McFlex/McFlex';
import { Pokemon } from '../boardState';
import { motion } from 'framer-motion';
import { useCardMap } from '../App';
import SpotlightableCard from './SpotlightableCard';

const MotionBox = motion(Box);
const MotionImage = motion(Image);

interface ActiveProps {
  active: Pokemon | null;
  isOpponent?: boolean;
}

const Active = ({ active, isOpponent = false }: ActiveProps) => {
  const cardMap = useCardMap();

  if (!active || !cardMap[active.id]) return <McFlex></McFlex>;

  const cardInfo = cardMap[active.id];
  const cardImage = cardInfo.images.large;

  return (
    <McFlex>
      {active && (
        <MotionBox
          position="relative"
          initial={{ scale: 0 }}
          animate={{
            scale: 1,
            transition: {
              type: 'spring',
              damping: 15,
              stiffness: 200,
            },
          }}
        >
          <SpotlightableCard cardId={active.id} cardImage={cardImage}>
            <MotionImage
              src={cardImage}
              alt={cardInfo.name}
              height="150px"
              width="auto"
              whileHover={{
                scale: 1.05,
                boxShadow: '0px 0px 8px rgba(255,215,0,0.6)',
              }}
            />
          </SpotlightableCard>

          {active.attachedCards && active.attachedCards.length > 0 && (
            <Flex position="absolute" top="0" right="0" direction="column">
              {active.attachedCards.map((card, cardIndex) => {
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
      )}
    </McFlex>
  );
};

export default Active;
