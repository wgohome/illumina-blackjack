class ChoicePicker:
    def __init__(self, prompt: str, options: list[tuple[int, str]]):
        self._prompt = prompt
        self._options = options

    def run(self) -> int:
        print(self._prompt)
        for index, description in self._options:
            print(f"{index}. {description}")
        choice = int(input("Enter your choice number: "))
        while choice not in [i for i, d in self._options]:
            print(f"{choice} is not a valid option number.")
            choice = int(input("Enter your choice number again: "))
        return choice
