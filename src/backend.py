from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS

from utils import read_db, get_data, convert_to_germany_time, connect_db

app = Flask(__name__)
CORS(app)

sqlite_db = "'../data/db.sqlite'"

# Erstelle die Parameter für "start" und "end" in Millisekunden
# start_timestamp = int(datetime(2023, 1, 1).timestamp() * 1000)
# end_timestamp = int(datetime(2023, 1, 31).timestamp() * 1000)


@app.route("/api/get_data", methods=["GET"])
def provide_data(start=datetime(2019, 1, 1), end=datetime(2020, 1, 1)):
    conn = connect_db(sqlite_db)
    df = read_db(conn, start, end)

    if df.empty:
        print("Fehler, dataframe leer...")
        return "", 500
    return jsonify(df.to_dict(orient="records"))


def setup() -> None:
    conn = connect_db(sqlite_db)
    start = int(datetime(2010, 1, 1).timestamp() * 1000)
    end = int(datetime(2023, 1, 1).timestamp() * 1000)
    df = get_data(start, end)
    assert not df.empty

    df["marketprice"] = (df["marketprice"] * 0.1).round(2)
    df["unit"] = "Cent/kWh"
    df["date"] = df["start_timestamp"].apply(lambda epoch: convert_to_germany_time(epoch))

    df_db = read_db(conn)
    if df.equals(df_db):
        print("DB is already available and populated, nothing to save...")
        return

    try:
        df.to_sql('awattar', conn, if_exists='replace', index=False)
    except Exception as e:
        print(f"Error writing to sqlite DB during setup: {e}")


if __name__ == "__main__":
    app.run(debug=True)
