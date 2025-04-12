import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';

interface LostZoneProps {
  lostZone: Card[] | null;
}

const LostZone = ({ lostZone }: LostZoneProps) => {
  return (
    <McFlex border="1px solid black" p={2}>
      Lost Zone
    </McFlex>
  );
};

export default LostZone;
