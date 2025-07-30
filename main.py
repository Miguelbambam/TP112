from cmu_graphics import *
from logic import *
import json


"""
Citations:
https://www.w3schools.com/python/python_inheritance.asp
https://www.w3schools.com/python/python_json.asp
Chess.com for piece images
"""

def loadUsers():
    with open("users.json", "r") as f:
        return json.load(f)

def onAppStart(app):
    app.width = 600
    app.height = 650 
    app.boardSize = 600
    app.squareSize = app.boardSize // 8
    
    app.screen = 'home'
    app.users = loadUsers()
    app.selectedWhite = None
    app.selectedBlack = None
    app.statusMessage = ""
    app.game = None

def onKeyPress(app, key):
    if key == 'r' and app.screen == 'game':
        app.game = ChessGame()
        app.statusMessage = f"{app.users[app.selectedWhite]['name']} (White) vs {app.users[app.selectedBlack]['name']} (Black)"
    
    elif app.screen == 'home' and key == 'enter':
        if app.selectedWhite is not None and app.selectedBlack is not None:
            app.game = ChessGame()
            app.statusMessage = f"{app.users[app.selectedWhite]['name']} (White) vs {app.users[app.selectedBlack]['name']} (Black)"
            app.screen = 'game'

def onMousePress(app, x, y):
    if app.screen == 'home':
        yStart = 100
        index = 0
        for user in app.users:
            boxY = yStart + index * 60
            if 150 <= x <= 450 and (boxY - 25) <= y <= (boxY + 25):
                if app.selectedWhite is None:
                    app.selectedWhite = index
                elif app.selectedBlack is None and index != app.selectedWhite:
                    app.selectedBlack = index
            index += 1
        return

    if app.screen != 'game':
        return

    row = y // app.squareSize
    col = x // app.squareSize

    if row >= 8 or col >= 8 or app.game.gameOver == True: return

    game = app.game
    board = game.board
    selected = game.selectedPiece
    validMoves = game.validMoves


    if selected and (row, col) in validMoves:
        startRow, startCol = selected
        piece = board[startRow][startCol]
        board[row][col], board[startRow][startCol] = piece, None
        piece.hasMoved = True
        piece.position = (row, col)

        if piece.type == 'king' and abs(col - startCol) == 2:
            if col == 6:
                board[row][5] = board[row][7]
                board[row][7] = None
                board[row][5].hasMoved = True
            elif col == 2:
                board[row][3] = board[row][0]
                board[row][0] = None
                board[row][3].hasMoved = True

        if piece.type == 'pawn' and (row == 0 or row == 7):
            board[row][col] = Queen(piece.color)

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
        elif game.isStalemate(game.turn):
                game.gameOver = True
                game.winner = None
                app.statusMessage = "Stalemate! It's a draw."
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
        if app.game.board[r][c] is None:
            drawCircle((c * app.squareSize) + app.squareSize//2, (r * app.squareSize) + app.squareSize//2,
                       app.squareSize//6, fill='gold')
        else:
            drawRect(c * app.squareSize, r * app.squareSize, app.squareSize, app.squareSize,
                     fill=None, border='red', borderWidth=3)

def drawStatus(app):
    drawRect(0, app.boardSize, app.width, 50, fill='lightGray')
    drawLabel(app.statusMessage, app.width // 2, app.boardSize + 20, size=20, bold=True)
    drawLabel("Press 'r' to reset", app.width // 2, app.boardSize + 40, size=14, bold=True)

def drawHomeScreen(app):
    drawLabel("Select White and Black Players", app.width // 2, 40, size=24, bold=True)

    yStart = 100
    index = 0
    for user in app.users:
        y = yStart + index * 60
        boxColor = 'white'
        if app.selectedWhite == index:
            boxColor = 'lightyellow'
        elif app.selectedBlack == index:
            boxColor = 'lightblue'

        drawRect(150, y - 25, 300, 50, fill=boxColor, border='black')
        drawLabel(f"{user['name']} (ELO: {user['elo']})", app.width // 2, y, size=20)
        index += 1

    if app.selectedWhite is None:
        drawLabel("Click to select WHITE player", app.width // 2, 500, size=16, italic=True)
    elif app.selectedBlack is None:
        drawLabel("Click to select BLACK player", app.width // 2, 500, size=16, italic=True)
    else:
        drawLabel("Press ENTER to start the game", app.width // 2, 500, size=16, italic=True)



def redrawAll(app):
    if app.screen == 'home':
        drawHomeScreen(app)
    elif app.screen == 'game':
        drawBoard(app)
        drawStatus(app)
        drawPieces(app)


def main():
    runApp()

main()