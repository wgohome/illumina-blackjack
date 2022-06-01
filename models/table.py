from models.deck import Deck
from models.participant import Participant
from utils.choice_picker import ChoicePicker
from utils.helpers import clear_screen


class Table:
    def __init__(self):
        self._round: int = 0
        self._deck: Deck = Deck()
        self._dealer: Participant
        self._players: list[Participant] = list()
        self._add_participants()

    def _add_participants(self) -> None:
        n = int(input("How many players? "))
        while n < 2:
            print("At least two players are needed for Blackjack ...")
            n = int(input("How many players?"))
        name = input("Enter name of dealer: ")
        self._dealer = Participant(name=name)
        for _ in range(n - 1):
            name = input("Enter name of player: ")
            self._players.append(Participant(name=name))

    @property
    def participants(self) -> list[Participant]:
        return [self._dealer, *self._players]

    def restart_game(self):
        self._round += 1
        self._deck = Deck()
        for participant in self.participants:
            participant.reset_hand(self._deck.hit(), self._deck.hit())
        self._get_status()
        for player in self._players:
            _ = input(f"Pass control to player {player.name}. Press enter once ready.")
            print()
            self._run_turn(player)
        # run dealer turn,
        # if not exploded, then compare against surviving players
        print("Dealer turn")
        self._run_dealer_turn()


    def _get_status(self) -> None:
        print(f"CURRENT STATUS FOR ROUND {self._round}")
        for participant in self.participants:
            print(participant.get_public_status())
        print()

    def _run_turn(self, participant: Participant) -> None:
        # if scored blackjack then just auto win 15 points
        if participant.hand_is_blackjack():
            print(participant.get_private_status())
            participant.add_points(15)
            # congratulate and skip to next person turn
            _ = input(f"Congratulations {participant.name}! You have earned 15 points from scoring a blackjack. End of your turn. Press enter to clear screen.")
            clear_screen()
            return None

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

        # ask to take hit until it lose or satistifed
        while participant.score <= 21:  # TODO max of 5 cards??
            print(participant.get_private_status())
            if participant.score > 16:
                choice = picker.run()
                # If 16 or less must take a card! (must be > 16)
                if choice == 0:
                    break
            else:
                _ = picker_2.run()  # player had no choice, just to acknowledge that they are hitting the deck
            new_score = participant.add_to_hand(self._deck.hit())
            print()
            print(participant.get_private_status())
            if new_score > 21:
                print("You have exceeded score of 21 on your hands. You will lose 10 points this round")
                participant.minus_points(10)
            # else will compare score with dealer to see who wins
        _ = input(f"End of {participant.name}'s turn. Press enter to clear screen.")
        clear_screen()

    def _run_dealer_turn(self) -> None:
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

        surviving_players = [player for player in self._players if player.score <= 21]

        # if scored blackjack then just auto win 15 points
        participant = self._dealer
        if participant.hand_is_blackjack():
            print(participant.get_private_status())
            participant.add_points(15)
            _ = input(f"Congratulations {participant.name}! You have earned 15 points from scoring a blackjack. The remaning surviving players will not earn any points.")
            clear_screen()
            return None

        import pdb; pdb.set_trace()

        while participant.score <= 21:
            print(participant.get_private_status())
            if participant.score > 16:
                choice = picker.run()
                if choice == 0:
                    break
            else:
                _ = picker_2.run()  # player had no choice, just to acknowledge that they are hitting the deck
            new_score = participant.add_to_hand(self._deck.hit())
            print()
            print(participant.get_private_status())

            if new_score > 21:
                print("You have exceeded score of 21 on your hands. You will lose 10 points per surviving players this round")
                participant.minus_points(10 * len(surviving_players))
                # surviving players will win 10 points
                for player in surviving_players:
                    player.add_points(10)
                    print(f"10 points added for {player.name}")

        if participant.score <= 21:
            for player in surviving_players:
                if player.score > participant.score:
                    player.add_points(10)
                    print(f"10 points added for player {player.name}")
                elif participant.score > player.score:
                    participant.add_points(10)
                    print(f"10 points added for dealer {participant.name}")
