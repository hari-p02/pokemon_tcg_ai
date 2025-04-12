import McFlex from '../McFlex/McFlex';
import McGrid from '../McGrid/McGrid';
import { Card } from '../boardState';
import sleeveImage from '../assets/sleeve.png';
import { Image } from '@chakra-ui/react';

interface PrizeCardsProps {
  prizeCards: Card[] | null;
}

const PrizeCards = ({ prizeCards }: PrizeCardsProps) => {
  return (
    <McFlex>
      <McGrid templateColumns="1fr 1fr" gap={1} auto>
        {prizeCards?.map((_, index) => (
          <Image
            key={index}
            src={sleeveImage}
            alt="Prize Card"
            style={{ width: 'auto', height: '100px' }}
            borderRadius="md"
          />
        ))}
      </McGrid>
    </McFlex>
  );
};

export default PrizeCards;
