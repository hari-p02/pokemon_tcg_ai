import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export interface Card {
  id: number;
}

export interface PokemonInPlay {
  id: number;
  hp: number;
  attachedCards?: Card[];
}

export interface PlayerState {
  active: PokemonInPlay | null;
  bench: PokemonInPlay[] | null;
  discard: Card[] | null;
  lostZone: Card[] | null;
  deck: Card[] | null;
  hand: Card[] | null;
  stadium: Card | null;
  prizeCards: Card[] | null;
}

export interface BoardState {
  playerOne: PlayerState;
  playerTwo: PlayerState;
  cardMap: Record<number, any>;
  highlightedCard?: number | null;
}

export const fetchGameState = async (
  preset: boolean = false
): Promise<BoardState> => {
  try {
    const response = await axios.get<BoardState>(
      `${API_BASE_URL}/state?preset=${preset}`
    );
    return response.data;
  } catch (error) {
    console.error('Error fetching game state:', error);
    throw error;
  }
};
