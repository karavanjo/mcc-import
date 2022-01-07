import logging
import csv

from pymongo import MongoClient

logger = logging.getLogger("mcc_import")


def import_stations(uri: str, cert: str):
    codes_info = get_full_codes_from_file()

    if cert:
        client = MongoClient(uri,
                             tls=True,
                             tlsCertificateKeyFile=cert)
    else:
        client = MongoClient(uri)

    db = client["mcc-climate"]
    c_stations = db["stations"]

    c_stations.drop()

    with open("data/stations/stations.csv") as csv_file:
        csv_reader = csv.reader(csv_file, dialect="excel")
        next(csv_reader)

        stations = []

        for row in csv_reader:
            short_code = row[0]
            full_code = codes_info[short_code]

            station = {
                "code": full_code,
                "short_code": row[0],
                "name": row[1],
                "river": row[8],
                "type": row[9],
                "location": {
                    "type": "Point",
                    "coordinates": [float(row[10]), float(row[11])]
                }
            }
            stations.append(station)

        c_stations.insert_many(stations)
        logger.info(f"{len(stations)} stations imported")
        stations.clear()

    doc_count = c_stations.count_documents({})
    logger.info(f"Stations import process is finished. {doc_count} stations were imported.")


def get_full_codes_from_file():
    codes_info = {}

    with open("data/stations/wykaz_stacji.csv", encoding="windows-1250") as csv_file:
        csv_reader = csv.reader(csv_file, dialect="excel")
        for row in csv_reader:
            codes_info[row[2].strip()] = row[0].strip()

    return codes_info
