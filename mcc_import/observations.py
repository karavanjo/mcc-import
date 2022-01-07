from io import TextIOWrapper
import logging
import csv
from zipfile import ZipFile
import glob
import re
from datetime import datetime

from pymongo import MongoClient

from mcc_import.utils import bulk_observations_insert

logger = logging.getLogger("mcc_import")


def import_observations(uri: str, cert: str):
    if cert:
        client = MongoClient(uri,
                             tls=True,
                             tlsCertificateKeyFile=cert)
    else:
        client = MongoClient(uri)

    db = client["mcc-climate"]

    db.drop_collection("observations")
    db.create_collection("observations",
                         timeseries={
                             "timeField": "ts",
                             "metaField": "source",
                             "granularity": "hours"
                         })
    c_observations = db["observations"]

    for file in glob.glob("data/observations/*.zip"):
        observation_type = file.split(".")[0].split("_")[-1]

        with ZipFile(file) as zf:
            files = zf.namelist()

            csv_file = None
            if observation_type == "k":
                csv_file = list(filter(lambda f: re.match(r"/*k_d[\d_]*.csv", f), files))[0]
            elif observation_type == "o":
                csv_file = files[0]
            elif observation_type == "s":
                csv_file = list(filter(lambda f: re.match(r"/*s_d[\d_]*.csv", f), files))[0]

            if csv_file:
                import_observations_set(zf, csv_file, observation_type, c_observations)

            zf.close()


def import_observations_set(zf, csv_file_name, observation_type, c_observations):
    with zf.open(csv_file_name, "r") as csv_file:
        csv_reader = csv.reader(TextIOWrapper(csv_file, "windows-1250"))
        next(csv_reader)
        import_observations_rows(csv_reader, c_observations, observation_type)
        csv_file.close()


def import_observations_rows(csv_reader, c_observations, observation_type):
    observations = []
    observation_maker = None

    if observation_type == "k":
        observation_maker = make_climate_observation
    elif observation_type == "o":
        observation_maker = make_precip_observation
    elif observation_type == "s":
        observation_maker = make_synop_observation

    for row in csv_reader:
        observation = observation_maker(row)
        observations.append(observation)
        bulk_observations_insert(observations, c_observations)

    bulk_observations_insert(observations, c_observations, all=True)


def make_climate_observation(row):
    return {
        "source": {
            "code": int(row[0]),
            "name": row[1],
            "type": "c"
        },
        "ts": datetime(int(row[2]), int(row[3]), int(row[4])),
        "tmax": float(row[5]) if row[5] else None,
        "tmin": float(row[7]) if row[7] else None,
        "tavg": float(row[9]) if row[9] else None,
        "precip": float(row[13]) if row[13] else None,
        "snowd": float(row[16]) if row[16] else None,
    }


def make_precip_observation(row):
    return {
        "source": {
            "code": int(row[0]),
            "name": row[1],
            "type": "p"
        },
        "ts": datetime(int(row[2]), int(row[3]), int(row[4])),
        "precip": float(row[5]) if row[5] else None,
        "snowd": float(row[8]) if row[8] else None,
        "snowfreshd": float(row[10]) if row[10] else None,
    }


def make_synop_observation(row):
    return {
        "source": {
            "code": int(row[0]),
            "name": row[1],
            "type": "s"
        },
        "ts": datetime(int(row[2]), int(row[3]), int(row[4])),
        "tmax": float(row[5]) if row[5] else None,
        "tmin": float(row[7]) if row[7] else None,
        "tavg": float(row[9]) if row[9] else None,
        "precip": float(row[13]) if row[13] else None,
        "snowd": float(row[16]) if row[16] else None,
        "raint": float(row[23]) if row[23] else None,
        "snowt": float(row[23]) if row[23] else None,
        "rainsnowt": float(row[27]) if row[27] else None,
        "cloudt": float(row[43]) if row[43] else None,
    }
