#!/usr/bin/env python3

import abc
import json
import logging
from typing import Any, Dict, Optional, Type

import requests

from pypurpleair import influx
from pypurpleair import measurement_base


class SensorBase(abc.ABC):
    """Sensor base class."""

    _db: Optional[influx.PurpleAirDb] = None

    @abc.abstractmethod
    def __init__(self, db: Optional[influx.PurpleAirDb] = None):
        """Create a sensor object

        Args:
            db: Optional database client.
        """
        self._db = db

    @abc.abstractmethod
    def _construct_url(self, *args, **kwargs) -> str:
        """Construct a URL to request."""
        ...

    @abc.abstractproperty
    def _measurement_klass(self) -> Type:
        """Return the class definition of the sensor reading type"""
        ...

    def query_and_write_database(self, *args, influx_measurement: str, **kwargs) -> bool:
        """Query the sensor and write the measurements to InfluxDB"""
        sensor_measurement = self.get_measurement(*args, **kwargs)
        if not sensor_measurement:
            logging.error("Error fetching sensor measurement. Cannot write database.")
            return False
        if self._db:
            return self._db.write_sensor_measurement(sensor_measurement, influx_measurement)
        else:
            logging.error("Sensor has no database reference. Cannot write to InfluxDB")
            return False

    def get_measurement(self, *args, **kwargs) -> Optional[measurement_base.MeasurementBase]:
        """Get a reading of the PurpleAir sensor.

        Args and kwargs go into self.query_sensor()

        Returns:
            A SensorReading object if the query succeeds else None
        """
        sensor_data = self.query_sensor(*args, **kwargs)
        if not sensor_data:
            return None
        return self._measurement_klass(sensor_data)

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
