
class Piece:
    def __init__(self, type, color):
        self.type = type
        self.color = color
        self.hasMoved = False

class Pawn(Piece):
    def __init__(self, color):
        super().__init__('pawn', color)

    def getMoves(self, board, row, col):
        moves = []
        direction = -1 if self.color == 'white' else 1
        startRow = 6 if self.color == 'white' else 1

        if 0 <= row + direction < 8 and board[row + direction][col] is None:
            moves.append((row + direction, col))

            if row == startRow and board[row + 2 * direction][col] is None:
                moves.append((row + 2 * direction, col))

        for dc in [-1, 1]:
            newCol = col + dc
            newRow = row + direction
            if 0 <= newCol < 8 and 0 <= newRow < 8:
                target = board[newRow][newCol]
                if target is not None and target.color != self.color:
                    moves.append((newRow, newCol))

        return moves

class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color)

    def getMoves(self, board, row, col):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for drow, dcol in directions:
            r, c = row + drow, col + dcol
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                else:
                    if board[r][c].color != self.color:
                        moves.append((r, c))
                    break
                r += drow
                c += dcol

        return moves

class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color)

    def getMoves(self, board, row, col):
        moves = []
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        for drow, dcol in directions:
            r, c = row + drow, col + dcol
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None or board[r][c].color != self.color:
                    moves.append((r, c))
        return moves
        
class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color)

    def getMoves(self, board, row, col):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for drow, dcol in directions:
            r, c = row + drow, col + dcol
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                else:
                    if board[r][c].color != self.color:
                        moves.append((r, c))
                    break
                r += drow
                c += dcol

        return moves

class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color)

    def getMoves(self, board, row, col):
        rookMoves = Rook.getMoves(self, board, row, col)
        bishopMoves = Bishop.getMoves(self, board, row, col)

        return rookMoves + bishopMoves

class King(Piece):
    def __init__(self, color):
        super().__init__('king', color)
    
    def getMoves(self, board, row, col):
        moves = []
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            ( 0, -1),          ( 0, 1),
            ( 1, -1), ( 1, 0), ( 1, 1)
        ]


        for drow, dcol in directions:
            r, c = row + drow, col + dcol
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None or board[r][c].color != self.color:
                    moves.append((r, c))
        return moves


class ChessGame:
    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)]
        self.setupPieces()
        self.selectedPiece = None
        self.validMoves = []
        self.turn = 'white'
        self.gameOver = False
        self.winner = None

    
    def setupPieces(self):
        backRow = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        pieceMap = {'rook': Rook, 'knight': Knight, 'bishop': Bishop, 'queen': Queen, 'king': King, 'pawn': Pawn}

        for col in range(8):
            self.board[0][col] = pieceMap[backRow[col]]('black')
            self.board[7][col] = pieceMap[backRow[col]]('white')

            self.board[1][col] = Pawn('black')
            self.board[6][col] = Pawn('white')
    
    def findKing(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.type == 'king' and piece.color == color:
                    return (row, col)
        return None

    def isSquareAttacked(self, row, col, attackerColor):
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece.color == attackerColor:
                    if (row, col) in piece.getMoves(self.board, r, c):
                        return True
        return False

    def isInCheck(self, color):
        kingRow, kingCol = self.findKing(color)
        return self.isSquareAttacked(kingRow, kingCol, 'black' if color == 'white' else 'white')

    def getLegalMoves(self, piece, row, col):
        legal = []
        for move in piece.getMoves(self.board, row, col):
            r2, c2 = move
            captured = self.board[r2][c2]
            self.board[r2][c2], self.board[row][col] = piece, None
            if not self.isInCheck(piece.color):
                legal.append(move)
            self.board[row][col], self.board[r2][c2] = piece, captured
        return legal

    def isCheckmate(self, color):
        if not self.isInCheck(color): return False
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    if self.getLegalMoves(piece, row, col):
                        return False
        return True