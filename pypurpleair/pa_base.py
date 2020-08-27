#!/usr/bin/env python3

import abc
import json
import logging
from typing import Any, Dict, Optional, Type

import requests


class SensorReadingBase(abc.ABC):
    @abc.abstractmethod
    def __init__(self, sensor_data: Dict[str, Any]):
        ...

    @abc.abstractproperty
    def sensor_id(self) -> str:
        ...

    @abc.abstractproperty
    def timestamp(self) -> str:
        ...

    @abc.abstractproperty
    def lat(self) -> float:
        ...

    @abc.abstractproperty
    def lon(self) -> float:
        ...

    @abc.abstractproperty
    def place(self) -> str:
        ...

    @abc.abstractproperty
    def rssi(self) -> int:
        ...

    @abc.abstractproperty
    def temp_f(self) -> int:
        ...

    @abc.abstractproperty
    def humidity(self) -> int:
        ...

    @abc.abstractproperty
    def pressure(self) -> float:
        ...

    @abc.abstractproperty
    def pm2_5_aqi(self) -> int:
        ...

    @abc.abstractproperty
    def pm2_5_aqi_b(self) -> int:
        ...

    @abc.abstractproperty
    def p_0_3_um(self) -> float:
        ...

    @abc.abstractproperty
    def p_0_3_um_b(self) -> float:
        ...

    @abc.abstractproperty
    def p_0_5_um(self) -> float:
        ...

    @abc.abstractproperty
    def p_0_5_um_b(self) -> float:
        ...

    @abc.abstractproperty
    def p_1_0_um(self) -> float:
        ...

    @abc.abstractproperty
    def p_1_0_um_b(self) -> float:
        ...

    @abc.abstractproperty
    def p_2_5_um(self) -> float:
        ...

    @abc.abstractproperty
    def p_2_5_um_b(self) -> float:
        ...

    @abc.abstractproperty
    def p_5_0_um(self) -> float:
        ...

    @abc.abstractproperty
    def p_5_0_um_b(self) -> float:
        ...

    @abc.abstractproperty
    def p_10_0_um(self) -> float:
        ...

    @abc.abstractproperty
    def p_10_0_um_b(self) -> float:
        ...

    @abc.abstractproperty
    def pm1_0_atm(self) -> float:
        ...

    @abc.abstractproperty
    def pm1_0_atm_b(self) -> float:
        ...

    @abc.abstractproperty
    def pm1_0_cf_1(self) -> float:
        ...

    @abc.abstractproperty
    def pm1_0_cf_1_b(self) -> float:
        ...

    @abc.abstractproperty
    def pm2_5_atm(self) -> float:
        ...

    @abc.abstractproperty
    def pm2_5_atm_b(self) -> float:
        ...

    @abc.abstractproperty
    def pm2_5_cf_1(self) -> float:
        ...

    @abc.abstractproperty
    def pm2_5_cf_1_b(self) -> float:
        ...

    @abc.abstractproperty
    def pm10_0_atm(self) -> float:
        ...

    @abc.abstractproperty
    def pm10_0_atm_b(self) -> float:
        ...

    @abc.abstractproperty
    def pm10_0_cf_1(self) -> float:
        ...

    @abc.abstractproperty
    def pm10_0_cf_1_b(self) -> float:
        ...


class SensorBase(abc.ABC):
    """Sensor base class."""

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        """Create a sensor object"""
        ...

    @abc.abstractmethod
    def _construct_url(self, *args, **kwargs) -> str:
        """Construct a URL to request."""
        ...

    @abc.abstractproperty
    def _reading_klass(self) -> Type:
        """Return the class definition of the sensor reading type"""
        ...

    def get_sensor_reading(self, *args, **kwargs) -> Optional[SensorReadingBase]:
        """Get a reading of the PurpleAir sensor.

        Args and kwargs go into self.query_sensor()

        Returns:
            A SensorReading object if the query succeeds else None
        """
        sensor_data = self.query_sensor(*args, **kwargs)
        if not sensor_data:
            return None
        return self._reading_klass(sensor_data)

    def query_sensor(self, *args, **kwargs) -> Optional[Dict[str, Any]]:
        """Query a sensor and return a dict from the json result

        Args and kwargs go into self._construct_url()

        Returns:
            The dict of the sensor json blob if the query succeeds else None
        """
        url = self._construct_url(*args, **kwargs)
        json_str = self._make_request(url)
        if not json_str:
            return None

        return json.loads(json_str)

    @staticmethod
    def _make_request(url) -> Optional[str]:
        """Perform the http get request

        Returns:
            A string in json format from the sensor
        """
        response = requests.get(url)
        if response.status_code != 200:
            logging.error(f"Cannot query URL: {url}")
            logging.error(f"Response status code: {response.status_code}")
            logging.error(f"Response text:\n{response.text}")
            return None

        return response.text
