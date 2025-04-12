import { Image } from '@chakra-ui/react';
import McFlex from '../McFlex/McFlex';
import { Card } from '../boardState';

interface HandProps {
  hand: Card[] | null;
}

const Hand = ({ hand }: HandProps) => {
  return (
    <McFlex gap={1}>
      {hand?.map((card, index) => (
        <Image
          key={index}
          src={card.info.images.large}
          alt={card.info.name}
          height="100px"
          width="auto"
        />
      ))}
    </McFlex>
  );
};

export default Hand;
