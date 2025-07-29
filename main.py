from cmu_graphics import *


"""
Citations:
https://www.w3schools.com/python/python_inheritance.asp
"""

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
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                    break
                else:
                    if board[r][c].color != self.color:
                        moves.append((r, c))
                    break
                r += drow
                c += dcol

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
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                    break
                else:
                    if board[r][c].color != self.color:
                        moves.append((r, c))
                    break
                r += drow
                c += dcol

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

def onAppStart(app):
    app.width = 600
    app.height = 650 
    app.boardSize = 600
    app.squareSize = app.boardSize // 8
    app.statusMessage = "White's turn"
    app.game = ChessGame()

def onMousePress(app, x, y):
    row = y // app.squareSize
    col = x // app.squareSize

    if row >= 8 or col >= 8 or app.game.gameOver == True: return

    board = app.game.board
    selected = app.game.selectedPiece
    validMoves = app.game.validMoves
    game = app.game

    if selected and (row, col) in validMoves:
        startRow, startCol = selected
        piece = board[startRow][startCol]
        board[row][col], board[startRow][startCol] = piece, None
        piece.hasMoved = True
        piece.position = (row, col)
        game.selectedPiece = None
        game.validMoves = []
        game.turn = 'black' if game.turn == 'white' else 'white'

        if game.isInCheck(game.turn):
            if game.isCheckmate(game.turn):
                game.gameOver = True
                game.winner = 'white' if game.turn == 'black' else 'black'
                app.statusMessage = f"Checkmate! {game.winner.capitalize()} wins!"
            else:
                app.statusMessage = f"{game.turn.capitalize()} is in check!"
        else:
            app.statusMessage = f"{game.turn.capitalize()}'s turn"
        return

    piece = board[row][col]
    if piece and piece.color == game.turn:
        game.selectedPiece = (row, col)
        game.validMoves = game.getLegalMoves(piece, row, col)
    else:
        game.selectedPiece = None
        game.validMoves = []

def drawPieces(app):
    for r in range(8):
        for c in range(8):
            piece = app.game.board[r][c]
            if piece is not None:
                x = c * app.squareSize + app.squareSize // 2
                y = r * app.squareSize + app.squareSize // 2
                color = 'black' if piece.color == 'black' else 'white'

                pieces = {
                    'king': 'pieces/wk.png' if color == 'white' else 'pieces/bk.png',
                    'queen': 'pieces/wq.png' if color == 'white' else 'pieces/bq.png',
                    'rook': 'pieces/wr.png' if color == 'white' else 'pieces/br.png',
                    'bishop': 'pieces/wb.png' if color == 'white' else 'pieces/bb.png',
                    'knight': 'pieces/wn.png' if color == 'white' else 'pieces/bn.png',
                    'pawn': 'pieces/wp.png' if color == 'white' else 'pieces/bp.png'
                }

                pieceImage = pieces.get(piece.type, '?')
                drawImage(pieceImage, x, y, width=app.squareSize, height=app.squareSize, align='center')


def drawBoard(app):
    for row in range(8):
        for col in range(8):
            color = rgb(220, 220, 220) if (row + col) % 2 == 0 else rgb(80, 130, 180)
            drawRect(
                col * app.squareSize,
                row * app.squareSize,
                app.squareSize,
                app.squareSize,
                fill=color
            )

            if row == 7:
                drawLabel(
                    chr(97 + col),
                    col * app.squareSize + 5,
                    row * app.squareSize + app.squareSize - 5,
                    size=12,
                    fill='black' if color == rgb(220, 220, 220) else 'white',
                    align='left-bottom'
                )

            if col == 0:
                drawLabel(
                    str(8 - row),
                    col * app.squareSize + 5,
                    row * app.squareSize + 5,
                    size=12,
                    fill='black' if color == rgb(220, 220, 220) else 'white',
                    align='left-top'
                )
    
    if app.game.selectedPiece is not None:
        r, c = app.game.selectedPiece
        drawRect(c * app.squareSize, r * app.squareSize, app.squareSize, app.squareSize,
                 fill=None, border='yellow', borderWidth=3)

    for (r, c) in app.game.validMoves:
        drawRect(c * app.squareSize, r * app.squareSize, app.squareSize, app.squareSize,
                 fill=None, border='green', borderWidth=3)

def drawStatus(app):
    drawRect(0, app.boardSize, app.width, 50, fill='lightGray')
    drawLabel(app.statusMessage, app.width // 2, app.boardSize + 20, size=20, bold=True)
    drawLabel("Press 'r' to reset", app.width // 2, app.boardSize + 40, size=14, bold=True)

def redrawAll(app):
    drawBoard(app)
    drawStatus(app)
    drawPieces(app)


def main():
    runApp()

main()