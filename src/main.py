from utils.const import *
from game.game import Game
from game.square import Square
from game.move import Move

import pygame
import sys

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        # icon = pygame.image.load("./assets/images/system-image/system.jpg") 
        # pygame.display.set_icon(icon)
        self.game = Game()
        self.menu_active = True

    def show_menu(self):
        while self.menu_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Kiểm tra xem con chuột có ở trên nút không
                    if button_rect.collidepoint(pygame.mouse.get_pos()):
                        self.menu_active = False  # Chuyển trạng thái để bắt đầu trò chơi
            # Load và vẽ hình nền
            menu_background = pygame.image.load("./assets/images/system-image/back-menu.jpg")  # Thay "menu_background.jpg" bằng đường dẫn đến tệp hình ảnh của bạn
            menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
            self.screen.blit(menu_background, (0, 0))   
                    
            # Hiển thị màn hình mờ
            menu_bg = pygame.Surface(self.screen.get_size())
            menu_bg.set_alpha(128)  # Đặt độ trong suốt
            menu_bg.fill((0, 0, 0))  # Đen
            self.screen.blit(menu_bg, (0, 0))
            
            # Vẽ nút "Chơi mới"
            button_width = 200
            button_height = 50
            button_color = (255, 255, 255)  # Màu trắng
            button_rect = pygame.Rect((WIDTH - button_width) // 2, (HEIGHT - button_height) // 2, button_width, button_height)
            pygame.draw.rect(self.screen, button_color, button_rect)
            
            # Vẽ văn bản trên nút
            font = pygame.font.Font(None, 36)
            text = font.render("Chơi mới", True, (0, 0, 0))  # Màu đen
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

            pygame.display.update()

    def play_game(self):     
        screen = self.screen
        game = self.game
        dragger = self.game.dragger
        board = self.game.board
        
        while True:
            # show methods
            game.show_bg(screen)
            game.show_last_moves(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                #click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    # Nếu ô click có quân
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # Kiểm tra màu của quân
                        if piece.color == game.next_player:
                            board.calc_moves(piece,clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_moves(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # Di chuyển chuột   
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        game.show_bg(screen)
                        game.show_last_moves(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                
                # Chuột được thả ra
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # Tạo nước đi có thể
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)
                        
                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)
                            board.set_true_en_passant(dragger.piece)
                            # Âm thanh
                            game.play_sound(captured)
                            # Hiển thị
                            game.show_bg(screen)
                            game.show_last_moves(screen)
                            game.show_pieces(screen)
                            # Chuyển lượt
                            game.next_turn()

                    dragger.undrag_piece()
                # Phím được nhấn
                elif event.type == pygame.KEYDOWN:

                    # Đổi chủ đề
                    if event.key == pygame.K_t:
                        game.change_theme()

                    # Reset trò chơi
                    if event.key == pygame.K_r:
                        game.reset()    
                        game = self.game
                        dragger = self.game.dragger
                        board = self.game.board

                    # Undo nước đi   
                    if event.key == pygame.K_z:    
                        board.undo_move()
                        game.next_turn()    
                        game = self.game
                        dragger = self.game.dragger
                        board = self.game.board  

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()              

    def mainloop(self):
        while True:
            self.show_menu()
            self.play_game()
    
        

main = Main()
main.mainloop()   
