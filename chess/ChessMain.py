import pygame as p
import ChessEngine
import SmartMove

# Khởi tạo Pygame
p.init()

# Các hằng số
WIDTH = HEIGHT = 512  # Kích thước cửa sổ bàn cờ
DIMENTION = 8  # Kích thước bàn cờ (8x8)
SQ_SIZE = HEIGHT // DIMENTION  # Kích thước của mỗi ô vuông trên bàn cờ
MAX_FPS = 15  # Tốc độ khung hình tối đa của trò chơi
IMAGES = {}  # Từ điển để lưu trữ hình ảnh các quân cờ

# Tải hình ảnh các quân cờ
def loadImage():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    # Tải hình ảnh cho từng quân cờ và chỉnh kích thước để phù hợp với ô vuông
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("./assets/imgs-80px/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

# Vẽ menu lên màn hình
def drawMenu(screen):
    background = p.image.load("./assets/backgrounds/back1.jpg")  # Tải ảnh nền
    background = p.transform.scale(background, (WIDTH, HEIGHT))  # Thay đổi kích thước ảnh nền
    screen.blit(background, (0, 0))  # Vẽ ảnh nền lên toàn màn hình
    font = p.font.SysFont("Helvitca", 45, True, False)
    text_start = font.render("Start", True, p.Color('White'))
    text_ai = font.render("Two players", True, p.Color('White'))
    text_exit = font.render("Exit", True, p.Color('White'))
    screen.blit(text_start, (WIDTH // 2 - text_start.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(text_ai, (WIDTH // 2 - text_ai.get_width() // 2, HEIGHT // 2))
    screen.blit(text_exit, (WIDTH // 2 - text_exit.get_width() // 2, HEIGHT // 2 + 60))
    p.display.flip()


# Hàm chính để chạy trò chơi
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))  # Thiết lập cửa sổ hiển thị
    clock = p.time.Clock()  # Thiết lập đồng hồ trò chơi
    screen.fill(p.Color("white"))  # Đổ màu trắng cho màn hình
    gs = ChessEngine.GameState()  # Khởi tạo trạng thái trò chơi
    validMoves = gs.getValidMoves()  # Lấy danh sách các nước đi hợp lệ
    moveMade = False  # Cờ kiểm tra nếu có nước đi được thực hiện
    animate = False  # Cờ kiểm tra nếu cần hiệu ứng
    loadImage()  # Tải hình ảnh của các quân cờ
    running = True  # Cờ vòng lặp chính
    sqSelected = ()  # Ô được chọn (ban đầu không có)
    playerClicks = []  # Danh sách lưu trữ các lần nhấp của người chơi
    gameOver = False  # Cờ kiểm tra nếu trò chơi kết thúc
    playerOne = True  # Cờ chỉ người chơi một là người chơi
    playerTwo = False  # Cờ chỉ người chơi hai là người chơi
    showMenu = True  # Cờ hiển thị menu

    while running:
        if showMenu:
            drawMenu(screen)
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()
                    if WIDTH // 2 - 100 <= location[0] <= WIDTH // 2 + 100:
                        if HEIGHT // 2 - 60 <= location[1] <= HEIGHT // 2 - 30:
                            showMenu = False  # Bắt đầu chơi
                        elif HEIGHT // 2 <= location[1] <= HEIGHT // 2 + 30:
                            showMenu = False  # Chơi với AI
                            playerTwo = True  # Chỉ định AI là người chơi thứ hai
                        elif HEIGHT // 2 + 60 <= location[1] <= HEIGHT // 2 + 90:
                            running = False  # Thoát
        else:
            humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
            
            # Vòng lặp xử lý sự kiện
            for e in p.event.get():
                if e.type == p.QUIT:  # Nếu người dùng thoát trò chơi
                    running = False
                
                elif e.type == p.MOUSEBUTTONDOWN:  # Nếu nút chuột được nhấn
                    if not gameOver and humanTurn:
                        location = p.mouse.get_pos()  # Lấy vị trí của chuột
                        col = location[0] // SQ_SIZE  # Tính cột dựa trên vị trí chuột
                        row = location[1] // SQ_SIZE  # Tính hàng dựa trên vị trí chuột
                        if sqSelected == (row, col):  # Nếu cùng một ô được nhấp lại
                            sqSelected = ()  # Bỏ chọn ô
                            playerClicks = []  # Xóa các lần nhấp của người chơi
                        else:
                            sqSelected = (row, col)  # Chọn ô mới
                            playerClicks.append(sqSelected)  # Thêm ô được chọn vào danh sách nhấp
                        if len(playerClicks) == 2:  # Nếu hai ô được chọn
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)  # Tạo một nước đi
                            print(move.getChessNotation())  # In nước đi theo ký hiệu cờ vua
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(validMoves[i])  # Thực hiện nước đi
                                    moveMade = True  # Đặt cờ moveMade thành True
                                    animate = True  # Đặt cờ animate thành True
                                    sqSelected = ()  # Bỏ chọn các ô
                                    playerClicks = []  # Xóa các lần nhấp của người chơi
                            if not moveMade:
                                playerClicks = [sqSelected]  # Đặt lại danh sách nhấp của người chơi về lựa chọn hiện tại
                
                elif e.type == p.KEYDOWN:  # Nếu một phím được nhấn
                    if e.key == p.K_z:  # Nếu phím 'z' được nhấn, hoàn tác nước đi
                        gs.undoMove()
                        moveMade = True
                        animate = False
                    if e.key == p.K_r:  # Nếu phím 'r' được nhấn, thiết lập lại trò chơi
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False

            # AI tìm nước đi
            if not gameOver and not humanTurn:
                AIMove = SmartMove.findBestMove(gs, validMoves)  # Tìm nước đi tốt nhất cho AI
                if AIMove == None:
                    AIMove = SmartMove.findRandomMove(validMoves)  # Nếu không có nước đi tốt nhất, tìm nước đi ngẫu nhiên
                gs.makeMove(AIMove)  # Thực hiện nước đi của AI
                moveMade = True
                animate = True

            if moveMade:  # Nếu có nước đi được thực hiện
                if animate:
                    animaMove(gs.moveLog[-1], screen, gs.board, clock)  # Hiệu ứng nước đi
                validMoves = gs.getValidMoves()  # Lấy danh sách mới của các nước đi hợp lệ
                moveMade = False
                animate = False

            drawGameState(screen, gs, validMoves, sqSelected)  # Vẽ trạng thái trò chơi

            if gs.checkmate:  # Kiểm tra chiếu hết
                gameOver = True
                if gs.whiteToMove:
                    drawText(screen, 'Black wins by checkmate')  # Hiển thị thông báo nếu đen thắng
                else:
                    drawText(screen, 'White wins by checkmate')  # Hiển thị thông báo nếu trắng thắng
            elif gs.stalemate:  # Kiểm tra hòa
                gameOver = True
                drawText(screen, 'Stalemate')  # Hiển thị thông báo hòa

            clock.tick(MAX_FPS)  # Điều khiển tốc độ khung hình
            p.display.flip()  # Cập nhật màn hình

# Làm nổi bật ô được chọn và các nước đi có thể cho quân cờ được chọn
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):  # Kiểm tra nếu ô được chọn là quân cờ
            # Làm nổi bật ô được chọn
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # Thiết lập độ trong suốt
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # Làm nổi bật các nước đi từ ô được chọn
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))

# Vẽ trạng thái hiện tại của trò chơi
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)  # Vẽ bàn cờ
    highlightSquares(screen, gs, validMoves, sqSelected)  # Làm nổi bật các ô
    drawPieces(screen, gs.board)  # Vẽ các quân cờ trên bàn cờ

# Vẽ bàn cờ
def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]  # Định nghĩa màu của bàn cờ
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            color = colors[(r + c) % 2]  # Thay đổi màu
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))  # Vẽ ô vuông

# Vẽ các quân cờ trên bàn cờ
def drawPieces(screen, board):
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            piece = board[r][c]
            if piece != "--":  # Nếu có quân cờ trên ô
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))  # Vẽ quân cờ

# Hiệu ứng nước đi
def animaMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow  # Hàng đích
    dC = move.endCol - move.startCol  # Cột đích
    framesPerSquare = 10  # Số khung hình trên mỗi ô vuông
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare  # Tổng số khung hình
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)  # Vẽ bàn cờ
        drawPieces(screen, board)  # Vẽ các quân cờ
        # Xóa ô đích
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # Vẽ quân cờ bị ăn lên ô đích (nếu có)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # Vẽ quân cờ đang di chuyển
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)  # Điều chỉnh tốc độ khung hình

# Vẽ văn bản lên màn hình (ví dụ: thông báo kết thúc trò chơi)
def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)  # Định nghĩa phông chữ
    textObject = font.render(text, 0, p.Color('Black'))  # Tạo văn bản
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2, HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)  # Hiển thị văn bản lên màn hình
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))  # Hiển thị văn bản với bóng đổ

# Chạy hàm main nếu đây là script được thực thi
if __name__ == "__main__":
    main()
