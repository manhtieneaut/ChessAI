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

    loadImage()
    # Vòng lặp chính
    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        # Vòng lặp xử lý sự kiện
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
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
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()        
                    moveMade = True
        
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()       

# Vẽ trạng thái hiện tại của trò chơi
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

# Vẽ bàn cờ
def drawBoard(screen):
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

# Chạy hàm main nếu đây là script được thực thi
if __name__ == "__main__":   
    main()  
