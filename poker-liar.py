import random as rd

from card import Card
from player import Player


PLAYERS_AMOUNT = 3
NO_PLAYERS_LEFT = "No players left"


# Stats: par game, globale, par joueur (et si plus de joueurs?)


class PokerLiar:
    def __init__(self, players_amount):
        self.players = [Player("P" + str(i)) for i in range(players_amount)]
        cards = [Card(rank, suit) for rank in range(1, 14) for suit in range(4)]
        deal(cards, self.players)

        self.table = [p for p in self.players]

        self.game = 0
        self.current = rd.randint(0, len(self.players))

    def start(self):
        self.game = 1
        while len(self.players) > 1:
            print(f"\n---------- Game #{self.game} ----------")
            self.game += 1

            self.rounds()

            print("\nStatus:")
            [print(p) for p in self.players]
            [print(p.get_stats()) for p in self.players]
            [print(p.stats.stats()) for p in self.players]
            print()

            self.filter_winners()

            if len(self.players) == 1:
                print(self.players[0], "lost the game!")
                return 0

    def filter_winners(self):
        self.players = [p for p in self.players if not p.win]
        self.current = self.current % len(self.players)

    def rounds(self):
        pile = []

        [p.remove_same_cards() for p in self.players]

        bet, last_played = self.players[self.current].launch()

        end, liar_id = self.plays(bet, pile, last_played)

        if end:
            return 0

        self.liar_judgment(bet, last_played, liar_id, pile)

    def plays(self, bet, pile, last_played):
        cards = last_played
        last_played = []
        while "playing":
            pile, last_played = next_turn(pile, last_played, cards)
            next_id = self.next_player()

            if next_id == NO_PLAYERS_LEFT:
                print("End of game")
                return "End", None

            self.current = next_id

            cards = self.players[self.current].play()
            self.players[self.current].update_stats(is_lying(bet, cards))

            liar_id = self.previous_player()

            if len(cards) == 0:
                break

            self.players[liar_id].has_win()

        return not "End", liar_id

    def liar_judgment(self, bet, last_played, liar_id, pile):
        print("\nChecking who is the liar:")

        verdict = is_lying(bet, last_played)
        self.players[liar_id].is_accused(verdict)
        self.players[self.current].is_accusing(verdict)

        if verdict:
            self.players[liar_id].hand += last_played + pile
        else:
            self.players[liar_id].has_win()
            self.current = self.next_player()

        print(f"\tHe gets +{len(pile) + len(last_played)} cards!")
        print(
            f"\nSummary:\n- Bet: {bet.value()}\n- Last played: {[str(c) for c in last_played]}\n- Pile: {[str(c) for c in pile]}\n- Liar id: {liar_id}"
        )

    def next_player(self, opt=None):
        c = self.current if opt is None else opt
        id = (c + 1) % len(self.players)
        if self.players[id].win:
            id = self.next_player(opt=id)
        return id if id != self.current else NO_PLAYERS_LEFT

    def previous_player(self, curr=None):
        c = self.current if curr is None else curr
        id = c - 1 if c - 1 >= 0 else len(self.players) - 1
        if self.players[id].win:
            id = self.previous_player(curr=id)
        return id


def is_lying(bet, cards_played):
    for c in cards_played:
        if bet.value() != c.value():
            return True
    return False


# --- Utils


def deal(cards, players):
    rd.shuffle(cards)

    for i, c in enumerate(cards):
        p = players[i % len(players)]
        p.hand += [c]


def next_turn(pile, last_played, cards):
    pile += last_played
    last_played = cards
    return pile, last_played


# --- Main


def main():
    print("\t-- Poker Liar -- \n")
    pl = PokerLiar(PLAYERS_AMOUNT)
    pl.start()


if __name__ == "__main__":
    main()
