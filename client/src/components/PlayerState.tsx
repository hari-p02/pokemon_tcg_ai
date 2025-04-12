import { CSSProperties } from 'react';
import McGrid from '../McGrid/McGrid';
import { PlayerState as PlayerStateType } from '../boardState';
import Active from './Active';
import Bench from './Bench';
import Deck from './Deck';
import Discard from './Discard';
import Hand from './Hand';
import LostZone from './LostZone';
import PrizeCards from './PrizeCards';
import Stadium from './Stadium';
import McFlex from '../McFlex/McFlex';

interface PlayerStateProps {
  playerState: PlayerStateType;
  style?: CSSProperties;
  isOpponent?: boolean;
}

const PlayerState = ({
  playerState,
  style,
  isOpponent = false,
}: PlayerStateProps) => {
  return (
    <McGrid
      templateColumns="0.5fr 2fr 0.5fr"
      gap={4}
      style={style}
      pb="5px"
      bg="rgba(128, 128, 128, 0.3)"
      borderRadius="md"
    >
      {/* First column - Prize Cards */}
      <PrizeCards prizeCards={playerState.prizeCards} isOpponent={isOpponent} />

      {/* Second column - Nested grid with 3 rows */}
      <McGrid templateRows="1fr auto auto" gap={2}>
        <McGrid templateColumns="1fr 1fr 1fr">
          <Stadium stadium={playerState.stadium} isOpponent={isOpponent} />
          <Active active={playerState.active} isOpponent={isOpponent} />
          <LostZone lostZone={playerState.lostZone} isOpponent={isOpponent} />
        </McGrid>
        <Bench bench={playerState.bench} isOpponent={isOpponent} />
        <Hand hand={playerState.hand} isOpponent={isOpponent} />
      </McGrid>

      {/* Third column - Nested grid with 2 rows */}
      <McFlex col orient={isOpponent ? 'top' : 'top right'}>
        <Deck deck={playerState.deck} isOpponent={isOpponent} />
        <Discard discard={playerState.discard} isOpponent={isOpponent} />
      </McFlex>
    </McGrid>
  );
};

export default PlayerState;
