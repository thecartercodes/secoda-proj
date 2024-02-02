from flask import Flask, jsonify
import os
import requests

app = Flask(__name__)

CMC_URL = os.environ["CMC_URL"]
CMC_API_KEY = os.environ["CMC_API_KEY"]


@app.route("/latest")
def latest():
    url = CMC_URL
    params = {"start": "1", "limit": "10", "convert": "USD"}
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}

    response = requests.get(url, params=params, headers=headers)
    return response.json()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8888)
