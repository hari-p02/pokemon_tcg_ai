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
  isInactive?: boolean;
  isPlayerTwo?: boolean;
  activePlayer?: number;
}

const PlayerState = ({
  playerState,
  style,
  isInactive: isOpponent = false,
  isPlayerTwo = false,
  activePlayer,
}: PlayerStateProps) => {
  return (
    <McGrid
      templateColumns="0.5fr 2fr 0.5fr"
      gap={4}
      style={style}
      pb="5px"
      bg={isPlayerTwo ? 'rgba(186, 118, 118, 0.3)' : 'rgba(136, 88, 136, 0.3)'}
      borderRadius={isOpponent ? '15px' : 'md'}
      mb={isOpponent ? '10px' : '20px'}
    >
      {/* First column - Prize Cards */}
      <PrizeCards
        prizeCards={playerState.prizeCards}
        isOpponent={isOpponent}
        isPlayerTwo={isPlayerTwo}
        activePlayer={activePlayer}
      />

      {/* Second column - Nested grid with 3 rows */}
      <McGrid templateRows="1fr auto auto" gap={2}>
        <McGrid templateColumns="1fr 1fr 1fr">
          <Stadium
            stadium={playerState.stadium}
            isOpponent={isOpponent}
            activePlayer={activePlayer}
          />
          <Active
            active={playerState.active}
            isOpponent={isOpponent}
            activePlayer={activePlayer}
          />
          <LostZone
            lostZone={playerState.lostZone}
            isOpponent={isOpponent}
            activePlayer={activePlayer}
          />
        </McGrid>
        <Bench
          bench={playerState.bench}
          isOpponent={isOpponent}
          activePlayer={activePlayer}
        />
        <Hand
          hand={playerState.hand}
          isOpponent={isOpponent}
          isPlayerTwo={isPlayerTwo}
          activePlayer={activePlayer}
        />
      </McGrid>

      {/* Third column - Nested grid with 2 rows */}
      <McFlex col orient={isOpponent ? 'top' : 'top right'}>
        <Deck
          deck={playerState.deck}
          isOpponent={isOpponent}
          isPlayerTwo={isPlayerTwo}
          activePlayer={activePlayer}
        />
        <Discard
          discard={playerState.discard}
          isOpponent={isOpponent}
          activePlayer={activePlayer}
        />
      </McFlex>
    </McGrid>
  );
};

export default PlayerState;
