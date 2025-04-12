import { ReactNode, useEffect } from 'react';
import { Box, Tooltip } from '@chakra-ui/react';
import { useSetSpotlightCard, useHighlightedCardId, useCardMap } from '../App';

interface SpotlightableCardProps {
  children: ReactNode;
  cardId: number;
  cardImage: string;
}

const SpotlightableCard = ({
  children,
  cardId,
  cardImage,
}: SpotlightableCardProps) => {
  const setSpotlightCard = useSetSpotlightCard();
  const highlightedCardId = useHighlightedCardId();
  const cardMap = useCardMap();

  // Check if this card is currently highlighted by the backend
  const isHighlightedByBackend = highlightedCardId === cardId;

  // If this card is highlighted by the backend, set it in the spotlight
  useEffect(() => {
    if (isHighlightedByBackend && cardMap[cardId]) {
      setSpotlightCard({ id: cardId, img: cardImage });
    }
  }, [isHighlightedByBackend, cardId, cardImage, cardMap, setSpotlightCard]);

  const handleSpotlight = (e: React.MouseEvent) => {
    // Stop propagation to prevent other click handlers from executing
    e.stopPropagation();

    // Set the spotlight card
    setSpotlightCard({ id: cardId, img: cardImage });
  };

  return (
    <Tooltip>
      <Box
        position="relative"
        onClick={handleSpotlight}
        cursor="pointer"
        className="spotlightable-card"
        _hover={{
          transform: 'scale(1.05)',
          transition: 'transform 0.2s ease',
          '&::after': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            borderRadius: 'md',
            zIndex: 1,
            pointerEvents: 'none',
          },
        }}
        sx={{
          // Apply pulsing highlight effect when this card is highlighted by the backend
          ...(isHighlightedByBackend && {
            '&::after': {
              content: '""',
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              boxShadow: '0 0 0 3px gold inset, 0 0 15px gold',
              borderRadius: 'md',
              zIndex: 1,
              pointerEvents: 'none',
              animation: 'pulse 1.5s infinite',
            },
            '@keyframes pulse': {
              '0%': { boxShadow: '0 0 0 3px gold inset, 0 0 10px gold' },
              '50%': { boxShadow: '0 0 0 3px gold inset, 0 0 20px gold' },
              '100%': { boxShadow: '0 0 0 3px gold inset, 0 0 10px gold' },
            },
          }),
        }}
      >
        {children}
      </Box>
    </Tooltip>
  );
};

export default SpotlightableCard;
