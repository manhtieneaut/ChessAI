import pygame

from const import *

class Dragger: 

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0

    # Cập nhật và hiển thị hình ảnh của quân cờ khi kéo
    def update_blit(self, surface):
        # Lấy texture của quân cờ
        self.piece.set_texture(size=128)
        texture = self.piece.texture
        # Load hình ảnh từ texture
        img = pygame.image.load(texture) 
        # Tính toán tọa độ trung tâm của hình ảnh
        img_center = (self.mouseX, self.mouseY)
        # Tạo hình chữ nhật đại diện cho hình ảnh
        self.piece.texture_rect = img.get_rect(center=img_center)
        # Hiển thị hình ảnh lên màn hình
        surface.blit(img, self.piece.texture_rect)  

    # Cập nhật vị trí chuột
    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos # (xcor,ycor)

    # Lưu vị trí ban đầu của quân cờ trước khi kéo
    def save_initial(self, pos):
        self.initial_row = pos[1] // SQSIZE    
        self.initial_col = pos[0] // SQSIZE   

    # Bắt đầu kéo quân cờ
    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    # Kết thúc kéo quân cờ
    def undrag_piece(self):
        self.piece = None
        self.dragging = False        
