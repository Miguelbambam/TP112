from cmu_graphics import *

# TODO: 
# Piece classes, 
# class for ChessGame, 
# initialize it in onAppStart
# status messages

def onAppStart(app):
    app.width = 600
    app.height = 650 
    app.boardSize = 600
    app.squareSize = app.boardSize // 8
    app.statusMessage = "White's turn"


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


def main():
    runApp()

main()