import McFlex from '../McFlex/McFlex';
import { Pokemon } from '../boardState';

interface BenchProps {
  bench: Pokemon[] | null;
}

const Bench = ({ bench }: BenchProps) => {
  return (
    <McFlex border="1px solid black" p={2}>
      Bench
    </McFlex>
  );
};

export default Bench;
