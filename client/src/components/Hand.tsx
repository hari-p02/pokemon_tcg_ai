import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';

interface HandProps {
  hand: Card[] | null;
}

const Hand = ({ hand }: HandProps) => {
  return (
    <McFlex border="1px solid black" p={2}>
      Hand
    </McFlex>
  );
};

export default Hand;
