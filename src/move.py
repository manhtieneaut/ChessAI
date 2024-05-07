
# __init__(self, initial, final): Khởi tạo một đối tượng Move với hai tham số là initial và final, 
# đại diện cho ô ban đầu và ô cuối của nước đi.

# __str__(self): Phương thức này trả về một chuỗi mô tả nước đi dưới định dạng (initial_col, initial_row) 
# -> (final_col, final_row). Ví dụ: (3, 1) -> (3, 3).

# __eq__(self, other): So sánh hai nước đi, trả về True nếu cả hai có cùng ô ban đầu và ô cuối.
# Điều này giúp kiểm tra xem hai nước đi có giống nhau không.

class Move:
    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v: k for k , v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v: k for k , v in filesToCols.items()}

    def __init__(self, initial, final):
        # initial and final are squares
        self.initial = initial
        self.final = final

    def __str__(self):
        s = ''
        s += f'({self.initial.col}, {self.initial.row})'
        s += f' -> ({self.final.col}, {self.final.row})'
        return s
    
    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final
    
    # In ra kí hiệu nước cờ : VD a1d4 a4d8 
    def getChessNotation(self):
        return self.getRankFile(self.initial.row, self.initial.col) + self.getRankFile(self.final.row, self.final.col)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]  