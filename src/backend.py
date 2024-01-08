from datetime import datetime, timezone
from flask import Flask, jsonify, request
from flask_cors import CORS

from utils import read_db, get_data, convert_to_germany_time, connect_db, simulated_energy_usage
from utils import script_dir

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

sqlite_db = f'{script_dir}/../data/db.sqlite'


@app.route("/api/get_data", methods=["GET"])
def provide_data(start=datetime(2019, 1, 1), end=datetime(2019, 2, 1)):
    """Response to a http GET request with data if available

    Args:
        start (datetime, optional): Start date. Defaults to datetime(2019, 1, 1).
        end (datetime, optional): End date. Defaults to datetime(2019, 2, 1).

    Returns:
        _type_: _description_
    """
    start_epoch = int(request.args.get('start'))
    end_epoch = int(request.args.get('end'))
    start = datetime.fromtimestamp(start_epoch / 1000.0, tz=timezone.utc)
    end = datetime.fromtimestamp(end_epoch / 1000.0, tz=timezone.utc)

    print(f"[provide_data] Request with:\n  start: {start_epoch}\n  end: {end_epoch}\n  converted to: {start} - {end}")

    conn = connect_db(sqlite_db)
    df = read_db(conn, start, end, 100)

    if df.empty:
        print("Error, dataframe empty...")
        return "", 500
    return jsonify(df.to_dict(orient="records")), 200


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
