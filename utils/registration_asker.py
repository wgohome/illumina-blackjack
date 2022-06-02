from models.participant import Participant


class RegistrationAsker:
    def __init__(self):
        self._n: int = self._ask_for_n_participants()
        self._dealer: Participant = self._create_dealer()
        self._players: list[Participant] = self._create_players()

    @classmethod
    def call(cls) -> tuple[Participant, list[Participant]]:
        registration_asker = cls()
        return registration_asker.dealer, registration_asker.players

    @property
    def dealer(self) -> Participant:
        return self._dealer

    @property
    def players(self) -> list[Participant]:
        return self._players

    def _create_dealer(self) -> Participant:
        return Participant(name=self._ask_for_name("dealer"))

    def _create_players(self) -> list[Participant]:
        return [
            Participant(name=self._ask_for_name("player"))
            for _ in range(self._n - 1)
        ]

    def _ask_for_n_participants(self) -> int:
        n: int = int(input("How many players? (including dealer)"))
        while n < 2:
            print("At least two players are needed for Blackjack ...")
            n = int(input("How many players? (including dealer)"))
        return n

    def _ask_for_name(self, role: str = "player") -> str:
        name: str = input(f"Enter name of the {role}").strip()
        while not name:
            print("Please enter a name that is not blank")
            name = input(f"Enter name of the {role}").strip()
        return name
