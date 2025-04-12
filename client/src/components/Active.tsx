import { Image } from '@chakra-ui/react';
import McFlex from '../McFlex/McFlex';
import { Pokemon } from '../boardState';

interface ActiveProps {
  active: Pokemon | null;
}

const Active = ({ active }: ActiveProps) => {
  return (
    <McFlex>
      <Image
        src={active?.info.images.large}
        alt={active?.info.name}
        height="150px"
        width="auto"
      />
    </McFlex>
  );
};

export default Active;
