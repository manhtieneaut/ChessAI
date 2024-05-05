

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
        self.whileToMove =  True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.enpassantPossible = ()
        self.curentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.curentCastlingRight.wks, self.curentCastlingRight.bks,
                                            self.curentCastlingRight.wqs, self.curentCastlingRight.bqs)]
        

    def makeMove(self, move):
        self.board[move.startRow][move.startCol]  = "--"  
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so we can undo it later
        self.whileToMove = not self.whileToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol) 
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol) 

        #pawn promotion
        if move.isPawnPromotion == True:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # enpassant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--'

        # update enpassantPossible move variable    
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = () 
        # castle
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = '--'
            else:
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = '--'          

        # castlingRight update
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.curentCastlingRight.wks, self.curentCastlingRight.bks,
                                            self.curentCastlingRight.wqs, self.curentCastlingRight.bqs))

    
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.curentCastlingRight.wks = False
            self.curentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.curentCastlingRight.bks = False
            self.curentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.curentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.curentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.curentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.curentCastlingRight.bks = False
        


    def undoMove(self):
    # Kiểm tra xem có nước đi nào để hoàn tác hay không.
        if len(self.moveLog) != 0:
            # Lấy nước đi cuối cùng.
            move = self.moveLog.pop()

            # Khôi phục trạng thái của bàn cờ.
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured

            # Chuyển lượt chơi sang người chơi tiếp theo.
            self.whileToMove = not self.whileToMove

            # Cập nhật vị trí vua nếu cần thiết.
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol) 
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol) 

            # Hoàn tác việc bắt quân (nếu có).
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)

            # Khôi phục trạng thái en passant (nếu có).
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

            # undo castle right
                self.castleRightsLog.pop()
                newRights = self.castleRightsLog[-1]
                self.curentCastlingRight = CastleRights(newRights.wks, newRights.bks,
                                                        newRights.wqs, newRights.bqs)

            # undo castle move    
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'
                
    
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.curentCastlingRight.wks, self.curentCastlingRight.bks,
                                        self.curentCastlingRight.wqs, self.curentCastlingRight.bqs)
        # 1 genneral posible move
        moves = self.getAllPossibleMoves()    
        
        if self.whileToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.whileToMove = not self.whileToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whileToMove = not self.whileToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True 
        else:
            self.checkmate = False
            self.stalemate = False        

        self.enpassantPossible = tempEnpassantPossible   
        self.curentCastlingRight = tempCastleRights
        return moves

    def inCheck(self):
        if self.whileToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
        
    def squareUnderAttack(self, r, c):
        self.whileToMove = not self.whileToMove
        oopMoves = self.getAllPossibleMoves()
        self.whileToMove = not self.whileToMove
        for move in oopMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False  

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whileToMove) or (turn == 'b' and not self.whileToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whileToMove:
            if self.board[r - 1][c] == "--":
                moves.append(Move((r, c),(r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c),(r - 2, c), self.board))

            if c - 1 >= 0: # capture to the left
                if self.board[r - 1][c - 1][0] == 'b': #enemy to capture
                    moves.append(Move((r, c),(r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c),(r - 1, c - 1), self.board, isEnpassantMove=True))

            if c + 1 <= 7: # cpture to the right
                if self.board[r - 1][c + 1][0] == 'b': #enemy to capture
                    moves.append(Move((r, c),(r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c),(r - 1, c + 1), self.board, isEnpassantMove=True))    

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
                    moves.append(Move((r, c),(r + 1, c - 1), self.board, isEnpassantMove=True))    

            if c + 1 <= 7: # cpture to the right
                if self.board[r + 1][c + 1][0] == 'w': #enemy to capture
                    moves.append(Move((r, c),(r + 1, c + 1), self.board))   
                elif (r + 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c),(r + 1, c + 1), self.board, isEnpassantMove=True))    
    

        # add pawn promotion next time later                     

    def getRookMoves(self, r, c, moves):

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whileToMove else "w"
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
        allyColor = "w" if self.whileToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whileToMove else "w"
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
        allyColor = "w" if self.whileToMove else "b"
        for i in range(8):
            endRow = r + king_moves[i][0]
            endCol = c + king_moves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))    
     

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return
        if (self.whileToMove and self.curentCastlingRight.wks) or (not self.whileToMove and self.curentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whileToMove and self.curentCastlingRight.wqs) or (not self.whileToMove and self.curentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)
        
        
    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
            if not self.squareUnderAttack( r , c + 1) and not self.squareUnderAttack(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove = True))


    def getQueensideCastleMoves(self, r, c, moves):    
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[ r ][c - 3] == '--':
            if not self.squareUnderAttack( r , c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove = True))



class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
                                        
class Move():
    # map keys to values
    # key : value

    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    
    rowsToRanks = {v: k for k , v in ranksToRows.items()}

    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    
    colsToFiles = {v: k for k , v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]  
        self.pieceCaptured = board[self.endRow][self.endCol]  
        # pawn promotion
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)

        # EnpassantMove    
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'pb' else 'bp'   

        # Castle move
        self.isCastleMove = isCastleMove    

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    
    def __eq__(self, other):
        if isinstance (other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]



