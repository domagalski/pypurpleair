#!/usr/bin/env python3

"""Read PurpleAir sensor data on a LAN"""

import re
from typing import Any, Dict, Optional, Type

from pypurpleair import pa_base


class SensorReading(pa_base.SensorReadingBase):
    def __init__(self, sensor_data: Dict[str, Any]):
        self._data = sensor_data

    @property
    def sensor_id(self) -> str:
        return self._data["SensorId"]

    @property
    def timestamp(self) -> str:
        return self._data["DateTime"].upper()

    @property
    def lat(self) -> float:
        return self._data["lat"]

    @property
    def lon(self) -> float:
        return self._data["lon"]

    @property
    def place(self) -> str:
        return self._data["place"]

    @property
    def rssi(self) -> int:
        return self._data["rssi"]

    @property
    def temp_f(self) -> int:
        return self._data["current_temp_f"]

    @property
    def humidity(self) -> int:
        return self._data["current_humidity"]

    @property
    def dew_point_f(self) -> int:
        return self._data["current_dewpoint_f"]

    @property
    def pressure(self) -> float:
        return self._data["pressure"]

    @property
    def pm2_5_aqi(self) -> int:
        return self._data["pm2.5_aqi"]

    @property
    def pm2_5_aqi_b(self) -> int:
        return self._data["pm2.5_aqi_b"]

    @property
    def p_0_3_um(self) -> float:
        return self._data["p_0_3_um"]

    @property
    def p_0_3_um_b(self) -> float:
        return self._data["p_0_3_um_b"]

    @property
    def p_0_5_um(self) -> float:
        return self._data["p_0_5_um"]

    @property
    def p_0_5_um_b(self) -> float:
        return self._data["p_0_5_um_b"]

    @property
    def p_1_0_um(self) -> float:
        return self._data["p_1_0_um"]

    @property
    def p_1_0_um_b(self) -> float:
        return self._data["p_1_0_um_b"]

    @property
    def p_2_5_um(self) -> float:
        return self._data["p_2_5_um"]

    @property
    def p_2_5_um_b(self) -> float:
        return self._data["p_2_5_um_b"]

    @property
    def p_5_0_um(self) -> float:
        return self._data["p_5_0_um"]

    @property
    def p_5_0_um_b(self) -> float:
        return self._data["p_5_0_um_b"]

    @property
    def p_10_0_um(self) -> float:
        return self._data["p_10_0_um"]

    @property
    def p_10_0_um_b(self) -> float:
        return self._data["p_10_0_um_b"]

    @property
    def pm1_0_atm(self) -> float:
        return self._data["pm1_0_atm"]

    @property
    def pm1_0_atm_b(self) -> float:
        return self._data["pm1_0_atm_b"]

    @property
    def pm1_0_cf_1(self) -> float:
        return self._data["pm1_0_cf_1"]

    @property
    def pm1_0_cf_1_b(self) -> float:
        return self._data["pm1_0_cf_1_b"]

    @property
    def pm2_5_atm(self) -> float:
        return self._data["pm2_5_atm"]

    @property
    def pm2_5_atm_b(self) -> float:
        return self._data["pm2_5_atm_b"]

    @property
    def pm2_5_cf_1(self) -> float:
        return self._data["pm2_5_cf_1"]

    @property
    def pm2_5_cf_1_b(self) -> float:
        return self._data["pm2_5_cf_1_b"]

    @property
    def pm10_0_atm(self) -> float:
        return self._data["pm10_0_atm"]

    @property
    def pm10_0_atm_b(self) -> float:
        return self._data["pm10_0_atm_b"]

    @property
    def pm10_0_cf_1(self) -> float:
        return self._data["pm10_0_cf_1"]

    @property
    def pm10_0_cf_1_b(self) -> float:
        return self._data["pm10_0_cf_1_b"]


class Sensor(pa_base.SensorBase):
    """LAN Sensor class.

    A Purpleair sensor's data can be found at the following:
    http://<IP_ADDRESS>/json

    For live data (updates roughly 10 seconds):
    http://<IP_ADDRESS>/json?live=true
    """

    def __init__(self, addr: str):
        """Create a sensor object

        Args:
            addr: (str) The IP address to query. Do not include the http://
        """
        if not re.fullmatch(r"\d+.\d+.\d+.\d+", addr):
            if not re.match(r"^purpleair-\d+", addr.lower()):
                raise ValueError("addr must be an IP or PurpleAir hostname.")

        self._addr = addr

    @property
    def _reading_klass(self) -> Type:
        return SensorReading

    def _construct_url(self, live: bool) -> str:
        """Construct a URL to request.

        Args:
            live: (bool) Get live data instead of a 120 second average.

        Returns:
            The URL to be used for requests
        """
        url = f"http://{self._addr}/json"
        if live:
            url = f"{url}?live=true"
        return url

    def get_sensor_reading(self, *, live: bool = True) -> Optional[SensorReading]:
        """Get a reading of the PurpleAir sensor.

        Args:
            live: (bool) Get live data instead of a 120 second average.

        Returns:
            A SensorReading object if the query succeeds else None
        """
        return super().get_sensor_reading(live=live)

    def query_sensor(self, *, live: bool = True) -> Optional[Dict[str, Any]]:
        """Query a sensor and return a dict from the json result

        Args:
            live: (bool) Get live data instead of a 120 second average.

        Returns:
            The dict of the sensor json blob if the query succeeds else None
        """
        return super().query_sensor(live=live)
