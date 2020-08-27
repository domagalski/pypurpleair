#!/usr/bin/env python3

import logging
import pathlib
import unittest
from unittest import mock

from pypurpleair import pa_lan

GOLDEN_DATA = pathlib.Path(__file__).parent / "data" / "lan.json"


def _load_golden_data(*args, **kwargs) -> str:
    with GOLDEN_DATA.open() as f:
        json_str = f.read()
    return json_str.strip()


@mock.patch("pypurpleair.pa_lan.Sensor._make_request", _load_golden_data)
class PurpleAirLanTest(unittest.TestCase):
    def setUp(self):
        self.sensor = pa_lan.Sensor("127.0.0.1")

    def test_sensor_query(self):
        sensor_dict = self.sensor.query_sensor()
        self.assertIsNotNone(sensor_dict)

        # This is potentially useful in case I ever update the golden data
        self.assertIn("SensorId", sensor_dict)
        self.assertIn("pm2.5_aqi", sensor_dict)
        self.assertIn("pm2.5_aqi_b", sensor_dict)

    def test_sensor_reading(self):
        # This doesn't actually do anything beyond dict keys
        sensor_reading = self.sensor.get_sensor_reading()
        logging.info("Sensor data:")
        logging.info(f"Sensor ID: {sensor_reading.sensor_id}")
        logging.info(f"Timestamp: {sensor_reading.timestamp}")
        logging.info(f"Latitude: {sensor_reading.lat}")
        logging.info(f"Longitude: {sensor_reading.lon}")
        logging.info(f"Place: {sensor_reading.place}")
        logging.info(f"RSSI: {sensor_reading.rssi}")
        logging.info(f"Temp (F): {sensor_reading.temp_f}")
        logging.info(f"Humidity: {sensor_reading.humidity}")
        logging.info(f"Dew Point (F): {sensor_reading.dew_point_f}")
        logging.info(f"Pressure: {sensor_reading.pressure}")
        logging.info(f"AQI (A): {sensor_reading.pm2_5_aqi}")
        logging.info(f"AQI (B): {sensor_reading.pm2_5_aqi_b}")
        logging.info(f"0.3 um/dl (A): {sensor_reading.p_0_3_um}")
        logging.info(f"0.3 um/dl (B): {sensor_reading.p_0_3_um_b}")
        logging.info(f"0.5 um/dl (A): {sensor_reading.p_0_5_um}")
        logging.info(f"0.5 um/dl (B): {sensor_reading.p_0_5_um_b}")
        logging.info(f"1.0 um/dl (A): {sensor_reading.p_1_0_um}")
        logging.info(f"1.0 um/dl (B): {sensor_reading.p_1_0_um_b}")
        logging.info(f"2.5 um/dl (A): {sensor_reading.p_2_5_um}")
        logging.info(f"2.5 um/dl (B): {sensor_reading.p_2_5_um_b}")
        logging.info(f"5.0 um/dl (A): {sensor_reading.p_5_0_um}")
        logging.info(f"5.0 um/dl (B): {sensor_reading.p_5_0_um_b}")
        logging.info(f"10.0 um/dl (A): {sensor_reading.p_10_0_um}")
        logging.info(f"10.0 um/dl (B): {sensor_reading.p_10_0_um_b}")
        logging.info(f"PM1.0_CF_ATM (A): {sensor_reading.pm1_0_atm}")
        logging.info(f"PM1.0_CF_ATM (B): {sensor_reading.pm1_0_atm_b}")
        logging.info(f"PM1.0_CF_1 (A): {sensor_reading.pm1_0_cf_1}")
        logging.info(f"PM1.0_CF_1 (B): {sensor_reading.pm1_0_cf_1_b}")
        logging.info(f"PM2.5_CF_ATM (A): {sensor_reading.pm2_5_atm}")
        logging.info(f"PM2.5_CF_ATM (B): {sensor_reading.pm2_5_atm_b}")
        logging.info(f"PM2.5_CF_1 (A): {sensor_reading.pm2_5_cf_1}")
        logging.info(f"PM2.5_CF_1 (B): {sensor_reading.pm2_5_cf_1_b}")
        logging.info(f"PM10.0_CF_ATM (A): {sensor_reading.pm10_0_atm}")
        logging.info(f"PM10.0_CF_ATM (B): {sensor_reading.pm10_0_atm_b}")
        logging.info(f"PM10.0_CF_1 (A): {sensor_reading.pm10_0_cf_1}")
        logging.info(f"PM10.0_CF_1 (B): {sensor_reading.pm10_0_cf_1_b}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()