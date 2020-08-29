#!/usr/bin/env python3

import argparse
import logging
import time

from pypurpleair import influx
from pypurpleair import pa_lan
from pypurpleair import pa_web


def main():
    parser = argparse.ArgumentParser()
    sgroup = parser.add_mutually_exclusive_group(required=True)
    sgroup.add_argument("-l", "--lan-addr", type=str, help="Address of a LAN sensor.")
    sgroup.add_argument("-w", "--web-sensor-id", type=int, help="Web sensor ID.")
    parser.add_argument(
        "--query-interval", default=30, type=int, help="Number of seconds to wait between queries."
    )
    parser.add_argument("--lan-live", action="store_true", help="Use the live feed in LAN mode.")
    parser.add_argument("-H", "--host", type=str, default="localhost", help="InfluxDB host.")
    parser.add_argument("-P", "--port", type=int, default=8086, help="InfluxDB port.")
    parser.add_argument("-u", "--username", default="root", help="InfluxDB username.")
    parser.add_argument("-p", "--password", default="root", help="InfluxDB password.")
    parser.add_argument("-d", "--database", help="InfluxDB database.")
    parser.add_argument("-t", "--timeout", help="InfluxDB timeout.")
    parser.add_argument("--ssl", action="store_true", help="InfluxDB SSL.")
    parser.add_argument("--verify_ssl", action="store_true", help="InfluxDB verify SSL.")
    parser.add_argument("--retries", type=int, default=3, help="InfluxDB retries.")
    parser.add_argument("--use-udp", action="store_true", help="InfluxDB use UDP.")
    parser.add_argument("--udp-port", type=int, default=4444, help="InfluxDB UDP port.")
    parser.add_argument("--proxies", help="InfluxDB proxies.")
    parser.add_argument("--pool-size", type=int, default=10, help="InfluxDB pool size.")
    parser.add_argument("--path", default="", help="InfluxDB path.")
    parser.add_argument("--cert", help="InfluxDB cert path.")
    parser.add_argument("--gzip", action="store_true", help="InfluxDB use gzip.")

    kwargs = vars(parser.parse_args())
    logging.basicConfig(level=logging.INFO)

    lan_addr = kwargs.pop("lan_addr")
    lan_live = kwargs.pop("lan_live")
    web_sensor_id = kwargs.pop("web_sensor_id")
    query_interval = kwargs.pop("query_interval")

    db = influx.PurpleAirDb(**kwargs)
    if lan_addr:
        sensor = pa_lan.Sensor(lan_addr, db)
        if lan_live:
            logging.info(f"Fetching the live sensor reading from {lan_addr}.")
        else:
            logging.info(f"Fetching the average sensor reading from {lan_addr}.")
    elif web_sensor_id:
        sensor = pa_web.Sensor(web_sensor_id, db)
        logging.info(f"Fetching data from sensor: {web_sensor_id}")
    else:
        ValueError("LAN address and web sensor ID are both invalid")

    # Wait for the database to come online.
    while not db.init_database():
        time.sleep(query_interval)

    logging.info(f"Data is fetched on a {query_interval} second interval.")
    try:
        while True:
            start = time.time()
            kwargs = {}
            if lan_addr:
                kwargs["influx_measurement"] = "live" if lan_live else "average"
                kwargs["live"] = lan_live
            else:
                kwargs["influx_measurement"] = "sensors"

            try:
                sensor.query_and_write_database(**kwargs)
            # Can be caused by the web sensor
            except RuntimeError:
                pass

            elapsed = time.time() - start
            time.sleep(max(query_interval - elapsed, 0))
    except KeyboardInterrupt:
        print("")


if __name__ == "__main__":
    main()
