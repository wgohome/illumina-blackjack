from itertools import product

from models.card import Card


class Participant:
    """
    Participant refer to either the dealer or the remaining players
    """
    counter: int = 0

    def __init__(self, name: str | None = None):
        Participant.counter += 1
        self._index: int = Participant.counter
        self.name: str = name or f"Participant no. {self._index}"
        self._points: int = 0  # points over multiple games
        self._hand: list[Card] = list()

    def __repr__(self):
        return f"<Participant(name={self.name}), index: {self._index}, points: {self.points}>"

    # Score refer to the total score in the current hand
    #  Computed on the fly as it is always changing, based on what's on hand
    @property
    def score(self) -> int:
        # Accounts for the rule that Ace can be 1 or 11, whichever is more favourable
        n_aces = len([card for card in self._hand if card.is_ace()])
        sum_non_aces = sum([card.value for card in self._hand if not card.is_ace()])
        if n_aces == 0:
            return sum_non_aces
        possible_sum_aces = [sum(res) for res in product([1, 11], repeat=n_aces)]
        possible_scores = [sum_non_aces + sum_aces for sum_aces in possible_sum_aces]
        filtered_scores = [score for score in possible_scores if score <= 21]
        if filtered_scores == []:  # All exceed 21
            return min(possible_scores)
        return max(filtered_scores)

    def hand_is_blackjack(self) -> bool:
        # Blackjack occurs when:
        # 1. 2 cards on the hand AND
        # 2. Either of:
        #   (a) Both cards ACE OR
        #   (b) One card ACE, One card value 10 (KING, QUEEN, JACK or TEN)
        if len(self._hand) != 2:
            return False
        if (self._hand[0].is_ace() and self._hand[1].is_ace()) or \
            (self._hand[0].is_ace() and self._hand[1].value == 10) or \
            (self._hand[0].value == 10 and self._hand[1].is_ace()):
            return True
        return False

    # Points refer to the points earned over multiple games
    #   No public setter access, can only add or minus points
    @property
    def points(self) -> int:
        return self._points

    def get_public_status(self) -> str:
        if self._hand == []:
            return f"{self.name}: Empty hand"
        assert len(self._hand) >= 2, "Hand cannot have only one Card"
        return f"{self.name}: {str(self._hand[0])} and {len(self._hand) - 1} other card(s)"

    def get_private_status(self) -> str:
        if self._hand == []:
            return f"{self.name}: Empty hand"
        assert len(self._hand) >= 2, "Hand cannot have only one Card"
        output = f"Score of current hand: {self.score}\n"
        output += "Your current hand: \n"
        for card in self._hand:
            output += f" - {str(card)}\n"
        return output

    def add_to_hand(self, new_card: Card) -> int:
        self._hand.append(new_card)
        return self.score

    # Reset happens when a new deck is instantiated, old cards can be discarded
    # 2 new cards are issued at the start of the round
    def reset_hand(self, card_1: Card, card_2: Card) -> None:
        self._hand = [card_1, card_2]

    def add_points(self, to_add: int) -> None:
        assert to_add > 0, "to_add must be a positive integer"
        self._points += to_add

    def minus_points(self, to_minus: int) -> None:
        assert to_minus > 0, "to_add must be a positive integer"
        self._points -= to_minus
        # _points can go to negative and we are allowing that
