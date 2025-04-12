import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';

interface StadiumProps {
  stadium: Card | null;
}

const Stadium = ({ stadium }: StadiumProps) => {
  return (
    <McFlex border="1px solid black" p={2}>
      Stadium
    </McFlex>
  );
};

export default Stadium;
