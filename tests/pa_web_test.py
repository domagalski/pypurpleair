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

    def test_measurement(self):
        # The web API automatically encodes a lot of floats as strings for some reason
        measurement = self.sensor.get_measurement()
        self.assertFalse(isinstance(measurement.lat, str))
        self.assertFalse(isinstance(measurement.lon, str))
        self.assertIsNotNone(measurement.place)
        self.assertFalse(isinstance(measurement.rssi, str))
        self.assertIsNotNone(measurement.rssi)
        self.assertFalse(isinstance(measurement.uptime, str))
        self.assertIsNotNone(measurement.uptime)
        self.assertFalse(isinstance(measurement.temp_f, str))
        self.assertIsNotNone(measurement.temp_f)
        self.assertFalse(isinstance(measurement.humidity, str))
        self.assertIsNotNone(measurement.humidity)
        self.assertFalse(isinstance(measurement.pressure, str))
        self.assertIsNotNone(measurement.pressure)
        self.assertFalse(isinstance(measurement.pm2_5_aqi, str))
        self.assertFalse(isinstance(measurement.pm2_5_aqi_b, str))
        self.assertIsNotNone(measurement.pm2_5_aqi_b)
        self.assertFalse(isinstance(measurement.pm2_5_aqi_epa, str))
        self.assertIsNotNone(measurement.pm2_5_aqi_epa)
        self.assertFalse(isinstance(measurement.p_0_3_um, str))
        self.assertFalse(isinstance(measurement.p_0_3_um_b, str))
        self.assertIsNotNone(measurement.p_0_3_um_b)
        self.assertFalse(isinstance(measurement.p_0_5_um, str))
        self.assertFalse(isinstance(measurement.p_0_5_um_b, str))
        self.assertIsNotNone(measurement.p_0_5_um_b)
        self.assertFalse(isinstance(measurement.p_1_0_um, str))
        self.assertFalse(isinstance(measurement.p_1_0_um_b, str))
        self.assertIsNotNone(measurement.p_1_0_um_b)
        self.assertFalse(isinstance(measurement.p_2_5_um, str))
        self.assertFalse(isinstance(measurement.p_2_5_um_b, str))
        self.assertIsNotNone(measurement.p_2_5_um_b)
        self.assertFalse(isinstance(measurement.p_5_0_um, str))
        self.assertFalse(isinstance(measurement.p_5_0_um_b, str))
        self.assertIsNotNone(measurement.p_5_0_um_b)
        self.assertFalse(isinstance(measurement.p_10_0_um, str))
        self.assertFalse(isinstance(measurement.p_10_0_um_b, str))
        self.assertIsNotNone(measurement.p_10_0_um_b)
        self.assertFalse(isinstance(measurement.pm1_0_atm, str))
        self.assertFalse(isinstance(measurement.pm1_0_atm_b, str))
        self.assertIsNotNone(measurement.pm1_0_atm_b)
        self.assertFalse(isinstance(measurement.pm1_0_cf_1, str))
        self.assertFalse(isinstance(measurement.pm1_0_cf_1_b, str))
        self.assertIsNotNone(measurement.pm1_0_cf_1_b)
        self.assertFalse(isinstance(measurement.pm2_5_atm, str))
        self.assertFalse(isinstance(measurement.pm2_5_atm_b, str))
        self.assertIsNotNone(measurement.pm2_5_atm_b)
        self.assertFalse(isinstance(measurement.pm2_5_cf_1, str))
        self.assertFalse(isinstance(measurement.pm2_5_cf_1_b, str))
        self.assertIsNotNone(measurement.pm2_5_cf_1_b)
        self.assertFalse(isinstance(measurement.pm2_5_atm, str))
        self.assertFalse(isinstance(measurement.pm2_5_atm_b, str))
        self.assertIsNotNone(measurement.pm2_5_atm_b)
        self.assertFalse(isinstance(measurement.pm2_5_cf_1, str))
        self.assertFalse(isinstance(measurement.pm2_5_cf_1_b, str))
        self.assertIsNotNone(measurement.pm2_5_cf_1_b)
        self.assertFalse(isinstance(measurement.pm10_0_atm, str))
        self.assertFalse(isinstance(measurement.pm10_0_atm_b, str))
        self.assertIsNotNone(measurement.pm10_0_atm_b)
        self.assertFalse(isinstance(measurement.pm10_0_cf_1, str))
        self.assertFalse(isinstance(measurement.pm10_0_cf_1_b, str))
        self.assertIsNotNone(measurement.pm10_0_cf_1_b)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
