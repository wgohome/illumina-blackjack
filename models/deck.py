from itertools import product
from random import shuffle as random_shuffle

from .card import Card, Suit, Rank

class Deck:
    def __init__(self):
        self._cards: list[Card] = [Card(rank, suit) for rank, suit in product(Rank, Suit)]
        self._discard_pile: list[Card] = []
        # Discard pile is abstracted here to allow for the cards to be reshuffled into the deck, if needed
        self._shuffle()

    def get_size(self) -> int:
        return len(self._cards)

    def hit(self) -> Card:
        return self._cards.pop()

    def _shuffle(self) -> None:
        # Shuffles list in place
        random_shuffle(self._cards)

    def send_to_discard(self, card: Card) -> None:
        self._discard_pile.append(card)
