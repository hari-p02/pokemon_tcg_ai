import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';

interface DiscardProps {
  discard: Card[] | null;
}

const Discard = ({ discard }: DiscardProps) => {
  return (
    <McFlex border="1px solid black" p={2}>
      Discard
    </McFlex>
  );
};

export default Discard;
