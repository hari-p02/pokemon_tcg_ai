import {
  useSetSpotlightCard,
  useCardMap,
  useSetHighlightedCardId,
} from '../App';

/**
 * Custom hook to programmatically spotlight a card from anywhere in the application
 * Can be used to spotlight a card without relying on the user clicking it
 */
function useSpotlight() {
  const setSpotlightCard = useSetSpotlightCard();
  const setHighlightedCardId = useSetHighlightedCardId();
  const cardMap = useCardMap();

  /**
   * Spotlight a card by its ID
   * @param cardId The ID of the card to spotlight
   * @param highlightOnly If true, only highlight the card without opening the spotlight overlay
   */
  const spotlightCard = (cardId: number | null, highlightOnly = false) => {
    if (cardId === null) {
      // Clear spotlight and highlight
      setHighlightedCardId(null);
      setSpotlightCard(null);
      return;
    }

    if (!cardMap[cardId]) {
      console.error(`Card with ID ${cardId} not found in cardMap`);
      return;
    }

    // Set the highlighted card ID
    setHighlightedCardId(cardId);

    // If highlightOnly is false, also open the spotlight overlay
    if (!highlightOnly) {
      const cardInfo = cardMap[cardId];
      setSpotlightCard({
        id: cardId,
        img: cardInfo.images.large,
      });
    }
  };

  /**
   * Clear the current spotlight/highlight
   */
  const clearSpotlight = () => {
    setHighlightedCardId(null);
    setSpotlightCard(null);
  };

  return { spotlightCard, clearSpotlight };
}

export default useSpotlight;
