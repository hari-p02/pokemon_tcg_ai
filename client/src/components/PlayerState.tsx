import McFlex from '../McFlex/McFlex';
import { PlayerState as PlayerStateType } from '../boardState';
import Active from './Active';
import Bench from './Bench';
import Discard from './Discard';
import LostZone from './LostZone';
import Deck from './Deck';
import Hand from './Hand';
import Stadium from './Stadium';
import PrizeCards from './PrizeCards';

interface PlayerStateProps {
  playerState: PlayerStateType;
}

const PlayerState = ({ playerState }: PlayerStateProps) => {
  return (
    <McFlex col gap={4} p={4}>
      <McFlex gap={4}>
        <Active active={playerState.active} />
        <Bench bench={playerState.bench} />
      </McFlex>

      <McFlex gap={4}>
        <Discard discard={playerState.discard} />
        <LostZone lostZone={playerState.lostZone} />
        <Deck deck={playerState.deck} />
      </McFlex>

      <McFlex gap={4}>
        <Hand hand={playerState.hand} />
        <Stadium stadium={playerState.stadium} />
        <PrizeCards prizeCards={playerState.prizeCards} />
      </McFlex>
    </McFlex>
  );
};

export default PlayerState;
