import random as rd

from statistics import Statistics


MAX_PLAYABLE_CARDS = 3


# AI
# save brain
# train
# input : cards (max being deck), bet, pile size, last play size, prev & next plyr hand size


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.win = False

        self.stats = Statistics()

    def __str__(self):
        return f"{self.name} [{len(self.hand)} cards]"

    def do(self):
        return f"\t{self.name}: "

    def get_stats(self):
        return str(self.stats)

    def launch(self):
        bet = self.get_bet()
        print(f"betting on {bet.value()}")

        cards = self.play(True)
        return bet, cards

    def play(self, launch=False):
        res = []
        min_amount = 1 if launch else 0
        for _ in range(rd.randint(min_amount, min(len(self.hand), MAX_PLAYABLE_CARDS))):
            pos = rd.randint(0, len(self.hand)-1)
            c = self.hand.pop(pos)
            res += [c]

        if not res:
            print(f"{self.do()} Calling for liar!")
        else:
            print(f"{self.do()}", [str(c) for c in res])

        return res

    def get_bet(self):
        b = rd.choice(self.hand)
        return b

    def remove_same_cards(self):
        self.hand.sort(key=lambda c: c.rank)

        # to_discard
        td = {}
        for c in self.hand:
            td[c.rank] = td.get(c.rank, 0) + 1

        td = {k: v for k, v in td.items() if v > 3}
        if td:
            print(f"\t{self.do()} discards following cards: {list(td.keys())}")

            new_hand = [c for c in self.hand if c.rank not in td.keys()]
            self.hand = new_hand

    def has_win(self):
        if not self.win and not self.hand:
            print(self.name, "finished the game !")
            self.win = True

    # ----- Stats -----

    def update_stats(self, lied):
        self.stats.lied += [lied]

    def is_accused(self, verdict):
        if verdict:
            print(f"\tLast player ({self.name}) lied!")
        self.stats.accused += [verdict]

    def is_accusing(self, verdict):
        if not verdict:
            print(f"\t{self.name} was wrong!")

        self.stats.accusations += [verdict]
