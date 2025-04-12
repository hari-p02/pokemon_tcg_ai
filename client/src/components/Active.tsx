import McFlex from '../McFlex/McFlex';
import { Pokemon } from '../boardState';

interface ActiveProps {
  active: Pokemon | null;
}

const Active = ({ active }: ActiveProps) => {
  return (
    <McFlex border="1px solid black" p={2}>
      Active
    </McFlex>
  );
};

export default Active;
