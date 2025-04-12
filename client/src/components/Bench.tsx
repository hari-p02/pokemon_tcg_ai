/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import { Image } from '@chakra-ui/react';
import McFlex from '../McFlex/McFlex';
import { Pokemon } from '../boardState';

interface BenchProps {
  bench: Pokemon[] | null;
}

const Bench = ({ bench }: BenchProps) => {
  return (
    <McFlex gap={1}>
      {bench?.map((pokemon, index) => (
        <Image
          key={index}
          src={pokemon.info.images.large}
          alt={pokemon.info.name}
          height="100px"
          width="auto"
        />
      ))}
    </McFlex>
  );
};

export default Bench;
