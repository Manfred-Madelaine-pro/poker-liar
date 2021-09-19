import random as rd

from card import Card
from player import Player


PLAYERS_AMOUNT = 3


# Stats: par game, globale, par joueur (et si plus de joueurs?)

# Game: next player, previous player


def start(players_amount):
    players = [Player("P" + str(i)) for i in range(players_amount)]
    cards = [Card(rank, suit) for rank in range(1, 14) for suit in range(4)]
    deal(cards, players)

    starter_id = 0 # TODO random ?
    manche = 1
    while len(players) > 1:
        print(f"\n---------- Manche #{manche} ----------")
        manche += 1
        starter_id = rounds(players, starter_id)

        print("\nStatus:")
        [print(p) for p in players]
        [print(p.get_stats()) for p in players]
        [print(p.stats.stats()) for p in players]
        print()
        players = [p for p in players if not p.win]

        if len(players) == 1:
            print(players[0], "lost the game!")
            return 0

        starter_id = starter_id % len(players)


def rounds(players, starter_id):
    t = 0
    pile = []
    last_played = []
    curr = starter_id

    [p.remove_same_cards() for p in players]

    round = 0
    print(f"- Round {t // len(players)}:", end=" ")
    bet, cards = players[curr].launch()
    pile, last_played, t = next_turn(pile, last_played, cards, t)

    liar_id, curr, ended = play(players, curr, round, t, bet, pile, last_played)

    if ended:
        return curr

    liar_id = check_liar(bet, last_played, liar_id, curr, players)

    # punish liar
    players[liar_id].hand += last_played + pile
    print(f"He gets +{len(pile) + len(last_played)} cards!")

    print(f"\nSummary:\n- Bet: {bet.value()}\n- Last played: {[str(c) for c in last_played]}\n- Pile: {[str(c) for c in pile]}\n- Liar id: {liar_id}")

    rd.shuffle(players[liar_id].hand)

    return curr if curr != liar_id else next_player(players, curr)


def play(players, curr, round, t, bet, pile, last_played):
    while "playing":
        next_id = next_player(players, curr)

        if next_id is None:
            print("End of game")
            return None, curr, "Ended"

        curr = next_id

        if round != t // len(players):
            print("- Round {t // len(players)}")
            round += 1

        cards = players[curr].play()
        players[curr].update_stats(is_lying(bet, cards))
        liar_id = handle_liar(players, curr=curr)

        if len(cards) == 0:
            break

        pile, last_played, t = next_turn(pile, last_played, cards, t)
        is_winner(players[liar_id])

    return liar_id, curr, not "Ended"


def handle_liar(players, curr=0):
    id = curr - 1
    if id < 0:
        id = len(players) - 1
    if players[id].win:
        id = handle_liar(players, curr=id)
    return id


# --- Verifications


def check_liar(bet, last_played, liar_id, curr, players):
    print("\nChecking who is the liar:")
    if is_lying(bet, last_played):
        print(f"\tLast player ({players[liar_id].name}) lied! ", end="")
        players[liar_id].stats.accused += [True]
        players[curr].stats.accusations += [True]
        return liar_id
    print(f"\t{players[curr].name} was wrong! ", end="")
    players[liar_id].stats.accused += [False]
    players[curr].stats.accusations += [False]

    is_winner(players[liar_id])
    return curr


def is_lying(bet, cards_played):
    for c in cards_played:
        if bet.value() != c.value():
            return True
    return False


def is_winner(player):
    # print(player, f"win: {player.win}")
    if not player.win and not player.hand:
        print(player.name, "finished the game !")
        player.win = True


# --- Utils


def deal(cards, players):
    rd.shuffle(cards)

    for i, c in enumerate(cards):
        p = players[i % len(players)]
        p.hand += [c]


def next_turn(pile, last_played, cards, turn):
    pile += last_played
    last_played = cards
    return pile, last_played, turn + 1


def next_player(players, curr):
    id = (curr+1) % len(players)
    if players[id].win:
        id = next_player(players, id)
    return id if id != curr else None


# --- Main


def main():
    print("\t-- Poker Liar -- \n")
    start(PLAYERS_AMOUNT)


if __name__ == "__main__":
    main()
