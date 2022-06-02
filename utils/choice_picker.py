class ChoicePicker:
    def __init__(self, prompt: str, options: list[tuple[int, str]]):
        self._prompt = prompt
        self._options = options

    def run(self) -> int:
        print(self._prompt)
        for index, description in self._options:
            print(f"{index}. {description}")
        choice = self._get_numeric_choice()
        while choice not in [i for i, _ in self._options]:
            print(f"{choice} is not a valid option number.")
            choice = self._get_numeric_choice()
        return choice

    def _get_numeric_choice(self) -> int:
        choice_str = input("Enter your choice number: ")
        return int(choice_str) if choice_str.isdigit() else -100000
