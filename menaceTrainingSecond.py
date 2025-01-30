import random, sys, pickle

# run 20 000

second = {}
winCount = 0


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
        return board, 0,0
    flip = flipped(board)
    if flip in boards:
        return flip, 1,0
    newBoard = turned(board)
    for i in range(3):
        if newBoard in boards:
            return newBoard, 0, i+1
        flip = flipped(newBoard)
        if flip in boards:
            return flip, 1, i+1
        old = newBoard
        newBoard = turned(old)
    return "XXXX", "X","X"

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

def computerMove():
    global currentBoard,moves,second, analysisMoves
    board,flips,turns= boardInDict(currentBoard,second)
    if board != "XXXX":
        if len(second[board])>0:
            move = random.choice(second[board])
        else:
            return "forfeit"
        moves.append((board,move))
        curr = board[:move] + "O" + board[move+1:]
        for i in range(flips):
            new = flipped(curr)
            curr = new
        for i in range(4-turns):
            new = flipped(curr)
            curr = new
        currentBoard = new
        analysisMoves.append(currentBoard)
        
    else:
        print(f"Something went wrong! Entered board: {currentBoard}")
        sys.exit()

def toFile(won):
    global analysisMoves
    with open("winLoss.txt","a") as f:
        f.write(f"{won}: {analysisMoves}\n")


def learning(won):
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
    global second
    with open("boardsSecond.bin","rb") as snd:
        second = pickle.load(snd)

setup()
trend = 0
for i in range(1000):
    forfeit = False
    currentBoard = "012345678"
    moves = []
    analysisMoves = []
    count = 0
    wonBy = None
    while count<9 and wonBy is None and forfeit == False: 
        if count%2 == 0:
            playerMove = random.randint(0,8)
            while currentBoard[playerMove] not in ["0","1","2","3","4","5","6","7","8"]:
                playerMove = random.randint(0,8)
            currentBoard = currentBoard[:playerMove] + "X" + currentBoard[playerMove+1:]
            analysisMoves.append(currentBoard)
        else:
            if count != 8:
                temp = computerMove()
                if temp == "forfeit":

                    forfeit = True
            else:
                for i in range(9):
                    if currentBoard[i] in "012345678":
                        currentBoard = currentBoard[:i] + "O" + currentBoard[i+1:]
                        analysisMoves.append(currentBoard)
                        
        count +=1
        wonBy = isWon(currentBoard)
    if wonBy == "X":
        print("--------- Loss")
        trend -=1
        learning("Lost")
        toFile("Lost")
    elif wonBy == "O":
        print("------------------- Win")
        trend += 3
        winCount+=1
        learning("Won")
        toFile("Won")
    else:
        print("Draw")
        trend += 1
        learning("Draw")
        toFile("Draw")

print(winCount)
with open("boardsSecond.bin","wb") as l:
    pickle.dump(second,l)