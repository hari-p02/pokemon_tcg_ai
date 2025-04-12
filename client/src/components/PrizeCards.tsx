import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';

interface PrizeCardsProps {
  prizeCards: Card[] | null;
}

const PrizeCards = ({ prizeCards }: PrizeCardsProps) => {
  return (
    <McFlex border="1px solid black" p={2}>
      Prize Cards
    </McFlex>
  );
};

export default PrizeCards;
