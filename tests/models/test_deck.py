from models.deck import Deck


def test_new_deck_has_52_cards():
    deck = Deck()
    assert deck.get_size() == 52


def test_deck_no_duplicates():
    deck = Deck()
    n_unique_cards = len(set([repr(card) for card in deck._cards]))
    assert deck.get_size() == n_unique_cards
