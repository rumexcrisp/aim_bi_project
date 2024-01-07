from datetime import datetime, timezone
import json
import pandas as pd
import numpy as np
import requests
import time
import pytz
import sqlite3
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))


def connect_db(db) -> sqlite3.Connection | None:
    """return db handle

    Args:
        db (string): path to sql file

    Returns:
        sqlite3.Connection | None: db handle
    """
    try:
        return sqlite3.connect(db)
    except Exception as e:
        print(f"[connect_db] Error connection to db: {e}", file=sys.stderr)
        return None


def get_data(start=datetime(2010, 1, 1), end=datetime(2023, 1, 1)) -> pd.DataFrame:
    """get data from awattar

    Args:
        start (datetime): datetime object
        end (datetime): datetime object

    Returns:
        pd.DataFrame: dataframe containing data
    """
    api_url = "https://api.awattar.de/v1/marketdata"
    df = pd.DataFrame()

    start_timestamp = int(start.timestamp() * 1000)
    end_timestamp = int(end.timestamp() * 1000)

    params = {
        'start': start_timestamp,
        'end': end_timestamp
    }

    print("Trying to get data from awattar api")

    start_time = time.time()
    response = requests.get(api_url, params=params)
    end_time = time.time()

    print(f"took {end_time - start_time:.6f} seconds to execute.")

    if response.status_code == 200:
        data = response.json()

        with open(f'{script_dir}/../data/api_response_{start}_{end}.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

        return pd.DataFrame(data["data"])
    else:
        print(f"Fehler bei der Anfrage. Statuscode: {response.status_code}")
        return df


def convert_to_germany_time(epoch) -> str:
    """converts input epoch to german time string

    Args:
        epoch (int): epoch in ms

    Returns:
        str: german time string
    """
    germany_timezone = pytz.timezone("Europe/Berlin")
    dt_utc = datetime.fromtimestamp(epoch / 1000, tz=timezone.utc)
    dt_germany = dt_utc.replace(tzinfo=pytz.utc).astimezone(germany_timezone)
    return dt_germany.strftime('%d-%m-%Y %H:%M:%S %Z')


def read_db(conn, start=datetime(1970, 1, 1, 1), end=datetime(1970, 1, 1, 1)) -> pd.DataFrame | None:
    """read data from sqlite db, returns whole db if start and end are default

    Args:
        conn (sqlite3.connect): sqlite3 db
        start (time.datetime, optional): start time. Defaults to datetime(1970, 1, 1, 1).
        end (time.datetime, optional): end time. Defaults to datetime(1970, 1, 1, 1).

    Returns:
        pd.DataFrame | None: _description_
    """
    print(f"[read_db] start: {start}, end: {end}")
    start = int(start.timestamp() * 1000)
    end = int(end.timestamp() * 1000)
    print(f"[read_db] start: {start}, end: {end}")
    df_db = pd.DataFrame()
    start_time = time.time()
    try:
        df_db = pd.read_sql('select * from awattar', conn)
    except Exception as e:
        print(f"[read_db] Error reading db: {e}")
        return pd.DataFrame()
    print(f"[read_db] db read took {(time.time()) - start_time:.6f} seconds to execute.")
    if start == 0 and end == 0:
        return df_db
    elif start <= end:
        print("[read_db] start <= end")
        df_db = df_db[(df_db['start_timestamp'] >= start) & (df_db['start_timestamp'] < end)]
        return (df_db)


def simulated_energy_usage(total_daily_energy=11, num_hours=24) -> np.ndarray:
    # Create an array representing the hours of the day
    hours = np.arange(num_hours)

    energy_usage = total_daily_energy * (
        0.6 * np.exp(-0.5 * ((hours - 6) / 2.0) ** 2) +
        0.5 * np.exp(-0.5 * ((hours - 12) / 2.0) ** 2) +
        0.7 * np.exp(-0.5 * ((hours - 18) / 2.0) ** 2)
    )

    # Ensure the energy usage is non-negative
    energy_usage = np.maximum(energy_usage, 0)

    # Normalize the energy usage to the total daily energy
    energy_usage = total_daily_energy * (energy_usage / np.sum(energy_usage))

    return energy_usage
