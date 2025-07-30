from cmu_graphics import *
from logic import *


"""
Citations:
https://www.w3schools.com/python/python_inheritance.asp
"""

def onAppStart(app):
    app.width = 600
    app.height = 650 
    app.boardSize = 600
    app.squareSize = app.boardSize // 8
    app.statusMessage = "White's turn"
    app.game = ChessGame()

def onKeyPress(app, key):
    if key == 'r':
        app.game = ChessGame()
        app.statusMessage = "White's turn"

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