#!/usr/bin/env python3

import logging
import pathlib
import unittest
from unittest import mock

from pypurpleair import pa_web

GOLDEN_DATA = pathlib.Path(__file__).parent / "data" / "web.json"


def _load_golden_data(*args, **kwargs) -> str:
    with GOLDEN_DATA.open() as f:
        json_str = f.read()
    return json_str.strip()


@mock.patch("pypurpleair.pa_web.Sensor._make_request", _load_golden_data)
class PurpleAirLanTest(unittest.TestCase):
    def setUp(self):
        self.sensor = pa_web.Sensor(0)

    def test_sensor_query(self):
        sensor_dict = self.sensor.query_sensor()
        self.assertIsNotNone(sensor_dict)

        self.assertIn("results", sensor_dict)
        self.assertEqual(len(sensor_dict["results"]), 2)

    def test_sensor_reading(self):
        # The web API automatically encodes a lot of floats as strings for some reason
        sensor_reading = self.sensor.get_sensor_reading()
        self.assertFalse(isinstance(sensor_reading.lat, str))
        self.assertFalse(isinstance(sensor_reading.lon, str))
        self.assertIsNotNone(sensor_reading.place)
        self.assertFalse(isinstance(sensor_reading.rssi, str))
        self.assertIsNotNone(sensor_reading.rssi)
        self.assertFalse(isinstance(sensor_reading.temp_f, str))
        self.assertIsNotNone(sensor_reading.temp_f)
        self.assertFalse(isinstance(sensor_reading.humidity, str))
        self.assertIsNotNone(sensor_reading.humidity)
        self.assertFalse(isinstance(sensor_reading.pressure, str))
        self.assertIsNotNone(sensor_reading.pressure)
        self.assertFalse(isinstance(sensor_reading.pm2_5_aqi, str))
        self.assertFalse(isinstance(sensor_reading.pm2_5_aqi_b, str))
        self.assertIsNotNone(sensor_reading.pm2_5_aqi_b)
        self.assertFalse(isinstance(sensor_reading.p_0_3_um, str))
        self.assertFalse(isinstance(sensor_reading.p_0_3_um_b, str))
        self.assertIsNotNone(sensor_reading.p_0_3_um_b)
        self.assertFalse(isinstance(sensor_reading.p_0_5_um, str))
        self.assertFalse(isinstance(sensor_reading.p_0_5_um_b, str))
        self.assertIsNotNone(sensor_reading.p_0_5_um_b)
        self.assertFalse(isinstance(sensor_reading.p_1_0_um, str))
        self.assertFalse(isinstance(sensor_reading.p_1_0_um_b, str))
        self.assertIsNotNone(sensor_reading.p_1_0_um_b)
        self.assertFalse(isinstance(sensor_reading.p_2_5_um, str))
        self.assertFalse(isinstance(sensor_reading.p_2_5_um_b, str))
        self.assertIsNotNone(sensor_reading.p_2_5_um_b)
        self.assertFalse(isinstance(sensor_reading.p_5_0_um, str))
        self.assertFalse(isinstance(sensor_reading.p_5_0_um_b, str))
        self.assertIsNotNone(sensor_reading.p_5_0_um_b)
        self.assertFalse(isinstance(sensor_reading.p_10_0_um, str))
        self.assertFalse(isinstance(sensor_reading.p_10_0_um_b, str))
        self.assertIsNotNone(sensor_reading.p_10_0_um_b)
        self.assertFalse(isinstance(sensor_reading.pm1_0_atm, str))
        self.assertFalse(isinstance(sensor_reading.pm1_0_atm_b, str))
        self.assertIsNotNone(sensor_reading.pm1_0_atm_b)
        self.assertFalse(isinstance(sensor_reading.pm1_0_cf_1, str))
        self.assertFalse(isinstance(sensor_reading.pm1_0_cf_1_b, str))
        self.assertIsNotNone(sensor_reading.pm1_0_cf_1_b)
        self.assertFalse(isinstance(sensor_reading.pm2_5_atm, str))
        self.assertFalse(isinstance(sensor_reading.pm2_5_atm_b, str))
        self.assertIsNotNone(sensor_reading.pm2_5_atm_b)
        self.assertFalse(isinstance(sensor_reading.pm2_5_cf_1, str))
        self.assertFalse(isinstance(sensor_reading.pm2_5_cf_1_b, str))
        self.assertIsNotNone(sensor_reading.pm2_5_cf_1_b)
        self.assertFalse(isinstance(sensor_reading.pm2_5_atm, str))
        self.assertFalse(isinstance(sensor_reading.pm2_5_atm_b, str))
        self.assertIsNotNone(sensor_reading.pm2_5_atm_b)
        self.assertFalse(isinstance(sensor_reading.pm2_5_cf_1, str))
        self.assertFalse(isinstance(sensor_reading.pm2_5_cf_1_b, str))
        self.assertIsNotNone(sensor_reading.pm2_5_cf_1_b)
        self.assertFalse(isinstance(sensor_reading.pm10_0_atm, str))
        self.assertFalse(isinstance(sensor_reading.pm10_0_atm_b, str))
        self.assertIsNotNone(sensor_reading.pm10_0_atm_b)
        self.assertFalse(isinstance(sensor_reading.pm10_0_cf_1, str))
        self.assertFalse(isinstance(sensor_reading.pm10_0_cf_1_b, str))
        self.assertIsNotNone(sensor_reading.pm10_0_cf_1_b)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
