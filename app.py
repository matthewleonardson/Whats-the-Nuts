from flask import Flask, jsonify, render_template, request
from treys import Deck, Evaluator, Card
from itertools import combinations

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generateboard')
def generate_board():
    deck = Deck()
    evaluator = Evaluator()
    board = tuple(deck.draw(5))

    possible_hands = list(combinations(deck.cards, 2))

    best_hands = [possible_hands[0]]
    current_best = evaluator.evaluate(possible_hands[0], tuple(board))
    for hand in possible_hands[1:]:
        hand_rank = evaluator.evaluate(hand, board)
        if hand_rank == current_best:
            best_hands.append(hand)
        elif hand_rank < current_best:
            current_best = hand_rank
            best_hands = [hand]

    response = {
        "board": board,
        "nuts": best_hands
    }

    return jsonify(response)

@app.route('/cardint')
def get_card_int():
    card1 = request.args.get('card1').capitalize()
    card2 = request.args.get('card2').capitalize()
    
    return jsonify({
        'card1': Card.new(card1),
        'card2': Card.new(card2) 
    })

app.run()