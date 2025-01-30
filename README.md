# MENACE - Machine Learning Naughts and Crosses bot!

## How it works:
The idea is based off Matt Parkers youtube video "MENACE: The pile of matchboxes that can learn". 
</br></br>Basically the bot stores all possible boards and the positions that can be the next move as a hashmap where the "key" is the board and the "value" is a list of all the positions of the next moves.
Then, as the game is played, the bot will backtrack through all the moves it made. If it won it will reinforce those moves by replicating that next move three times in the record of the previous board.
If it lost, it will take out one instance of the moves from their record. And if it drew, it will replicate that move once.

The bot uses separate hashmaps based on whether it is the first or second player (stored in boardsFirst.bin and boardsSecond.bin respectively)

## Restarting the bot:
In order to allow the bot to have a starting place for what all the boards were and what thier possible moves were, I wrote findBoards.py

It goes through every possible board, in a tree like fassion, adding it to a hashmap if;
  -  It is a valid board (i.e. there is equal Xs and Os or one more X in the case X just moved)
  -  It is not already in the hashmap (I've also cut out all repititions of rotations, or flips)
  -   It is not after the board is already won

I then use pickle to dump the hashmap directly to a binary file

## Training the bot:
I trained the bot by playing it against a random move generator 20,000 times both in the case it was going first and the case it was going second.

My "pre-trained" hashmaps are stored in boardsFirst.bin and boardsSecond.bin
