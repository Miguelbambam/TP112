from cmu_graphics import *

# TODO: 
# Piece classes, 
# class for ChessGame, 
# initialize it in onAppStart
# status messages

def onAppStart(app):
    app.width = 600
    app.height = 650 
    app.board_size = 600
    app.square_size = app.board_size // 8


def draw_board(app):
    for row in range(8):
        for col in range(8):
            color = rgb(220, 220, 220) if (row + col) % 2 == 0 else rgb(80, 130, 180)
            drawRect(
                col * app.square_size,
                row * app.square_size,
                app.square_size,
                app.square_size,
                fill=color
            )

            if row == 7:
                drawLabel(
                    chr(97 + col),
                    col * app.square_size + 5,
                    row * app.square_size + app.square_size - 5,
                    size=12,
                    fill='black' if color == rgb(220, 220, 220) else 'white',
                    align='left-bottom'
                )

            if col == 0:
                drawLabel(
                    str(8 - row),
                    col * app.square_size + 5,
                    row * app.square_size + 5,
                    size=12,
                    fill='black' if color == rgb(220, 220, 220) else 'white',
                    align='left-top'
                )

def redrawAll(app):
    draw_board(app)


def main():
    runApp()

main()