from cmu_graphics import *
from logic import *
import json


"""
Citations:
https://www.w3schools.com/python/python_inheritance.asp
https://www.w3schools.com/python/python_json.asp
https://www.w3schools.com/python/python_ref_string.asp
https://en.wikipedia.org/wiki/Elo_rating_system
Chess.com for piece images
"""

def loadUsers():
    with open("users.json", "r") as f:
        return json.load(f)

def saveUsers(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

def calculateElo(ratingA, ratingB, scoreA, K=20):
    expectedA = 1 / (1 + 10 ** ((ratingB - ratingA) / 400))
    ratingANew = ratingB + K * (scoreA - expectedA)
    return int(ratingANew)



def onAppStart(app):
    app.width = 600
    app.height = 700 
    app.boardSize = 600
    app.squareSize = app.boardSize // 8
    
    app.screen = 'home'
    app.users = loadUsers()
    app.selectedWhite = None
    app.selectedBlack = None
    app.statusMessage = ""
    app.game = None

    app.creatingUser = False
    app.newUserName = ""

    app.isFlipped = False

def getDisplayCoords(app, row, col):
    if app.isFlipped:
        return 7 - row, 7 - col
    return row, col

def updateEloAfterGame(app):
    whiteIndex = app.selectedWhite
    blackIndex = app.selectedBlack
    whiteUser = app.users[whiteIndex]
    blackUser = app.users[blackIndex]

    if app.game.winner == 'white':
        scoreWhite, scoreBlack = 1, 0
        resultMessage = f"{whiteUser['name']} (White) wins!"
    elif app.game.winner == 'black':
        scoreWhite, scoreBlack = 0, 1
        resultMessage = f"{blackUser['name']} (Black) wins!"
    else:
        scoreWhite = scoreBlack = 0.5
        resultMessage = "It's a draw!"

    newWhiteElo = calculateElo(whiteUser['elo'], blackUser['elo'], scoreWhite)
    newBlackElo = calculateElo(blackUser['elo'], whiteUser['elo'], scoreBlack)

    whiteUser['elo'] = newWhiteElo
    blackUser['elo'] = newBlackElo

    saveUsers(app.users)

    app.statusMessage = f"Game Over! {resultMessage} New ELOs - {whiteUser['name']}: {newWhiteElo}, {blackUser['name']}: {newBlackElo}"


def onKeyPress(app, key):
    if key == 'r' and app.screen == 'game':
        app.game = ChessGame()
        app.selectedWhite, app.selectedBlack = app.selectedBlack, app.selectedWhite
        app.statusMessage = f"{app.users[app.selectedWhite]['name']} (White) vs {app.users[app.selectedBlack]['name']} (Black)"
        app.isFlipped = False
    
    elif app.screen == 'home' and key == 'enter':
        if app.selectedWhite is not None and app.selectedBlack is not None:
            app.game = ChessGame()
            app.statusMessage = f"{app.users[app.selectedWhite]['name']} (White) vs {app.users[app.selectedBlack]['name']} (Black)"
            app.screen = 'game'
            app.isFlipped = False
    
    if app.creatingUser:
        if key == 'enter' and app.newUserName.strip() != "":
            name = app.newUserName.strip()

            for user in app.users:
                if user['name'].lower() == name.lower():
                    return

            if len(app.users) >= 7:
                return

            newUser = {
                "name": name,
                "elo": 1200
            }
            app.users.append(newUser)
            saveUsers(app.users)
            app.creatingUser = False
            app.newUserName = ""

        elif key == 'backspace':
            app.newUserName = app.newUserName[:-1]
        elif len(key) == 1 and key.isprintable():
            app.newUserName += key

def onMousePress(app, x, y):
    if app.screen == 'home':
        yStart = 100

        for i in range(len(app.users)):
            boxY = yStart + i * 60
            if 150 <= x <= 450 and (boxY - 25) <= y <= (boxY + 25):
                if app.selectedWhite is None:
                    app.selectedWhite = i
                elif app.selectedBlack is None and i != app.selectedWhite:
                    app.selectedBlack = i
       
        for i in range(len(app.users)):
            boxY = yStart + i * 60
            if 460 <= x <= 490 and (boxY - 15) <= y <= (boxY + 15):
                if app.selectedWhite == i:
                    app.selectedWhite = None
                elif app.selectedBlack == i:
                    app.selectedBlack = None
                app.users.pop(i)
                saveUsers(app.users)
                return

        if 200 <= x <= 400 and 580 <= y <= 620:
            app.creatingUser = True
            app.newUserName = ""
            return
        return

    if app.screen != 'game':
        return
    
    if 10 <= x <= 90 and app.boardSize + 50 <= y <= app.boardSize + 90:
        if app.game.gameOver: return
        app.game.gameOver = True
        app.game.winner = 'black' if app.game.turn == 'white' else 'white'
        updateEloAfterGame(app)

    if app.width - 90 <= x <= app.width - 10 and app.boardSize + 50 <= y <= app.boardSize + 90:
        if app.game.gameOver: return
        app.game.gameOver = True
        app.game.winner = None
        updateEloAfterGame(app)


    row = y // app.squareSize
    col = x // app.squareSize
    
    if app.isFlipped:
        row = 7 - row
        col = 7 - col

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
        app.isFlipped = (game.turn == 'black')

        if game.isInCheck(game.turn):
            if game.isCheckmate(game.turn):
                game.gameOver = True
                game.winner = 'white' if game.turn == 'black' else 'black'
                updateEloAfterGame(app)
            else:
                app.statusMessage = f"{game.turn.capitalize()} is in check!"
        elif game.isStalemate(game.turn):
                game.gameOver = True
                game.winner = None
                updateEloAfterGame(app)
        else:
            app.statusMessage = f"{game.turn.capitalize()}'s turn"

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
                dr, dc = getDisplayCoords(app, r, c)
                x = dc * app.squareSize + app.squareSize // 2
                y = dr * app.squareSize + app.squareSize // 2
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
            dr, dc = getDisplayCoords(app, row, col)
            color = rgb(220, 220, 220) if (row + col) % 2 == 0 else rgb(80, 130, 180)
            drawRect(
                dc * app.squareSize,
                dr * app.squareSize,
                app.squareSize,
                app.squareSize,
                fill=color
            )

            if dr == 7:
                drawLabel(
                    chr(97 + col),
                    dc * app.squareSize + 5,
                    dr * app.squareSize + app.squareSize - 5,
                    size=12,
                    fill='black' if color == rgb(220, 220, 220) else 'white',
                    align='left-bottom'
                )

            if dc == 0:
                drawLabel(
                    str(8 - row),
                    dc * app.squareSize + 5,
                    dr * app.squareSize + 5,
                    size=12,
                    fill='black' if color == rgb(220, 220, 220) else 'white',
                    align='left-top'
                )
    
    if app.game.selectedPiece is not None:
        r, c = app.game.selectedPiece
        dr, dc = getDisplayCoords(app, r, c)
        drawRect(dc * app.squareSize, dr * app.squareSize, app.squareSize, app.squareSize,
                 fill=None, border='yellow', borderWidth=3)

    for (r, c) in app.game.validMoves:
        dr, dc = getDisplayCoords(app, r, c)
        if app.game.board[r][c] is None:
            drawCircle((dc * app.squareSize) + app.squareSize//2, (dr * app.squareSize) + app.squareSize//2,
                       app.squareSize//6, fill='gold')
        else:
            drawRect(dc * app.squareSize, dr * app.squareSize, app.squareSize, app.squareSize,
                     fill=None, border='red', borderWidth=3)

def drawStatus(app):
    drawRect(0, app.boardSize, app.width, 100, fill='lightGray')
    drawLabel(app.statusMessage, app.width // 2, app.boardSize + 30, size=16, bold=True)
    drawLabel("Press 'r' to reset", app.width // 2, app.boardSize + 60, size=14, bold=True)

    drawRect(10, app.boardSize + 50, 80, 40, fill='red', border='black')
    drawLabel("Resign", 50, app.boardSize + 70, size=14, fill='white', bold=True)

    drawRect(app.width - 90, app.boardSize + 50, 80, 40, fill='orange', border='black')
    drawLabel("Draw", app.width - 50, app.boardSize + 70, size=14, fill='white', bold=True)

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

        drawRect(460, y - 15, 30, 30, fill='red')
        drawLabel('X', 475, y, size=16, fill='white')

        index += 1

    if app.selectedWhite is None:
        drawLabel("Click to select WHITE player", app.width // 2, 500, size=16, italic=True)
    elif app.selectedBlack is None:
        drawLabel("Click to select BLACK player", app.width // 2, 500, size=16, italic=True)
    else:
        drawLabel("Press ENTER to start the game", app.width // 2, 500, size=16, italic=True)
    
    drawRect(200, 580, 200, 40, fill='lightgreen', border='black')
    drawLabel("Create New User", 300, 600, size=16, bold=True)

    if app.creatingUser:
        drawRect(150, 530, 300, 40, fill='white', border='black')
        drawLabel(f"Enter name: {app.newUserName}", 300, 550, size=16)



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