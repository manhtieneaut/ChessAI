import pygame as p
import ChessEngine

# Khởi tạo Pygame
p.init()

# Các hằng số
WIDTH = HEIGHT = 512
DIMENTION = 8
SQ_SIZE = HEIGHT // DIMENTION
MAX_FPS = 15
IMAGES = {}

# Tải hình ảnh các quân cờ
def loadImage():
    pieces = [
            'wp',
            'wR',
            'wN',
            'wB',
            'wQ',
            'wK',
            'bp',
            'bR',
            'bN',
            'bB',
            'bQ',
            'bK']
            
    # Tải hình ảnh cho từng quân cờ và lưu vào từ điển IMAGES
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("./assets/imgs-80px/" + piece + ".png"),(SQ_SIZE, SQ_SIZE)) 

# Hàm chính
def main():
    p.init()        
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    loadImage()
    # Vòng lặp chính
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    while running:
        # Vòng lặp xử lý sự kiện
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse hanler    
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:    
                    # Lấy vị trí của chuột
                    location = p.mouse.get_pos() #location of move
                    # Tính cột và hàng của ô đã được click
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected  = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2: #sau khi click lần thứ 2
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()        
                    moveMade = True
                    animate = False
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False    
        
        if moveMade:
            if animate:
                animaMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkmate:
            gameOver = True
            if gs.WhileToMove:
                drawText(screen, 'Black wins by checkmate')
            else:    
                drawText(screen, 'White wins by checkmate')
        elif gs.stalemate:
            gameOver = True
            drawText(screen, 'Stalemate')        

        clock.tick(MAX_FPS)
        p.display.flip()       

# Hightlight square selected and move for piece selected
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.WhileToMove else 'b'): #sqselected is a piece
            #highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE,r*SQ_SIZE))
            #hightlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s,(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

# Vẽ trạng thái hiện tại của trò chơi
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

# Vẽ bàn cờ
def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in  range(DIMENTION):
        for c in range(DIMENTION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE ,SQ_SIZE))

# Vẽ các quân cờ trên bàn cờ
def drawPieces(screen, board):  
    for r in  range(DIMENTION):
        for c in range(DIMENTION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE ,SQ_SIZE)) 

# animation
def animaMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #erase
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captureed piece onto recttangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2 ,HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.color('Black'))
    screen.blit(textObject, textLocation.move(2, 2)) 

# Chạy hàm main nếu đây là script được thực thi
if __name__ == "__main__":   
    main()  
