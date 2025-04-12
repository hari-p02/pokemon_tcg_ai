import { Image } from '@chakra-ui/react';
import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';
import sleeveImage from '../assets/sleeve.png';

interface DeckProps {
  deck: Card[] | null;
}

const Deck = ({ deck }: DeckProps) => {
  return (
    <McFlex p={2}>
      <Image
        borderRadius="md"
        src={sleeveImage}
        alt="Deck"
        height="100px"
        width="auto"
      />
    </McFlex>
  );
};

export default Deck;
