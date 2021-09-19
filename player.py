import random as rd


MAX_PLAYABLE_CARDS = 3


class Stats:
    def __init__(self):
        self.lies = 0
        self.truths = 0

        self.liar_calls = 0
        self.good_calls = 0
        self.missed_calls = 0

        self.spotted = 0
        self.wrongfully_accused = 0

        self.worst_loss = 0
        self.best_escape = 0
        self.total_cards_exchanged = 0

# AI
# save brain
# train
# input : cards (max being deck), bet, pile size, last play size, prev & next plyr hand size


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.win = False

        self.stats = Stats()

    def __str__(self):
        return f"{self.name} [{len(self.hand)} cards]"

    def do(self):
        return f"\t{self.name}: "

    def launch(self):
        bet = self.get_bet()
        print(f"betting on {bet.val()}")

        cards = self.play(bet, True)
        return bet, cards

    def play(self, bet, launch=False):
        res = []
        min_amount = 1 if launch else 0
        for _ in range(rd.randint(min_amount, min(len(self.hand), MAX_PLAYABLE_CARDS))):
            c = self.hand.pop()
            res += [c]

        if not res:
            print(f"{self.do()} Calling for liar!")
        else:
            print(f"{self.do()}", [str(c) for c in res])

        self.update_stats(bet, res)
        return res

    def get_bet(self):
        b = rd.choice(self.hand)
        return b

    def remove_same_cards(self):
        self.hand.sort(key=lambda c: c.value)

        # to_discard
        td = {}
        for c in self.hand:
            td[c.value] = td.get(c.value, 0) + 1

        td = {k: v for k, v in td.items() if v > 3}
        if td:
            print(f"\t{self.do()} discards following cards: {list(td.keys())}")

            new_hand = [c for c in self.hand if c.value not in td.keys()]
            self.hand = new_hand

    # ----- Stats -----
    def update_stats(self, bet, action):
        if not action:
            print("denouncing!")
            self.stats.liar_calls += 1
        elif is_lying(bet, action):
            self.stats.lies += 1
        else:
            self.stats.truths += 1

    def is_spotted(self):
        self.stats.spotted += 1

    def is_innocent(self):
        self.stats.wrongfully_accused += 1

    def was_right(self):
        self.stats.good_calls += 1

    def was_wrong(self):
        self.stats.missed_calls += 1


def is_lying(bet, cards_played):
    for c in cards_played:
        if bet.val() != c.val():
            return True
    return False
