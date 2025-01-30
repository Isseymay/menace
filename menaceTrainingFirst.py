import random, sys, pickle

# run 20 000

first = {}
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
    global currentBoard,moves,first, analysisMoves
    board,flips,turns= boardInDict(currentBoard,first)
    if board != "XXXX":
        if len(first[board])>0:
            move = random.choice(first[board])
        else:
            return "forfeit"
        moves.append((board,move))
        curr = board[:move] + "X" + board[move+1:]
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
    

    
 
def setup():
    global first
    with open("boardsFirst.bin","rb") as fst:
        first = pickle.load(fst)

setup()
trend = 0
for i in range(1001):
    forfeit = False
    currentBoard = "012345678"
    moves = []
    analysisMoves = []
    temp = computerMove()
    if temp == "forfeit":
        print(f"First Move forfeit {first["012345678"]}")
        forfeit = True
    count = 1
    wonBy = isWon(currentBoard)
    while count<9 and wonBy is None and forfeit == False: 
        if count%2 == 1:
            playerMove = random.randint(0,8)
            while currentBoard[playerMove] not in ["0","1","2","3","4","5","6","7","8"]:
                playerMove = random.randint(0,8)
            currentBoard = currentBoard[:playerMove] + "O" + currentBoard[playerMove+1:]
            analysisMoves.append(currentBoard)
        else:
            if count != 8:
                temp = computerMove()
                if temp == "forfeit":
                    
                    forfeit = True
            else:
                for i in range(9):
                    if currentBoard[i] in "012345678":
                        currentBoard = currentBoard[:i] + "X" + currentBoard[i+1:]
                        analysisMoves.append(currentBoard)
                        
        count +=1
        wonBy = isWon(currentBoard)
    if wonBy == "O":
        trend -=1
        learning("Lost")
        toFile("Lost")
    elif wonBy == "X":
        trend += 3
        winCount+=1
        learning("Won")
        toFile("Won")
    else:
        trend += 1
        learning("Draw")
        toFile("Draw")


print(winCount)
with open("boardsFirst.bin","wb") as l:
    pickle.dump(first,l)