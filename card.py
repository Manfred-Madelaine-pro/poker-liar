HIGH_RANKS = ["J", "Q", "K"]
SUITS = ["♤", "♡", "♢", "♧"]


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        r = self.value()
        s = SUITS[self.suit]
        return f"{r}-{s}"

    def value(self):
        r = self.rank
        r = r if r <= 10 else HIGH_RANKS[r % 10 - 1]
        return r


def main():
    cards = [Card(c, 0) for c in range(1, 14)]
    [print(c, end=", ") for c in cards]


if __name__ == "__main__":
    main()
