from models.card import Card, Rank, Suit
from models.participant import Participant


def test_participant_add_points():
    participant = Participant()
    assert participant.points == 0

    participant.add_points(1)
    participant.add_points(33)
    assert participant.points == 34


def test_participant_minus_points():
    participant = Participant()
    assert participant.points == 0

    participant.minus_points(9)
    assert participant.points == -9


def test_participant_reset_hand():
    participant = Participant()
    participant._hand._cards = [
        Card(Rank.THREE, Suit.HEARTS),
        Card(Rank.FIVE, Suit.SPADES),
    ]
    new_cards = [Card(Rank.ACE, Suit.DIAMONDS), Card(Rank.KING, Suit.CLUBS)]
    _ = participant.reset_hand(*new_cards)
    assert participant._hand._cards == new_cards
