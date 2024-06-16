from flask import Flask, render_template, request, jsonify, send_file
import chess.svg
import chess
import io
import cairosvg
from games import ChessGame
from minimax import minimax


app = Flask(__name__)
cgame = ChessGame()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/perform_action', methods=['POST'])
def perform_action():
    move = request.json['move']
    try:
        action = chess.Move.from_uci(move)
        cgame.perform_action(action)
        response = {
            'status': 'ok',
            'fen': cgame.fen(),
            'message': 'Move successful'
        }
    except ValueError:
        response = {
            'status': 'error',
            'message': 'Invalid move'
        }
    return jsonify(response)


@app.route('/perform_search_action', methods=['POST'])
def perform_search_action():
    try:
        v, action = minimax(cgame, depth=3)
        cgame.perform_action(action)
        response = {
            'status': 'ok',
            'fen': cgame.fen(),
            'message': 'Move successful'
        }
    except ValueError:
        response = {
            'status': 'error',
            'message': 'Invalid move'
        }
    return jsonify(response)


@app.route('/reset', methods=['POST'])
def reset():
    global cgame
    cgame = ChessGame()
    response = {
        'status': 'ok',
        'message': 'Board reset',
        'fen': cgame.fen()
    }
    return jsonify(response)


@app.route('/board_image')
def board_image():
    svg_data = chess.svg.board(board=cgame).encode('utf-8')
    png_data = cairosvg.svg2png(bytestring=svg_data)
    return send_file(io.BytesIO(png_data), mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)