from models.table import Table
from utils.choice_picker import ChoicePicker


should_end_game = ChoicePicker(
        prompt="Do you want to continue with the next round of the game?",
        options=[
            (1, "Hell yes, let's roll into the next round!"),
            (0, "We are done - end the game now ..."),
        ]
    )

def main() -> None:
    table = Table()
    while True:
        print_participant_status(table)
        table.run_a_round()
        if should_end_game.run() == 0:
            break
    print_participant_status(table)


def print_participant_status(table: Table) -> None:
    print("Here is how the game went \n")
    print(f"Total of {table.round} rounds have been played.")
    print("Points so far:")
    for participant in table.participants:
        print(participant.get_points_status())


if __name__ == "__main__":
    main()
