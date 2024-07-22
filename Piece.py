class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position
    
    def move(self, new_position):
        self.position = new_position

    def valid_moves(self, board):
        raise NotImplementedError("Este método debe ser implementado por subclases")
    
    def __str__(self):
        return f"{self.__class__.__name__}({self.color}, {self.position})"

    def __repr__(self):
        return self.__str__()
