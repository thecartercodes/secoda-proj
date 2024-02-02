from flask import Flask, jsonify

app = Flask(__name__)


def price_msg(name, category, price):
    return jsonify({"name": name, "category": category, "price": price})


@app.route("/onion")
def onion():
    return price_msg("onion", "vegetable", 2.09)


@app.route("/tomato")
def tomato():
    return price_msg("tomato", "vegetable", 2.29)


@app.route("/chocolate")
def chocolate():
    return price_msg("chocolate", "candy", 1.99)


@app.route("/lollipop")
def lollipop():
    return price_msg("lollipop", "candy", 1.09)


@app.route("/shirt")
def shirt():
    return price_msg("shirt", "clothing", 12.00)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5555)
