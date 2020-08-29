#!/usr/bin/env python3

import datetime
import logging
import json
from typing import Any, Dict, Optional, Type, Union

from pypurpleair import influx
from pypurpleair import measurement_base
from pypurpleair import sensor_base


_SENSOR_KEYS = {
    "pm1_0_atm",  # ATM PM1.0 particulate mass in ug/m3
    "pm2_5_atm",  # ATM PM2.5 particulate mass in ug/m3
    "pm10_0_atm",  # ATM PM10.0 particulate mass in ug/m3
    "pm1_0_cf_1",  # CF=1 PM1.0 particulate mass in ug/m3
    "pm2_5_cf_1",  # CF=1 PM2.5 particulate mass in ug/m3
    "pm10_0_cf_1",  # CF=1 PM10.0 particulate mass in ug/m3
    "p_0_3_um",  # 0.3 micrometer particle counts per deciliter of air
    "p_0_5_um",  # 0.5 micrometer particle counts per deciliter of air
    "p_1_0_um",  # 1.0 micrometer particle counts per deciliter of air
    "p_2_5_um",  # 2.5 micrometer particle counts per deciliter of air
    "p_5_0_um",  # 5.0 micrometer particle counts per deciliter of air
    "p_10_0_um",  # 10.0 micrometer particle counts per deciliter of air
}


class WebDataError(Exception):
    pass


class Measurement(measurement_base.MeasurementBase):
    _ch_a: Dict[str, Any] = {}
    _ch_b: Dict[str, Any] = {}
    _ch_a_stats: Dict[str, Union[int, float]] = {}
    _ch_b_stats: Dict[str, Union[int, float]] = {}

    def __init__(self, sensor_data: Dict[str, Any]):
        results = sensor_data.get("results", [])
        if not results:
            raise WebDataError("No data in sensor data dict")

        self._ch_a = results[0]
        self._ch_a_stats = json.loads(self._ch_a["Stats"])
        if len(results) < 2:
            logging.warning("Only one channel of data present.")
        else:
            self._ch_b = results[1]
            self._ch_b_stats = json.loads(self._ch_b["Stats"])

    def prepare_for_influxdb(self) -> Dict[str, Any]:
        """Prepare data as an InfluxDB point"""

        tags: Dict[str, Any] = {}
        tags["sensor_id"] = self.sensor_id
        tags["label"] = self._ch_a["Label"]
        tags["lat"] = self.lat
        tags["lon"] = self.lat
        tags["hidden"] = self._ch_a["Hidden"].lower() == "true"

        # If self._ch_b is available, then both sensors are present.
        fields: Dict[str, Any] = {}
        if self._ch_b:
            for key in _SENSOR_KEYS:
                fields[key] = self.__getattribute__(key)
                fields[key + "_b"] = self.__getattribute__(key + "_b")
            fields["pm2.5_aqi"] = self.pm2_5_aqi
            fields["pm2.5_aqi_b"] = self.pm2_5_aqi_b
            fields["temp_f"] = self.temp_f
            fields["pressure"] = self.pressure
            fields["humidity"] = self.humidity
            fields["rssi"] = self.rssi
            fields["uptime"] = self.uptime
            tags["place"] = self.place
            tags["version"] = self._ch_a["Version"]
            tags["hardwarediscovered"] = self._ch_a["DEVICE_HARDWAREDISCOVERED"]
            tags["type"] = self._ch_a["Type"]
        else:
            for key in _SENSOR_KEYS:
                fields[key + "_b"] = self.__getattribute__(key)
            fields["pm2.5_aqi_b"] = self.pm2_5_aqi

        influx_point = {"time": self.timestamp, "tags": tags, "fields": fields}
        return influx_point

    @property
    def sensor_id(self) -> int:
        return self._ch_a["ID"]

    @property
    def timestamp(self) -> str:
        timestamp_s = self._ch_a_stats["lastModified"] / 1e3
        timestamp_dt = datetime.datetime.utcfromtimestamp(timestamp_s)
        return timestamp_dt.isoformat(sep="T", timespec="milliseconds") + "Z"

    @property
    def lat(self) -> float:
        return self._ch_a["Lat"]

    @property
    def lon(self) -> float:
        return self._ch_a["Lon"]

    @property
    def place(self) -> Optional[str]:
        return self._ch_a.get("DEVICE_LOCATIONTYPE")

    @property
    def rssi(self) -> Optional[int]:
        rssi = self._ch_a.get("RSSI")
        if rssi is not None:
            rssi = int(rssi)
        return rssi

    @property
    def uptime(self) -> Optional[int]:
        uptime = self._ch_a.get("Uptime")
        if uptime is not None:
            uptime = int(uptime)
        return uptime

    @property
    def temp_f(self) -> Optional[int]:
        temp_f = self._ch_a.get("temp_f")
        if temp_f is not None:
            temp_f = int(temp_f)
        return temp_f

    @property
    def humidity(self) -> Optional[int]:
        humidity = self._ch_a.get("humidity")
        if humidity is not None:
            humidity = int(humidity)
        return humidity

    @property
    def pressure(self) -> Optional[float]:
        pressure = self._ch_a.get("pressure")
        if pressure is not None:
            pressure = float(pressure)
        return pressure

    @staticmethod
    def _get_aqi(pm_2_5: float) -> float:
        """Convert a pm 2.5 value to an AQI"""
        # Taken from wikipedia: https://en.wikipedia.org/wiki/Air_quality_index
        concentration_limits = [
            (0.0, 12.0),
            (12.1, 35.4),
            (35.5, 55.4),
            (55.5, 150.4),
            (150.5, 250.4),
            (250.5, 350.4),
            (350.5, 500.4),
        ]
        aqi_limits = [
            (0, 50),
            (51, 100),
            (101, 150),
            (151, 200),
            (201, 300),
            (301, 400),
            (401, 500),
        ]
        limit = None
        index_breakpoints = None
        for i, (low, high) in enumerate(concentration_limits):
            if low <= pm_2_5 <= high:
                limit = (low, high)
                index_breakpoints = aqi_limits[i]
                break
        if limit is None:
            raise RuntimeError(f"PM 2.5 out of range: {pm_2_5}")

        c_low, c_high = limit
        i_low, i_high = index_breakpoints
        aqi = (i_high - i_low) * (pm_2_5 - c_low) / (c_high - c_low) + i_low
        return aqi

    @property
    def pm2_5_aqi(self) -> int:
        pm_2_5 = float(self._ch_a["PM2_5Value"])
        return self._get_aqi(pm_2_5)

    @property
    def pm2_5_aqi_b(self) -> Optional[int]:
        pm_2_5 = self._ch_b.get("PM2_5Value")
        if pm_2_5 is None:
            return None
        return self._get_aqi(float(pm_2_5))

    @property
    def p_0_3_um(self) -> float:
        return float(self._ch_a["p_0_3_um"])

    @property
    def p_0_3_um_b(self) -> Optional[float]:
        reading = self._ch_b.get("p_0_3_um")
        if reading is not None:
            reading = float(reading)
        return reading

    @property
    def p_0_5_um(self) -> float:
        return float(self._ch_a["p_0_5_um"])

    @property
    def p_0_5_um_b(self) -> Optional[float]:
        reading = self._ch_b.get("p_0_5_um")
        if reading is not None:
            reading = float(reading)
        return reading

    @property
    def p_1_0_um(self) -> float:
        return float(self._ch_a["p_1_0_um"])

    @property
    def p_1_0_um_b(self) -> Optional[float]:
        reading = self._ch_b.get("p_1_0_um")
        if reading is not None:
            reading = float(reading)
        return reading

    @property
    def p_2_5_um(self) -> float:
        return float(self._ch_a["p_2_5_um"])

    @property
    def p_2_5_um_b(self) -> Optional[float]:
        reading = self._ch_b.get("p_2_5_um")
        if reading is not None:
            reading = float(reading)
        return reading

    @property
    def p_5_0_um(self) -> float:
        return float(self._ch_a["p_5_0_um"])

    @property
    def p_5_0_um_b(self) -> Optional[float]:
        reading = self._ch_b.get("p_5_0_um")
        if reading is not None:
            reading = float(reading)
        return reading

    @property
    def p_10_0_um(self) -> float:
        return float(self._ch_a["p_10_0_um"])

    @property
    def p_10_0_um_b(self) -> Optional[float]:
        reading = self._ch_b.get("p_10_0_um")
        if reading is not None:
            reading = float(reading)
        return reading

    @property
    def pm1_0_atm(self) -> float:
        return float(self._ch_a["pm1_0_atm"])

    @property
    def pm1_0_atm_b(self) -> Optional[float]:
        reading = self._ch_b.get("pm1_0_atm")
        if reading is not None:
            reading = float(reading)
        return reading

    @property
    def pm1_0_cf_1(self) -> float:
        return float(self._ch_a["pm1_0_cf_1"])

    @property
    def pm1_0_cf_1_b(self) -> Optional[float]:
        reading = self._ch_b.get("pm1_0_cf_1")
        if reading is not None:
            reading = float(reading)
        return reading

    @property
    def pm2_5_atm(self) -> float:
        return float(self._ch_a["pm2_5_atm"])

    @property
    def pm2_5_atm_b(self) -> Optional[float]:
        reading = self._ch_b.get("pm1_0_atm")
        if reading is not None:
            reading = float(reading)
        return reading

    @property
    def pm2_5_cf_1(self) -> float:
        return float(self._ch_a["pm2_5_cf_1"])

    @property
    def pm2_5_cf_1_b(self) -> Optional[float]:
        reading = self._ch_b.get("pm2_5_cf_1")
        if reading is not None:
            reading = float(reading)
        return reading

    @property
    def pm10_0_atm(self) -> float:
        return float(self._ch_a["pm10_0_atm"])

    @property
    def pm10_0_atm_b(self) -> Optional[float]:
        reading = self._ch_b.get("pm10_0_atm")
        if reading is not None:
            reading = float(reading)
        return reading

    @property
    def pm10_0_cf_1(self) -> float:
        return float(self._ch_a["pm10_0_cf_1"])

    @property
    def pm10_0_cf_1_b(self) -> Optional[float]:
        reading = self._ch_b.get("pm10_0_cf_1")
        if reading is not None:
            reading = float(reading)
        return reading


class Sensor(sensor_base.SensorBase):
    """Web sensor class.

    This uses the JSON API for querying all online sensors.
    """

    def __init__(self, sensor_id: int, db: Optional[influx.PurpleAirDb] = None):
        """Create a web sensor

        Args:
            sensor_id: (int) Numerical ID of the sensor.
            db: Optional database client.
        """
        super().__init__(db)
        self._sensor_id = sensor_id

    @property
    def _measurement_klass(self) -> Type:
        return Measurement

    def _construct_url(self) -> str:
        url = f"https://www.purpleair.com/json?show={self._sensor_id}"
        return url

    @property
    def _lost_connection_msg(self):
        return "Cannot connect: purpleair.com"

    @property
    def _regained_connection_msg(self):
        return "Connected: purpleair.com"
