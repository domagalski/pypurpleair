#!/usr/bin/env python3

"""Read PurpleAir sensor data on a LAN"""

import re
from typing import Any, Dict, Optional, Type

from pypurpleair import influx
from pypurpleair import measurement_base
from pypurpleair import sensor_base

_TAG_KEYS = {
    "SensorId",
    "Geo",
    "ssid",
    "lat",
    "lon",
    "place",
    "version",
    "hardwareversion",
    "hardwarediscovered",
}


class Measurement(measurement_base.MeasurementBase):
    def __init__(self, sensor_data: Dict[str, Any]):
        self._data = sensor_data

    def prepare_for_influxdb(self) -> Optional[Dict[str, Any]]:
        """Prepare data as an InfluxDB point"""
        # This happens in early boot-phase when data isn't yet available.
        for key, value in self._data.items():
            # Only check particle sensor readings. This skips over Adc,
            # which takes a lot longer to initialize after boot.
            if not (key.startswith("p_") or key.startswith("pm")):
                continue
            if value == "nan":
                return None

        tags: Dict[str, Any] = {}
        for key in _TAG_KEYS:
            tags[key] = self._data[key]

        fields: Dict[str, Any] = {}
        for key in sorted(self._data.keys()):
            if key.startswith("current"):
                fields[key] = self._data[key]
            if key.startswith("p") and key not in ["pa_latency", "period", "place"]:
                fields[key] = self._data[key]
            if key in ["rssi", "uptime"]:
                fields[key] = self._data[key]

        fields["pm2.5_epa_correction"] = self.pm2_5_epa_correction
        fields["pm2.5_aqi_epa"] = self.pm2_5_aqi_epa

        influx_point = {"time": self.timestamp, "tags": tags, "fields": fields}
        return influx_point

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
    def uptime(self) -> int:
        return self._data["uptime"]

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


class Sensor(sensor_base.SensorBase):
    """LAN Sensor class.

    A Purpleair sensor's data can be found at the following:
    http://<IP_ADDRESS>/json

    For live data (updates roughly 10 seconds):
    http://<IP_ADDRESS>/json?live=true
    """

    def __init__(self, addr: str, db: Optional[influx.PurpleAirDb] = None):
        """Create a sensor object

        Args:
            addr: (str) The IP address to query. Do not include the http://
            db: Optional database client.
        """
        if not re.fullmatch(r"\d+.\d+.\d+.\d+", addr):
            if not re.match(r"^purpleair-\d+", addr.lower()):
                raise ValueError("addr must be an IP or PurpleAir hostname.")

        super().__init__(db)
        self._addr = addr

    @property
    def _measurement_klass(self) -> Type:
        return Measurement

    @property
    def _lost_connection_msg(self):
        return f"Cannot connect to sensor: {self._addr}"

    @property
    def _regained_connection_msg(self):
        return f"Connected to sensor: {self._addr}"

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

    def get_measurement(self, *, live: bool = True) -> Optional[Measurement]:
        """Get a reading of the PurpleAir sensor.

        Args:
            live: (bool) Get live data instead of a 120 second average.

        Returns:
            A SensorReading object if the query succeeds else None
        """
        return super().get_measurement(live=live)

    def query_sensor(self, *, live: bool = True) -> Optional[Dict[str, Any]]:
        """Query a sensor and return a dict from the json result

        Args:
            live: (bool) Get live data instead of a 120 second average.

        Returns:
            The dict of the sensor json blob if the query succeeds else None
        """
        return super().query_sensor(live=live)
