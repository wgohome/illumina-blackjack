# from itertools import product

from models.card import Card
from models.hand import Hand


class Participant:
    """
    Participant refer to either the dealer or the remaining players
    """
    counter: int = 0

    def __init__(self, name: str | None = None):
        Participant.counter += 1
        self._index: int = Participant.counter
        self._name: str = name or f"Participant no. {self._index}"
        self._points: int = 0  # points over multiple games
        self._hand: Hand = Hand()

    def __repr__(self):
        return f"<Participant(name={self.name}), index: {self._index}, points: {self.points}>"

    # Read only access, but can chain Hand instance methods on this property
    @property
    def hand(self):
        return self._hand

    @property
    def name(self):
        return self._name

    # Points refer to the points earned over multiple games
    #   No public setter access, can only add or minus points
    @property
    def points(self) -> int:
        return self._points

    def get_public_status(self) -> str:
        if self._hand == []:
            return f"{self.name}: Empty hand"
        assert self._hand.size >= 2, "Hand cannot have only one Card"
        return f" - {self.name}: {str(self._hand.cards[0])} and {self._hand.size - 1} other card(s)"

    def get_private_status(self) -> str:
        if self._hand.size == []:
            return f"{self.name}: Empty hand"
        assert self._hand.size >= 2, "Hand cannot have only one Card"
        output = f"Score of current hand: {self.hand.score}\n"
        output += "Your current hand: \n"
        for card in self._hand.cards:
            output += f" - {str(card)}\n"
        return output

    def reset_hand(self, card_1: Card, card_2: Card) -> list[Card]:
        dropped_cards = self._hand.drop()
        _ = self._hand.add(card_1, card_2)
        return dropped_cards

    def add_points(self, to_add: int) -> None:
        assert to_add > 0, "to_add must be a positive integer"
        self._points += to_add

    def minus_points(self, to_minus: int) -> None:
        assert to_minus > 0, "to_add must be a positive integer"
        self._points -= to_minus
        # _points can go to negative and we are allowing that
