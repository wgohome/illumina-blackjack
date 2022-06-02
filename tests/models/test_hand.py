from models.card import Card, Rank, Suit
from models.hand import Hand


def test_can_add_one_card():
    hand = Hand()
    hand.add(Card(Rank.THREE, Suit.CLUBS))
    assert len(hand._cards) == 1
    assert hand._cards[0] == Card(Rank.THREE, Suit.CLUBS)


def test_two_ace_is_blackjack():
    hand = Hand()
    hand.add(Card(Rank.ACE, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS))
    assert hand.is_blackjack() is True


def test_one_ace_is_blackjack():
    hand = Hand()
    hand.add(Card(Rank.ACE, Suit.CLUBS), Card(Rank.TEN, Suit.HEARTS))
    assert hand.is_blackjack() is True
    hand = Hand()
    hand.add(Card(Rank.KING, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS))
    assert hand.is_blackjack() is True


def test_three_ace_not_blackjack():
    hand = Hand()
    hand.add(
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.HEARTS)
    )
    assert hand.is_blackjack() is False


def test_other_21_not_blackjack():
    hand = Hand()
    hand.add(
        Card(Rank.SEVEN, Suit.CLUBS),
        Card(Rank.SIX, Suit.HEARTS),
        Card(Rank.EIGHT, Suit.SPADES)
    )
    assert hand.is_blackjack() is False


def test_score_correct():
    hand = Hand()
    hand.add(
        Card(Rank.FIVE, Suit.SPADES),
        Card(Rank.THREE, Suit.DIAMONDS),
    )
    assert hand.score == 8


def test_score_ace_as_11():
    hand = Hand()
    hand.add(
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.THREE, Suit.DIAMONDS),
    )
    assert hand.score == 14  # instead of 4


def test_score_ace_as_1():
    hand = Hand()
    hand.add(
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.FIVE, Suit.DIAMONDS),
        Card(Rank.NINE, Suit.DIAMONDS),
    )
    assert hand.score == 15  # instead of 25
