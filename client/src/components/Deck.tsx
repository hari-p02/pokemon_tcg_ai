import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';

interface DeckProps {
  deck: Card[] | null;
}

const Deck = ({ deck }: DeckProps) => {
  return (
    <McFlex border="1px solid black" p={2}>
      Deck
    </McFlex>
  );
};

export default Deck;
