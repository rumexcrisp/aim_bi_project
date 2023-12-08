from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
import json
import pandas as pd
import requests

app = Flask(__name__)
CORS(app)

api_url = "https://api.awattar.de/v1/marketdata"
df = None

# Erstelle die Parameter für "start" und "end" in Millisekunden
start_timestamp = int(datetime(2023, 1, 1).timestamp() * 1000)
end_timestamp = int(datetime(2023, 1, 31).timestamp() * 1000)


@app.route("/api/get_data", methods=["GET"])
def get_data():
    params = {"start": start_timestamp, "end": end_timestamp}

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()

        df = pd.DataFrame(data["data"])
        df["marketprice"] = (df["marketprice"] * 0.1).round(2)
        df["unit"] = "Cent/kWh"

        # Speichere die JSON-Daten in einer Datei
        # with open('api_response.json', 'w') as json_file:
        #     json.dump(data, json_file, indent=4)
    else:
        print(f"Fehler bei der Anfrage. Statuscode: {response.status_code}")
        return "", 500
    return jsonify(df.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)
