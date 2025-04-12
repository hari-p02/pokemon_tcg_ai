interface Card {
  id: string;
  details: any;
}

interface PokemonInPlay {
  id: string;
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
}

export type { BoardState, PlayerState, PokemonInPlay as Pokemon, Card };



