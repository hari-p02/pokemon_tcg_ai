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

interface PlayerStateProps {
  playerState: PlayerStateType;
  style?: CSSProperties;
}

const PlayerState = ({ playerState, style }: PlayerStateProps) => {
  return (
    <McGrid templateColumns="1fr 2fr 1fr" gap={4} style={style}>
      {/* First column - Prize Cards */}
      <PrizeCards prizeCards={playerState.prizeCards} />

      {/* Second column - Nested grid with 3 rows */}
      <McGrid templateRows="1fr auto auto" gap={2}>
        <McGrid templateColumns="1fr 1fr 1fr">
          <Stadium stadium={playerState.stadium} />
          <Active active={playerState.active} />
          <LostZone lostZone={playerState.lostZone} />
        </McGrid>
        <Bench bench={playerState.bench} />
        <Hand hand={playerState.hand} />
      </McGrid>

      {/* Third column - Nested grid with 2 rows */}
      <McGrid templateRows="1fr 1fr" gap={4}>
        <Deck deck={playerState.deck} />
        <Discard discard={playerState.discard} />
      </McGrid>
    </McGrid>
  );
};

export default PlayerState;
