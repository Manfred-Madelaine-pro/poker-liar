import random as rd

# choose users
# default AI

# pick amount of players
PLAYERS_AMOUNT = 3
MAX_AMOUNT = 3
DELAY = 10


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


# clean
# 		  
# AI
# save brain
# train
# input : cards (max being deck), bet, pile size, last play size, prev & next plyr hand size

# Stats: par game, globale, par joueur (et si plus de joueurs?)

# Game: next player, previous player

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.win = False

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
        for _ in range(rd.randint(min_amount, min(len(self.hand), MAX_AMOUNT))):
            c = self.hand.pop()
            res += [c]

        if not res:
            print(f"{self.do()} Calling for liar! ")
        else:
            print(f"{self.do()}", [str(c) for c in res])

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


def start(players_amount):
    players = [Player("P" + str(i)) for i in range(players_amount)]
    cards = [Card(c, n) for c in range(1, 14) for n in range(4)]
    deal(cards, players)

    starter_id = 0 # TODO random ?
    manche = 1
    while len(players) > 1:
        print(f"\n---------- Manche #{manche} ----------")
        manche += 1
        starter_id = start_trick(players, starter_id)

        print("\nStatus:")
        [print(p) for p in players]
        print()
        players = [p for p in players if not p.win]

        if len(players) == 1:
            print(players[0], "lost the game!")
            return 0

        starter_id = starter_id % len(players)


def deal(cards, players):
    rd.shuffle(cards)

    for i, c in enumerate(cards):
        p = players[i % len(players)]
        p.hand += [c]


def start_trick(players, starter_id):
    t = 0
    pile = []
    last_played = []
    curr = starter_id

    [p.remove_same_cards() for p in players]

    round = 0
    print(f"- Round {t // len(players)}:", end=" ")
    bet, cards = players[curr].launch()
    pile, last_played, t = next_turn(pile, last_played, cards, t)

    while "playing":
        next_id = next_player(players, curr)

        if next_id is None:
            print("End of game")
            return curr

        curr = next_id

        if round != t // len(players):
            print("- Round " + str(t // len(players)))
            round += 1

        cards = players[curr].play(bet)
        liar_id = handle_liar(players, curr=curr)

        if len(cards) == 0:
            break

        pile, last_played, t = next_turn(pile, last_played, cards, t)
        is_winner(players[liar_id])

    liar_id = check_liar(bet, last_played, liar_id, curr, players)

    # punish liar
    players[liar_id].hand += last_played + pile
    print(f"He gets +{len(pile) + len(last_played)} cards!")

    print(f"\nSummary:\n- Bet: {bet.val()}\n- Last played: {[str(c) for c in last_played]}\n- Pile: {[str(c) for c in pile]}\n- Liar id: {liar_id}")

    rd.shuffle(players[liar_id].hand)

    return curr if curr != liar_id else next_player(players, curr)


def next_turn(pile, last_played, cards, turn):
    pile += last_played
    last_played = cards
    return pile, last_played, turn + 1


def next_player(players, curr):
    id = (curr+1) % len(players)
    if players[id].win:
        print("next player!")
        id = next_player(players, id)
    return id if id != curr else None


def handle_liar(players, curr=0):
    id = curr - 1
    if id < 0:
        id = len(players) - 1
    if players[id].win:
        id = handle_liar(players, curr=id)
    return id


def check_liar(bet, last_played, liar_id, curr, players):
    print("\nChecking who is the liar:")
    for c in last_played:
        if bet.val() != c.val():
            print(f"\tLast player ({players[liar_id].name}) lied! ", end="")
            return liar_id
    print(f"\t{players[curr].name} was wrong! ", end="")
    is_winner(players[liar_id])
    return curr


def is_winner(player):
    # print(player, f"win: {player.win}")
    if not player.win and not player.hand:
        print(player.name, "finished the game !")
        player.win = True


def poker_liar():
    print("\t-- Poker Liar -- \n")
    start(PLAYERS_AMOUNT)


poker_liar()
