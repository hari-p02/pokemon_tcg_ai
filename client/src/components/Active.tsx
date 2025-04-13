import { Image, Box, Flex, Text } from '@chakra-ui/react';
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
  activePlayer?: number;
}

const Active = ({ active, isOpponent = false, activePlayer }: ActiveProps) => {
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
              delay: 0.5,
            },
          }}
          key={activePlayer}
        >
          <SpotlightableCard cardId={active.id} cardImage={cardImage}>
            {active.hp > 0 && (
              <Box
                position="absolute"
                top="-8px"
                right="-2px"
                zIndex={1}
                width="30px"
                height="30px"
                borderRadius="50%"
                backgroundColor="blue.500"
                border="2px solid white"
                boxShadow="0 2px 4px rgba(0,0,0,0.3), 0 4px 8px rgba(0,0,0,0.2)"
                display="flex"
                alignItems="center"
                justifyContent="center"
              >
                <Text
                  color="white"
                  fontWeight="900"
                  fontFamily="'Press Start 2P', monospace"
                  fontSize="6px"
                  letterSpacing="1px"
                  textTransform="uppercase"
                  textShadow="2px 2px 0 rgba(0, 0, 0, 0.5)"
                >
                  {active.hp}
                </Text>
              </Box>
            )}
            <MotionImage
              src={cardImage}
              alt={cardInfo.name}
              height="150px"
              width="auto"
              borderRadius="md"
              filter="drop-shadow(0 12px 16px rgba(0,0,0,0.45)) drop-shadow(0 24px 32px rgba(0,0,0,0.3)) drop-shadow(0 -2px 8px rgba(255,255,255,0.15))"
              style={{
                transform: 'perspective(800px) rotateX(12deg)',
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
                scale: 1.12,
                rotateY: 8,
                rotateX: 5,
                filter:
                  'drop-shadow(0 24px 48px rgba(0,0,0,0.5)) drop-shadow(0 32px 64px rgba(0,0,0,0.35)) drop-shadow(0 -4px 12px rgba(255,255,255,0.2))',
                boxShadow: '0px 0px 30px rgba(255,215,0,0.8)',
                transition: { duration: 0.3 },
              }}
            />
            {active.attachedCards && active.attachedCards.length > 0 && (
              <Flex position="absolute" top="0" left="-12px" direction="column">
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
                        height="40px"
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
          </SpotlightableCard>
        </MotionBox>
      )}
    </McFlex>
  );
};

export default Active;
