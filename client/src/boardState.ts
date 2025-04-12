interface Card {
  id: number;
}

interface PokemonInPlay {
  id: number;
  hp: number;
  attachedCards?: Card[];
}

interface PlayerState {
  active: PokemonInPlay | null;
  bench: PokemonInPlay[] | null;
  discard: Card[] | null;
  lostZone: Card[] | null;
  deck: Card[] | null;
  hand: Card[] | null;
  stadium: Card | null;
  prizeCards: Card[] | null;
}

interface BoardState {
  playerOne: PlayerState;
  playerTwo: PlayerState;
  cardMap: Record<number, any>;
}

export type { BoardState, PlayerState, PokemonInPlay as Pokemon, Card };
