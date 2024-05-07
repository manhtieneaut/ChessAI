import random

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STATEMATE = 0
DEPTH = 2

def findRandomMove(validmoves):
    return validmoves[random.randint(0, len(validmoves) - 1)]

def findBestMove(gs, validMoves):
    random.shuffle(validMoves)
    maxScore = -CHECKMATE
    bestMove = None
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, DEPTH - 1, -CHECKMATE, CHECKMATE, 1 if gs.whileToMove else -1)
        if score > maxScore:
            maxScore = score
            bestMove = move
        gs.undoMove()
    return bestMove

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        maxScore = max(maxScore, score)
        alpha = max(alpha, score)
        gs.undoMove()
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
                score -= pieceScore[square[1]]
    return score

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score
