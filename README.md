# poker-liar

create venv
install pytorch
Allow player picker 
If provided before the game
Create missing p then shuffle order 

Ai
Change random algo
Use ML lib (torch)
Set hands, starter? And train
Bet choice will be done randomly at first 

In
Bet 
52 cards per rank and color with true false
Pile amount
Last played amount 
Next p cards amount 
Prev p cards amount 

Out
Amount of Cards to play? 
If amount == 0: call liar
Proba per card (52)
If Proba > x play until amount is reached 


Save stats (win, loss, ...?) 
Train on full or single game N times 
Filter winners (based on score?) 
Reproduce
Train child's again
Display win ratio over generations

Trainning mode (reproduction) 
Use mode
   See one turn, one game, the full game
Reuse players? 

1- create AI
Use lib (venv + install pytorch Linux) 
Populate input
Run ML
Display output
Use output for decision
Save & load brain? 

2- integrate AI in one game
Check outcome 

3- run full game

4- create training mode
Display generation stats (win ratio, dénonciations...) 
Save brain conf
Load brain 

Save games in file as Json (Game) 
Hands
Starter
Bet
Plays
Outcome

Read game? Opt


Perf study & improvements 
