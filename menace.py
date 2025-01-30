import random, sys, pickle

first = {}
second  = {}


def flipped(board):
    newBoard = ""
    for i in range(9):
        currPos = (((i//3)+1)*3) -((i%3)+1)
        if board[currPos] not in "012345678":
            newBoard += board[currPos]
        else:
            newBoard += str(i)
    return newBoard
    
def turned(board):
    newBoard=""
    for i in range(9):
        currPos = (2-(i%3))*3 + (i//3)
        if board[currPos] not in "012345678":
            newBoard += board[currPos]
        else:
            newBoard += str(i)
    return newBoard

def boardInDict(board,boards):
    if board in boards:
        return board, 0,0 #returning the board in the right direction then the number of flips and turns
    flip = flipped(board)
    if flip in boards:
        return flip, 1,0
    newBoard = turned(board)
    for i in range(3):
        if newBoard in boards:
            return newBoard, 0,i+1
        flip = flipped(newBoard)
        if flip in boards:
            return flip, 1,i+1
        old = newBoard
        newBoard = turned(old)
    return "XXXX", "X","X"

def turnBack(flips,turns,board):
    curr = board
    for i in range(flips):
        new = flipped(curr)
        curr = new
    for i in range(4-turns):
        new = turned(curr)
        curr = new
    return curr

def findMove(old,new):
    for i in range(9):
        if old[i] != new[i]:
            return i
    return "X"

def prettyPrint(board):
    print(f"\n {board[0]} | {board[1]} | {board[2]} \n{"-"*11}\n {board[3]} | {board[4]} | {board[5]} \n{"-"*11}\n {board[6]} | {board[7]} | {board[8]} \n")

def isWon(board):
    for i in range(3):
        if board[3*(i)] == board[3*(i)+1] and board[3*(i)] == board[3*(i)+2]:
            return board[3*i]
        if board[i] == board[i+3] and board[i] == board[i+6]:
            return board[i]
    if board[0] == board[4] and board[0] == board[8]:
        return board[0]
    if board[2] == board[4] and board[2] == board[6]:
        return board[2]
    return None

def computerMove(boards):
    global currentBoard,moves, computerFirst
    play = "O"
    if computerFirst:
        play = "X"
    board,flips,turns = boardInDict(currentBoard,boards)
    if board != "XXXX":
        if len(boards[board]) == 0:
            return "Forfeit"
        move = random.choice(boards[board])
        temp = board[:move] + play + board[move+1:]
        newBoard = turnBack(flips,turns,temp)
        realMove = findMove(currentBoard,newBoard)
        print(f"\nThe computer moved to {realMove}. The board is now") # Change to position of move after de-flipping
        prettyPrint(newBoard)
        moves.append((board,move))
        currentBoard = newBoard
    else:
        print(f"Something went wrong! Entered board: {currentBoard}")
        sys.exit()

def learningFirst(won):
    global moves,first
    for m in moves:
        board = m[0]
        move = m[1]
        if won == "Won":
            for i in range(3):
                first[board].append(move)
        elif won == "Draw":
            first[board].append(move)
        else:
            if move in first[board]:
                first[board].remove(move)
            else:
                print(f"{move}, {first[board]}, {board}")

def learningSecond(won):
    global moves,second
    for m in moves:
        board = m[0]
        move = m[1]
        if won == "Won":
            for i in range(3):
                second[board].append(move)
        elif won == "Draw":
            second[board].append(move)
        else:
            if move in second[board]:
                second[board].remove(move)
            else:
                print(f"{move}, {second[board]}, {board}")


def setup():
    global first, second
    with open("boardsFirst.bin","rb") as fst:
        first = pickle.load(fst)
    with open("boardsSecond.bin","rb") as snd:
        second = pickle.load(snd)

def playerMove():
    global currentBoard, computerFirst
    play = "X"
    if computerFirst:
        play = "O"
    playerMove = input("What position would you like to move to? ")
    while playerMove:
        if playerMove in ["0","1","2","3","4","5","6","7","8"]:
            currentBoard = currentBoard[:int(playerMove)] + play + currentBoard[int(playerMove)+1:]
            print("The board is now:")
            prettyPrint(currentBoard)
            return
        else:
            print("I didn't understand :( Pick again\n")
        playerMove = input("What position would you like to move to? ")

setup()
print("\nWelcome to the naughts and crosses bot!!!")
quit = False
while not quit:
    currentBoard = "012345678"
    moves = []
    fst = input("\nWould you like to go first?(yes/no) ").lower()
    computerFirst = True
    if fst == "yes" or fst == "y":
        computerFirst = False
        print("\nGreat! You're crosses :)\nThe board is;")
        prettyPrint("012345678")
    count = 0
    wonBy = None
    forfeit = False

    if computerFirst:
        while count < 9 and wonBy is None and forfeit == False:
            if count%2 == 0:
                if count <8:
                    trash = computerMove(first)
                    if trash == "Forfeit":
                        forfeit = True
                else:
                    for i in range(9):
                        if currentBoard[i] in "012345678":
                            currentBoard = currentBoard[:i] + "X" + currentBoard[i+1:]
                            print(f"\nThe computer moved to {i}. The board is now")
                            prettyPrint(currentBoard)
            else:
                playerMove()
            count += 1
            wonBy = isWon(currentBoard)

        if wonBy == "X":
            print("You lost :(")
            learningFirst("Won")
        elif wonBy == "O":
            print("You won! Congratulations :)")
            learningFirst("Lost")
        else:
            print("It was a draw :/")
            learningFirst("Draw")
    else:

        while count < 9 and wonBy is None and forfeit == False:
            if count%2 == 0:
                playerMove()

            else:
                trash = computerMove(second)
                if trash == "Forfeit":
                    forfeit = True

            count+=1
            wonBy = isWon(currentBoard)

        if wonBy == "X":
            print("You won! Congratulations :)")
            learningSecond("Lost")
        elif wonBy == "O":
            print("You lost :(")
            learningSecond("Won")
        else:
            print("It was a draw :/")
            learningSecond("Draw")

    again = input("\nWould you like to play again?(yes/no) ").lower()
    if again == "no" or again == "n":
        quit = True
        print("\nOk :( Goodbye")
    else:
        print("Yay!!")   



