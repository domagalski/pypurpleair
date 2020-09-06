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

    def test_measurement(self):
        # This doesn't actually do anything beyond dict keys
        measurement = self.sensor.get_measurement()
        logging.info("Sensor data:")
        logging.info(f"Sensor ID: {measurement.sensor_id}")
        logging.info(f"Timestamp: {measurement.timestamp}")
        logging.info(f"Latitude: {measurement.lat}")
        logging.info(f"Longitude: {measurement.lon}")
        logging.info(f"Place: {measurement.place}")
        logging.info(f"RSSI: {measurement.rssi}")
        logging.info(f"Uptime: {measurement.uptime}")
        logging.info(f"Temp (F): {measurement.temp_f}")
        logging.info(f"Humidity: {measurement.humidity}")
        logging.info(f"Dew Point (F): {measurement.dew_point_f}")
        logging.info(f"Pressure: {measurement.pressure}")
        logging.info(f"AQI (A): {measurement.pm2_5_aqi}")
        logging.info(f"AQI (B): {measurement.pm2_5_aqi_b}")
        logging.info(f"AQI (EPA): {measurement.pm2_5_aqi_epa}")
        logging.info(f"0.3 um/dl (A): {measurement.p_0_3_um}")
        logging.info(f"0.3 um/dl (B): {measurement.p_0_3_um_b}")
        logging.info(f"0.5 um/dl (A): {measurement.p_0_5_um}")
        logging.info(f"0.5 um/dl (B): {measurement.p_0_5_um_b}")
        logging.info(f"1.0 um/dl (A): {measurement.p_1_0_um}")
        logging.info(f"1.0 um/dl (B): {measurement.p_1_0_um_b}")
        logging.info(f"2.5 um/dl (A): {measurement.p_2_5_um}")
        logging.info(f"2.5 um/dl (B): {measurement.p_2_5_um_b}")
        logging.info(f"5.0 um/dl (A): {measurement.p_5_0_um}")
        logging.info(f"5.0 um/dl (B): {measurement.p_5_0_um_b}")
        logging.info(f"10.0 um/dl (A): {measurement.p_10_0_um}")
        logging.info(f"10.0 um/dl (B): {measurement.p_10_0_um_b}")
        logging.info(f"PM1.0_CF_ATM (A): {measurement.pm1_0_atm}")
        logging.info(f"PM1.0_CF_ATM (B): {measurement.pm1_0_atm_b}")
        logging.info(f"PM1.0_CF_1 (A): {measurement.pm1_0_cf_1}")
        logging.info(f"PM1.0_CF_1 (B): {measurement.pm1_0_cf_1_b}")
        logging.info(f"PM2.5_CF_ATM (A): {measurement.pm2_5_atm}")
        logging.info(f"PM2.5_CF_ATM (B): {measurement.pm2_5_atm_b}")
        logging.info(f"PM2.5_CF_1 (A): {measurement.pm2_5_cf_1}")
        logging.info(f"PM2.5_CF_1 (B): {measurement.pm2_5_cf_1_b}")
        logging.info(f"PM10.0_CF_ATM (A): {measurement.pm10_0_atm}")
        logging.info(f"PM10.0_CF_ATM (B): {measurement.pm10_0_atm_b}")
        logging.info(f"PM10.0_CF_1 (A): {measurement.pm10_0_cf_1}")
        logging.info(f"PM10.0_CF_1 (B): {measurement.pm10_0_cf_1_b}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
