

class Square:

    ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    def __init__(self, row, col, piece = None):
        self.row = row
        self.col = col
        self.piece = piece 
        self.alphacol = self.ALPHACOLS[col]
        
    # So sánh hai ô trên bảng cờ với nhau, trả về True nếu cả hai có cùng hàng và cùng cột.
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    
    # Kiểm tra xem ô có quân cờ không.
    def has_piece(self):
        return self.piece != None  
    
    # Kiểm tra xem ô có trống không.
    def isempty(self):
        return not self.has_piece()
    
    # Kiểm tra xem ô có quân cờ của màu đội của mình không.
    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color 
    
    # Kiểm tra xem ô có quân cờ của đối phương không.
    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color 
    
    # Kiểm tra xem ô có trống hoặc có quân cờ của đối phương không.
    def isempty_or_enemy(self, color):
        return self.isempty() or self.has_enemy_piece(color)
    
    # Phương thức tĩnh để kiểm tra xem một giá trị có nằm trong khoảng từ 0 đến 7 không.
    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
            
        return True
    
    # Phương thức tĩnh để lấy chữ cái biểu diễn cột của ô theo hệ thống bảng cờ vua, được sử dụng trong việc hiển thị giao diện người dùng.
    @staticmethod
    def get_alphacol(col):
        ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return ALPHACOLS[col]