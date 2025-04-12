import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';
import { Image } from '@chakra-ui/react';

interface LostZoneProps {
  lostZone: Card[] | null;
}

const LostZone = ({ lostZone }: LostZoneProps) => {
  const lastCard =
    lostZone && lostZone.length > 0 ? lostZone[lostZone.length - 1] : null;

  if (!lastCard) return <McFlex></McFlex>;

  return (
    <McFlex p={2}>
      <Image
        src={lastCard.info.imageUrl}
        alt={lastCard.info.name || 'Lost Zone Card'}
        height="100px"
        width="auto"
        borderRadius="md"
      />
    </McFlex>
  );
};

export default LostZone;
