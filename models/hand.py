from itertools import product

from models.card import Card


class Hand:
    def __init__(self):
        self._cards: list[Card] = list()

    def add(self, *new_cards: Card) -> int:
        # Allows adding 2 cards in one go when starting a new round
        for new_card in new_cards:
            self._cards.append(new_card)
        return self.score

    def drop(self) -> list[Card]:
        cards = self._cards
        self._cards = []
        return cards

    @property
    def size(self) -> int:
        return len(self._cards)

    @property
    def cards(self) -> list[Card]:
        return self._cards

    # Score refer to the total score in the current hand
    #  Computed on the fly as it is always changing, based on what's on hand
    @property
    def score(self) -> int:
        # Accounts for the rule that Ace can be 1 or 11, whichever is more favourable
        n_aces = len([card for card in self._cards if card.is_ace()])
        sum_non_aces = sum([card.value for card in self._cards if not card.is_ace()])
        if n_aces == 0:
            return sum_non_aces
        possible_sum_aces = [sum(res) for res in product([1, 11], repeat=n_aces)]
        possible_scores = [sum_non_aces + sum_aces for sum_aces in possible_sum_aces]
        filtered_scores = [score for score in possible_scores if score <= 21]
        if filtered_scores == []:  # All exceed 21
            return min(possible_scores)
        return max(filtered_scores)

    def is_blackjack(self) -> bool:
        # Blackjack occurs when:
        # 1. 2 cards on the hand AND
        # 2. Either of:
        #   (a) Both cards ACE OR
        #   (b) One card ACE, One card value 10 (KING, QUEEN, JACK or TEN)
        if len(self._cards) != 2:
            return False
        if (self._cards[0].is_ace() and self._cards[1].is_ace()) or \
            (self._cards[0].is_ace() and self._cards[1].value == 10) or \
            (self._cards[0].value == 10 and self._cards[1].is_ace()):
            return True
        return False

    def is_empty(self) -> bool:
        return self.size == 0
