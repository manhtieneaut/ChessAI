import pygame

from utils.const import *
from game.board import Board
from game.dragger import Dragger
from utils.config import Config
from game.square import Square

class Game:

    def __init__(self):
        # Lượt chơi tiếp theo, mặc định là 'white'
        self.next_player = 'white'
        # Ô hiện tại được hover
        self.hovered_sqr = None
        # Bảng cờ
        self.board = Board()
        # Đối tượng Dragger để di chuyển quân cờ
        self.dragger = Dragger()
        # Cấu hình game
        self.config = Config()

    # Các phương thức blit
    # Vẽ bàn cờ
    def show_bg(self, surface):
        # Hiển thị nền bàn cờ
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                # Màu của ô
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark  
                # Tạo hình chữ nhật đại diện cho ô
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)    

                # Hiển thị chỉ số hàng
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    #label
                    lbl = self.config.font.render(str(ROWS-row), 1, color)
                    lbl_pos = (5, 5 + row * SQSIZE)
                    # blit
                    surface.blit(lbl, lbl_pos)

                # Hiển thị chỉ số cột
                if row == 7:
                    # color
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    #label
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 0, HEIGHT - 20)
                    # blit
                    surface.blit(lbl, lbl_pos)    

    # xắp xếp quân cờ để bắt đầu chơi
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # Kiểm tra ô có quân cờ không
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece 

                    # Không hiển thị quân đang được kéo
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80) 
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect =  img.get_rect(center = img_center)
                        surface.blit(img, piece.texture_rect)           

    def show_moves(self, surface):
        # Hiển thị các nước đi có thể của quân đang kéo
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece
            for move in piece.moves:
                # Màu của ô
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                # Tạo hình chữ nhật đại diện cho ô
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
    
    def show_last_moves(self, surface):
        # Hiển thị các ô đã được di chuyển gần nhất
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in (initial, final):
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        # Hiển thị ô được hover
        if self.hovered_sqr:
            color = (180, 180, 180) 
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    # other method
    # Chuyển lượt chơi sang bên đối diện
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
    
    # Đặt ô được hover
    def set_hover(self, row, col):
        if Square.in_range(row, col):
            self.hovered_sqr = self.board.squares[row][col]
        
    # Thay đổi chủ đề của game
    def change_theme(self):
        self.config.change_theme()    

    # Phát âm thanh
    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
    # Reset trạng thái của game
    def reset(self):
        self.__init__()  

    


