import pickle

xMoves = {}
oMoves = {}

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

def boardInList(board,boards):
    if flipped(board) in boards:
        return True
    newBoard = turned(board)
    for i in range(3):
        if newBoard in boards:
            return True
        if flipped(newBoard) in boards:
            return True
        old = newBoard
        newBoard = turned(old)
    return False

def prettyPrint(board):
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("-"*11)
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("-"*11)
    print(f" {board[6]} | {board[7]} | {board[8]} ")

def isWon(board):
    for i in range(3):
        if board[3*(i)] == board[3*(i)+1] and board[3*(i)] == board[3*(i)+2]:
            return True
        if board[i] == board[i+3] and board[i] == board[i+6]:
            return True
    if board[0] == board[4] and board[0] == board[8]:
        return True
    if board[2] == board[4] and board[2] == board[6]:
        return True
    return False

def isValid(board):
    Xs = 0
    Os = 0
    for i in range(9):
        if board[i] == "X":
            Xs+=1
        elif board[i] == "O":
            Os+=1
    if Xs == Os or (Xs-1) == Os:
        return True
    return False

        
def findPossX(board):
    next = []
    for x in board:
        if x in "0123345678":
            next.append(int(x))
    if len(next) > 1:
        xMoves[board] = next


def findPossO(board):
    next = []
    for o in board:
        if o in "0123345678":
            next.append(int(o))
    if len(next) > 1:
        oMoves[board] = next

def findAllBoards(curr,num):
    if num == 9:
        return
    players = ["X","O"]
    player = players[num%2]
    new = []
    for board in curr:
        for i in range(9):
            if board[i] in "012345678":
                temp = board[:i] + player + board[i+1:]
                if player == "X":
                    if isValid(temp) and not isWon(temp) and not boardInList(temp,oMoves):
                        findPossO(temp)
                        new.append(temp)
                else:
                    if isValid(temp) and not isWon(temp) and not boardInList(temp,xMoves):
                        findPossX(temp)
                        new.append(temp)
    num+=1
    findAllBoards(new,num)

findPossX("012345678")
findAllBoards(["012345678"],0)
print(len(xMoves))

with open("boardsFirst.bin","wb") as x:
    pickle.dump(xMoves,x)

with open("boardsSecond.bin","wb") as o:
    pickle.dump(oMoves,o)

print("\n Done!!")