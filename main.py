from cmu_graphics import *


"""
Citations:
https://www.w3schools.com/python/python_inheritance.asp
"""

class Piece:
    def __init__(self, type, color):
        self.type = type
        self.color = color

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

class ChessGame:
    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)]
        self.setupPieces()
        self.selectedPiece = None
        self.validMoves = []

    
    def setupPieces(self):
        backRow = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for col in range(8):
            self.board[1][col] = Pawn('black')
            self.board[6][col] = Pawn('white')
        
        for piece in range(len(backRow)):
            self.board[0][piece] = Piece(backRow[piece], 'black')
            self.board[7][piece] = Piece(backRow[piece], 'white')

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

    if row >= 8 or col >= 8: return

    board = app.game.board
    selected = app.game.selectedPiece
    validMoves = app.game.validMoves

    if selected and (row, col) in validMoves:
        ogRow, ogCol = selected
        board[row][col] = board[ogRow][ogCol]
        board[ogRow][ogCol] = None
        app.game.selectedPiece = None
        app.game.validMoves = []
        app.statusMessage = "Black's turn" if app.statusMessage.startswith("White") else "White's turn"
        return

    piece = board[row][col]
    if piece and piece.type == 'pawn':
        moves = piece.getMoves(board, row, col)
        app.game.selectedPiece = (row, col)
        app.game.validMoves = moves
    else:
        app.game.selectedPiece = None
        app.game.validMoves = []

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