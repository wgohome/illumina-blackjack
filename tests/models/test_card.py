import random
from models.card import Card, Rank, Suit


def test_face_cards_value_10():
    for rank in [Rank.JACK, Rank.QUEEN, Rank.KING]:
        card = Card(rank, random.choice([*Suit]))
        assert card.value == 10


def test_is_ace():
    card = Card(Rank.ACE, random.choice([*Suit]))
    assert card.is_ace() == True


def test_is_not_ace():
    rank = random.choice([rank for rank in Rank if rank is not Rank.ACE])
    card = Card(rank, random.choice([*Suit]))
    assert card.is_ace() == False
