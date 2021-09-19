
class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

    def __str__(self):
        v = self.val()
        c = ["♤", "♡", "♢", "♧"][self.color]
        return f"{v}-{c}"

    def val(self):
        v = self.value
        v = v if v <= 10 else ["J", "Q", "K"][v % 10 - 1]
        return v


def main():
    cards = [Card(c, 0) for c in range(1, 14)]
    [print(c, end=", ") for c in cards]


if __name__ == "__main__":
    main()
