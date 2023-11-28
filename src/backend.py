from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Create a simple Pandas DataFrame for demonstration
data = {"Name": ["John", "Jane", "Bob"], "Age": [25, 30, 22]}
df = pd.DataFrame(data)


@app.route("/api/get_data", methods=["GET"])
def get_data():
    return jsonify(df.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)
