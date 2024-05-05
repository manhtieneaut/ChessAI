import random

pieceScore = {"K":0, "Q":10, "R":5, "B":3, "N":3, "p":1}
CHECKMATE = 1000
STATEMATE = 0
DEPTH = 4

def findRandomMove(validmoves):
    return validmoves[random.randint(0, len(validmoves)-1)]

def findBestMoveMinMaxNoRecursion(gs, validMoves):
    turnMultiplier = 1 if gs.whileToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)

    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.stalemate:
            opponentMaxScore = STATEMATE
        elif gs.checkmate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                gs.getValidMoves()
                if gs.checkmate:
                    score = CHECKMATE
                elif gs.stalemate:
                    score = STATEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                    # bestPlayerMove = playerMove
                gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()    
    return bestPlayerMove


def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    #findMoveMinMax(gs, validMoves, DEPTH, gs.whileToMove)
    findMoveNegaMaxAlphaBeta( gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whileToMove else -1)
    return nextMove


def findMoveMinMax(gs, validMoves, depth, whileToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    
    if whileToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore            

    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False) 
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore             

def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move 
        gs.undoMove()
    return maxScore 

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    

    #move ordering - implememt later
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1,-beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move 
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break

    return maxScore    


def scoreBoard(gs):
    if gs.checkmate:
        if gs.whileToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STATEMATE   

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score += pieceScore[square[1]]

    return score


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row :
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    
    return score