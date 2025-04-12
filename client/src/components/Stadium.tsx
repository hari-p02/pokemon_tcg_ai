import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';
import { Image } from '@chakra-ui/react';

interface StadiumProps {
  stadium: Card | null;
}

const Stadium = ({ stadium }: StadiumProps) => {
  if (!stadium) return <McFlex></McFlex>;

  return (
    <McFlex>
      <Image
        src={stadium.info.imageUrl}
        alt={stadium.info.name || 'Stadium Card'}
        style={{ width: 'auto', height: '100px' }}
        borderRadius="md"
      />
    </McFlex>
  );
};

export default Stadium;
