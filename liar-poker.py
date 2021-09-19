
import random as rd
import time

# choose users
# default AI

# pick amount of players
PLAYERS_AMOUNT = 3
max_amount = 3
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
		v = v if v <= 10 else ["J", "Q", "K"][v%10-1]
		return v
		
		 
#clean 
# 		  
# AI
# save brain
# train
# input : cards (max being deck), bet, pile size, last play size, prev & next plyr hand size

  
class Player:
		def __init__(self, name):
			self.name = name
			self.hand = []
			self.win = False
			
		def __str__(self):
			return f"{self.name} [{len(self.hand)} cards]"
		
		def do(self):
			return f"\t{self.name}: "
		#
		def launch(self):
			bet = self.get_bet()
			print(f"betting on {bet.val()}")
			
			cards = self.play(bet, True)
			return bet, cards
			
		#
		def play(self, bet, launch=False):
			res = [] 
			min_amount = 1 if launch else 0
			for _ in range(rd.randint(min_amount, min(len(self.hand), max_amount))):
				c = self.hand.pop()
				res += [c]
				
			if not res:
				print (f"{self.do()} Calling for liar! ") 
			else:
				print(f"{self.do()}", [str(c) for c in res])
			 
			return res
			
		#
		def get_bet(self):
			b = rd.choice(self.hand)
			return b
	
		#
		def remove_same_cards(self):
			self.hand.sort(key=lambda c: c.value)
			count = 0
			v = False
			
			# to_discard
			td = {}
			for c in self.hand:
				td[c.value] = td.get(c.value, 0) + 1
			
			td = {k:v for k,v in td.items() if v > 3}
			if td:
				print(f"\t{self.do()} discards following cards: {list(td.keys())}")
					#{list(td.keys()).join(', ')}")
			
				new_hand = [c for c in self.hand if c.value not in td.keys()]
				self.hand = new_hand

# - - - - - - - 

		
# start game
def start(players_amount):
	players = create_players(players_amount)
	
	cards = create_cards()
	deal(cards, players)
	
	# pick starter heart queen
	starter_id = 0
	manche = 1
	# start turn clockwise 
	while len(players) > 1:
		print(f"\n---------- Manche #{manche} ----------")
		manche += 1
		starter_id = start_trick(players, starter_id)
		
		print("\nStatus:")
		[print(p) for p in players]
		time.sleep(DELAY)
		print()
		players = [p for p in players if not p.win]
		starter_id = starter_id%len(players)
		
	if len(players) == 1:
		print(players[0], "lost the game!")


def create_players(players_amount):
	return [Player("P" + str(i)) for i in range(players_amount) ]


def create_cards(): 
	return [Card(c, n) for c in range(1,14) for n in range(4)] 
	
	
def deal(cards, players):
	rd.shuffle(cards) 
	
	for i, c in enumerate(cards):
		p = players[i%len(players)]
	
		p.hand += [c]
	
	
def start_trick(players, starter_id):
	t=0
	liar_id = False
	pile = []
	last_played = []
	
	# clean hands
	[p.remove_same_cards() for p in players]
	
	round = 0
	print(f"- Round {t//len(players)}:", end=" ")
	bet, cards = players[starter_id].launch()
	pile, last_played, t = next_turn(pile, last_played, cards, t)
	
	while "playing":
		curr = next_player(players, starter_id, t)
		
		if round != t//len(players):
			print("- Round " + str(t//len(players))) 
			round += 1
		
		cards = players[curr].play(bet) 	
		if len(cards) == 0:
			break
		
		liar_id = handle_liar(players, curr=curr)
		
		pile, last_played, t = next_turn(pile, last_played, cards, t)
		is_winner(players[liar_id])
		
	liar_id = check_liar(bet, last_played, liar_id, curr, players) 
	
	# punish liar
	players[liar_id].hand += last_played + pile
	print(f"He gets +{len(pile) + len(last_played)} cards!")
	
	print(f"\nSummary:\n- Bet: {bet.val()}\n- Last played: {[str(c) for c in last_played]}\n- Pile: {[str(c) for c in pile]}\n- Liar id: {liar_id}")
	
	rd.shuffle(players[liar_id].hand)
	
	return curr if curr != liar_id else next_player(players, starter_id, t)
	

def next_turn(pile, last_played, cards, turn):
		pile += last_played
		last_played = cards	
		return pile, last_played, turn +1	

	
def next_player(players, starter_id, t):
	id = (starter_id + t)%len(players)
	if players[id].win:
		id += 1
		print("next player!")
	return id


def handle_liar(players, curr=0):
	id = curr - 1
	if id < 0:
		id = len(players) - 1
	if players[id].win:
			id = handle_liar(players, curr=id) 
	return id 

def check_liar(bet, last_played, liar_id, curr, players):
	print("\nChecking who is the liar:")
	for c in last_played :
		if bet.val()!=c.val():
			print(f"\tLast player ({players[liar_id].name}) lied! ", end="")
			return liar_id
	print(f"\t{players[curr].name} was wrong! ", end="")
	return curr
			
		
def is_winner(player):
	#print(player, f"win: {player.win}")
	if not player.win and not player.hand :
			print(player.name, "finished the game !")
			player.win = True
 

def liar_poker():
	print("\t-- Liar's Poker -- \n")
	start(PLAYERS_AMOUNT)



liar_poker()