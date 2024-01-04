from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
import os

from utils import read_db, get_data, convert_to_germany_time, connect_db
from utils import script_dir

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

sqlite_db = f'{script_dir}/../data/db.sqlite'


@app.route("/api/get_data", methods=["GET"])
def provide_data(start=datetime(2019, 1, 1), end=datetime(2020, 1, 1)):
    conn = connect_db(sqlite_db)
    assert conn is not None
    df = read_db(conn, start, end)

    if df.empty:
        print("Fehler, dataframe leer...")
        return "", 500
    return jsonify(df.to_dict(orient="records"))


def setup(read_api=False) -> None:
    if read_api:
        start = datetime(2010, 1, 1).timestamp()
        end = datetime(2023, 1, 1).timestamp()
        df = get_data(start, end)
        assert not df.empty

        df["marketprice"] = (df["marketprice"] * 0.1).round(2)
        df["unit"] = "Cent/kWh"
        df["date"] = df["start_timestamp"].apply(lambda epoch: convert_to_germany_time(epoch))

    conn = connect_db(sqlite_db)
    try:
        df_db = read_db(conn)
        if read_api and df.equals(df_db):
            print("DB is already available and populated, nothing to save...")
            return
    except Exception:
        print(f"Error reading db: {sqlite_db}")
        print("writing to DB...")
        try:
            df.to_sql('awattar', conn, if_exists='replace', index=False)
        except Exception as e:
            print(f"Error writing to sqlite DB during setup: {e}")


if __name__ == "__main__":
    if os.path.exists(sqlite_db) and os.path.isfile(sqlite_db):
        setup()
    else:
        setup(read_api=False)
    app.run(debug=True)
