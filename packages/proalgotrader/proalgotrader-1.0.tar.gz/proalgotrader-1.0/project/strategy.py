class Strategy:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def calculate(self) -> int:
        return self.x + self.y
