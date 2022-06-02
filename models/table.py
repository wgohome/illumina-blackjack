import time

from models.deck import Deck
from models.participant import Participant
from utils.choice_picker import ChoicePicker
from utils.helpers import (
    clear_screen,
)
from utils.registration_asker import RegistrationAsker


class Table:
    """
    A Table holds the game, with a deck, a dealer and at least one player
    """
    def __init__(
        self,
        dealer: Participant | None = None,
        players: list[Participant] | None = None
    ):
        self._round: int = 0
        self._deck: Deck = Deck()
        if dealer is None or players is None:
            dealer, players = RegistrationAsker.call()
        self._dealer: Participant = dealer
        self._players: list[Participant] = players

    @property
    def participants(self) -> list[Participant]:
        return [self._dealer, *self._players]

    @property
    def round(self) -> int:
        return self._round

    def run_a_round(self) -> None:
        self._round += 1
        self._deck = Deck()  # Reset deck
        print("\nShuffling the decks ...")
        time.sleep(1)
        print(f"{self._dealer.name} is dealing out fresh cards ...")
        time.sleep(1)
        for participant in self.participants:
            _ = participant.reset_hand(self._deck.hit(), self._deck.hit())
        self._print_round_status()
        clear_screen()
        for player in self._players:
            _ = input(f"Pass control to player {player.name}. Press enter once ready. \n")
            self._print_round_status()
            self._run_player_turn(player)
        _ = input(f"Pass control to dealer {self._dealer.name}. Press enter once ready. \n")
        self._print_round_status()
        self._run_dealer_turn()

    def _print_round_status(self) -> None:
        print(f"CURRENT STATUS FOR ROUND {self._round}")
        for participant in self.participants:
            print(participant.get_public_status())
        print()

    def _run_player_turn(self, player: Participant) -> None:
        print(f"Player {player.name}'s turn")
        print(player.get_private_status())
        if player.hand.is_blackjack():
            self._handle_blackjack_case(player)
            self._deck.send_to_discard(*player.hand.drop())
            _ = input(f"End of {player.name}'s turn. Press enter to clear screen.")
            clear_screen()
            return None  # Done with turn if hits blackjack
        while True:
            choice = self._deck_hitter(player)
            if choice == 0:
                break  # points will be handled during dealer's turn
            new_score = player.hand.add(self._deck.hit())
            print()
            print(player.get_private_status())
            if new_score > 21:
                self._handle_exceed_21(player)
                self._deck.send_to_discard(*player.hand.drop())
                break
        _ = input(f"End of {player.name}'s turn. Press enter to clear screen.")
        clear_screen()

    def _run_dealer_turn(self) -> None:
        dealer = self._dealer
        surviving_players = [player for player in self._players if not player.hand.is_empty()]
        print(f"Dealer {dealer.name}'s turn")
        print(dealer.get_private_status())
        if dealer.hand.is_blackjack():
            self._handle_blackjack_case(dealer, role="dealer")
            self._deck.send_to_discard(*dealer.hand.drop())
            _ = input(f"End of this round. Press enter to clear screen.")
            clear_screen()
            return None
        while True:
            choice = self._deck_hitter(dealer)
            if choice == 0:
                break  # points will be handled during dealer's turn
            new_score = dealer.hand.add(self._deck.hit())
            print()
            print(dealer.get_private_status())
            if new_score > 21:
                self._handle_exceed_21_for_dealer(surviving_players)
                _ = input(f"End of this round. Press enter to clear screen.")
                clear_screen()
                return None
        # Face off with surviving players
        print("\nSurviving players are dealing with the dealer ...")
        for player in surviving_players:
            self._dealer_duel_against(player)
        self._deck.send_to_discard(*dealer.hand.drop())
        _ = input(f"End of this round. Press enter to clear screen.")
        clear_screen()

    def _handle_blackjack_case(
        self,
        participant: Participant,
        role: str = "player"
    ) -> None:
        # Assumes participant has been validated to hit blackjack
        participant.add_points(15)
        print(f"Congratulations {participant.name}! \nYou have earned 15 points from scoring a blackjack.")
        if role == "dealer":
            print("Remaining participants will not earn any more points this round")
        _ = input(f"End of your turn. Press enter to clear screen for the next player.")
        clear_screen()

    def _handle_exceed_21(self, participant: Participant) -> None:
        participant.minus_points(10)
        print("You have exceeded score of 21 on your hands. You will lose 10 points this round")

    def _handle_exceed_21_for_dealer(self, surviving_players: list[Participant]) -> None:
        print("You have exceeded score of 21 on your hands.")
        for player in surviving_players:
            print(f"As a dealer, you lose 10 points to {player.name}, who has a hand of {player.hand.score}")
            self._dealer.minus_points(10)
            # player don't earn points here
            self._deck.send_to_discard(*player.hand.drop())
        self._deck.send_to_discard(*self._dealer.hand.drop())

    def _dealer_duel_against(self, player: Participant) -> None:
        dealer = self._dealer
        dealer_score: int = dealer.hand.score
        player_score: int = player.hand.score
        assert 16 < dealer_score <= 21, f"Dealer ({dealer.name}) score out of range (16,21]"
        assert 16 < player_score <= 21, f"Player ({player.name}) score out of range (16,21]"
        if dealer_score > player_score:
            dealer.add_points(10)
            print(f"Dealer {dealer.name} ({dealer.hand.score}) won player {player.name} ({player.hand.score}) and earned 10 points.")
        elif dealer_score < player_score:
            player.add_points(10)
            print(f"Player {player.name} ({player.hand.score}) won dealer {dealer.name} ({dealer.hand.score}) and earned 10 points.")
        else:
            print(f"It is a push. Both dealer ({dealer.name}) and player ({player.name}) have the same score and no points are awarded.")
        self._deck.send_to_discard(*player.hand.drop())

    def _deck_hitter(self, participant: Participant) -> int:
        picker = ChoicePicker(
            prompt="Do you want to take another hit?",
            options=[
                (1, "Yes, hit the deck for another card"),
                (0, "No, that's enough for me"),
            ]
        )
        picker_2 = ChoicePicker(
            prompt="Do you want to take another hit?",
            options=[
                (1, "Yes, I have to take another hit - My hand hasn't exceeded 16"),
            ]
        )
        if participant.hand.score > 16:
            return picker.run()
        # Else, participant have no choice,
        # Prompt just to acknowledge that they are hitting the deck
        return picker_2.run()
