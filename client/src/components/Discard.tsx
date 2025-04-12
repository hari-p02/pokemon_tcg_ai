import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';
import { Image } from '@chakra-ui/react';

interface DiscardProps {
  discard: Card[] | null;
}

const Discard = ({ discard }: DiscardProps) => {
  console.log(discard);
  const lastCard =
    discard && discard.length > 0 ? discard[discard.length - 1] : null;

  if (!lastCard) return <McFlex></McFlex>;

  return (
    <McFlex p={2}>
      <Image
        src={lastCard.info.imageUrl}
        alt={lastCard.info.name || 'Discard Card'}
        height="100px"
        width="auto"
        borderRadius="md"
      />
    </McFlex>
  );
};

export default Discard;
