from enum import Enum


class Rank(Enum):
    # ACES can take value of 1 (default) or 11 in some cases
    #   Should be handled when calculating player's hand
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    # Face (picture) cards share the same value of 10,
    #   which will be reflected when calling value() on the Card
    JACK = 11
    QUEEN = 12
    KING = 13


class Suit(Enum):
    SPADES = "Spades"
    HEARTS = "Hearts"
    CLUBS = "Clubs"
    DIAMONDS = "Diamonds"


class Card:
    def __init__(self, rank: Rank, suit: Suit) -> None:
        self._rank: Rank = rank
        self._suit: Suit = suit

    def __repr__(self) -> str:
        return f"<Card({self._suit}, {self._rank})>"

    def __str__(self) -> str:
        return f"{self._rank.name.capitalize()} of {self._suit.value}"

    def __eq__(self, other: "Card") -> bool:
        return (self._rank, self._suit) == (other._rank, other._suit)

    @property
    def value(self) -> int:
        # Jack, Queen, King each have true value of 10,
        # but were represented otherwise in the enum for unique enum values
        return min(self._rank.value, 10)

    @property
    def name(self) -> str:
        return self.__str__()

    def is_ace(self) -> bool:
        return self._rank == Rank.ACE
