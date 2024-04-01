

class GameState():
    def __init__(self):
        self.board = [
            [ "bR" , "bN" , "bB" , "bQ" , "bK" , "bB" , "bN" , "bR" ],
            [ "bp" , "bp" , "bp" , "bp" , "bp" , "bp" , "bp" , "bp" ],
            [ "--" , "--" , "--" , "--" , "--" , "--" , "--" , "--" ],
            [ "--" , "--" , "--" , "--" , "--" , "--" , "--" , "--" ],
            [ "--" , "--" , "--" , "--" , "--" , "--" , "--" , "--" ],
            [ "--" , "--" , "--" , "--" , "--" , "--" , "--" , "--" ],
            [ "wp" , "wp" , "wp" , "wp" , "wp" , "wp" , "wp" , "wp" ],
            [ "wR" , "wN" , "wB" , "wQ" , "wK" , "wB" , "wN" , "wR" ]
            ] 
        
        self.moveFunctions = {'p': self.getPawnMoves, 'R':self.getRookMoves, 'N':self.getKnightMoves,
                            'B': self.getBishopMoves, 'Q':self.getQueenMoves, 'K':self.getKingMoves}
        self.WhileToMove =  True
        self.moveLog = []
        self.whileKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol]  = "--"  
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so we can undo it later
        self.WhileToMove = not self.WhileToMove
        #
        if move.pieceMoved == 'wK':
            self.whileKingLocation = (move.endRow, move.endCol) 
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol) 

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][ move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.WhileToMove = not self.WhileToMove
            # update the king 'position if needed
            if move.pieceMoved == 'wK':
                self.whileKingLocation = (move.startRow, move.startCol) 
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol) 
    
    def getValidMoves(self):
        #1 generate valid all possible move
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.WhileToMove:
            kingRow = self.whileKingLocation[0]
            kingCol = self.whileKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()    
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking =  self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)   
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break

                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()

        return moves



    # def inCheck(self):
    #     if self.WhileToMove:
    #         return self.squareUnderAttack(self.whileKingLocation[0], self.whileKingLocation[1])
    #     else:
    #         return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
        
    # def squareUnderAttack(self, r, c):
    #     self.WhileToMove = not self.WhileToMove
    #     oopMoves = self.getAllPossibleMoves()
    #     self.WhileToMove = not self.WhileToMove
    #     for move in oopMoves:
    #         if move.endRow == r and move.endCol == c:
    #             return True
    #     return False    


    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.WhileToMove) or (turn == 'b' and not self.WhileToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.WhileToMove:
            if self.board[r-1][c] == "--":
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c),(r-1, c), self.board))
                    if r == 6 and self.board[r-2][c] == "--":
                        moves.append(Move((r, c),(r-2, c), self.board))

            if c - 1 >= 0: # capture to the left
                if self.board[r - 1][c - 1][0] == 'b': #enemy to capture
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r, c),(r - 1, c - 1), self.board))

            if c + 1 <= 7: # cpture to the right
                if self.board[r - 1][c - 1][0] == 'b': #enemy to capture
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r, c),(r - 1, c + 1), self.board))

        # black pawn move
        else:
            if self.board[r + 1][c] == "--":
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((r, c),(r-1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "--":
                        moves.append(Move((r, c),(r+2, c), self.board))

            if c - 1 >= 0: # capture to the left
                if self.board[r + 1][c - 1][0] == 'w': #enemy to capture
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((r, c),(r + 1, c - 1), self.board))

            if c + 1 <= 7: # cpture to the right
                if self.board[r + 1][c + 1][0] == 'w': #enemy to capture
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((r, c),(r - 1, c + 1), self.board))   

        # add pawn promotion next time later                     

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.WhileToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:    
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
            
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2),(2, -1), (2, 1))
        allyColor = "w" if self.WhileToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirections = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirections = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break


        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.WhileToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirections == d or pinDirections == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:    
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                    else:
                        break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.WhileToMove else "b"

        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    if allyColor == 'w':
                        self.whileKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)    
                    inCheck, pins, checks = self.checkForPinsAndChecks()    
                    if not checks:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    if allyColor == 'w':
                        self.whileKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)            

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.WhileToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whileKingLocation[0]
            startCol = self.whileKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))    
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece  = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5 ))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow ,endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2),(2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck =True
                    inCheck.append((endRow, endCol, m[0], m[1]))

        return inCheck, pins, checks
    


class Move():
    # map keys to values
    # key : value

    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    
    rowsToRanks = {v: k for k , v in ranksToRows.items()}

    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    
    colsToFiles = {v: k for k , v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]  
        self.pieceCaptured = board[self.endRow][self.endCol]  
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    
    def __eq__(self, other):
        if isinstance (other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]



