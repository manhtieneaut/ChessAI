

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
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = ()
        

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

        #pawn promotion
        if move.isPawnPromotion == True:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # enpassant
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--'

        # update enpassantPossible move variable    
        if move.pieceMoved[1] == 'p' and abs( move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow - move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()    


            

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
        tempEnpassantMove= self.enpassantPossible
        moves = self.getAllPossibleMoves()    
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.WhileToMove = not self.WhileToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.WhileToMove = not self.WhileToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate == True
            else:
                self.staleMate == True 
        else:
            self.checkMate == False
            self.staleMate ==False        

        self.enpassantPossible = tempEnpassantMove    
        return moves

    def inCheck(self):
        if self.WhileToMove:
            return self.squareUnderAttack(self.whileKingLocation[0], self.whileKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
        
    def squareUnderAttack(self, r, c):
        self.WhileToMove = not self.WhileToMove
        oopMoves = self.getAllPossibleMoves()
        self.WhileToMove = not self.WhileToMove
        for move in oopMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False  


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
        if self.WhileToMove:
            if self.board[r - 1][c] == "--":
                moves.append(Move((r, c),(r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c),(r - 2, c), self.board))

            if c - 1 >= 0: # capture to the left
                if self.board[r - 1][c - 1][0] == 'b': #enemy to capture
                    moves.append(Move((r, c),(r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c),(r - 1, c - 1), self.board, isEnpassantPossible=True))

            if c + 1 <= 7: # cpture to the right
                if self.board[r - 1][c + 1][0] == 'b': #enemy to capture
                    moves.append(Move((r, c),(r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c),(r - 1, c + 1), self.board, isEnpassantPossible=True))    

        # black pawn move
        else:
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c),(r+1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c),(r + 2, c), self.board))

            if c - 1 >= 0: # capture to the left
                if self.board[r + 1][c - 1][0] == 'w': #enemy to capture
                    moves.append(Move((r, c),(r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c),(r + 1, c - 1), self.board, isEnpassantPossible=True))    

            if c + 1 <= 7: # cpture to the right
                if self.board[r + 1][c + 1][0] == 'w': #enemy to capture
                    moves.append(Move((r, c),(r + 1, c + 1), self.board))   
                elif (r + 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c),(r + 1, c + 1), self.board, isEnpassantPossible=True))    
    

        # add pawn promotion next time later                     

    def getRookMoves(self, r, c, moves):

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.WhileToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
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
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2),(2, -1), (2, 1))
        allyColor = "w" if self.WhileToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.WhileToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
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
        king_moves = [(-1, -1), (1, 0), (-1, 1), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 0)]
        allyColor = "w" if self.WhileToMove else "b"
        for i in range(8):
            endRow = r + king_moves[i][0]
            endCol = c + king_moves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))    

                                    
class Move():
    # map keys to values
    # key : value

    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    
    rowsToRanks = {v: k for k , v in ranksToRows.items()}

    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    
    colsToFiles = {v: k for k , v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, enpassantPossible = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]  
        self.pieceCaptured = board[self.endRow][self.endCol]  
        # pawn promotion
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)

        # EnpassantMove    
        self.isEnpassantMove = enpassantPossible
        
        # self.promotionChoice = 'Q'    

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    
    def __eq__(self, other):
        if isinstance (other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]



