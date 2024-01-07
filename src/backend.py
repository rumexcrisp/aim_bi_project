from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from time import sleep

from utils import read_db, get_data, convert_to_germany_time, connect_db, simulated_energy_usage
from utils import script_dir

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

sqlite_db = f'{script_dir}/../data/db.sqlite'


@app.route("/api/get_data", methods=["GET"])
def provide_data(start=datetime(2019, 1, 1), end=datetime(2019, 2, 1)):
    conn = connect_db(sqlite_db)
    df = read_db(conn, start, end)

    if df.empty:
        print("Fehler, dataframe leer...")
        return "", 500
    return jsonify(df.to_dict(orient="records"))


def setup(force_api=False) -> None:
    start = datetime(2010, 1, 1)
    end = datetime(2023, 1, 1)

    conn = connect_db(sqlite_db)
    df_db = read_db(conn)
    if df_db.empty or force_api:
        df = get_data(start, end)

        df["marketprice"] = (df["marketprice"] * 0.1).round(2)
        df["unit"] = "Cent/kWh"
        df["date"] = df["start_timestamp"].apply(lambda epoch: convert_to_germany_time(epoch))
        print(f"db is empty: {sqlite_db}")
        print("writing to DB...")
        try:
            df.to_sql('awattar', conn, if_exists='replace', index=False)
        except Exception as e:
            print(f"Error writing to sqlite DB during setup: {e}")


if __name__ == "__main__":
    setup()
    app.run(debug=True)
