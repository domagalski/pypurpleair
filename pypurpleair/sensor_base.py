#!/usr/bin/env python3

import abc
import json
import logging
from typing import Any, Dict, Optional, Type

import requests
from requests import exceptions as rq_err

from pypurpleair import influx
from pypurpleair import measurement_base


class SensorBase(abc.ABC):
    """Sensor base class."""

    _db: Optional[influx.PurpleAirDb] = None
    _connected: bool = True

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

    def _make_request(self, url) -> Optional[str]:
        """Perform the http get request

        Returns:
            A string in json format from the sensor
        """
        try:
            response = requests.get(url)
        except rq_err.ConnectionError as err:
            if self._set_connection_state(False):
                logging.error("Requests Connection Error:")
                logging.error(str(err))
            return None

        if response.status_code != 200:
            logging.error(f"Cannot query URL: {url}")
            logging.error(f"Response status code: {response.status_code}")
            logging.error(f"Response text:\n{response.text}")
            return None

        return response.text

    @abc.abstractproperty
    def _lost_connection_msg(self):
        ...

    @abc.abstractproperty
    def _regained_connection_msg(self):
        ...

    def _set_connection_state(self, state: bool) -> bool:
        """Set the connection state to the sensor and report any changes"""
        state_changed = False
        if state and not self._connected:
            logging.info(self._regained_connection_msg)
            state_changed = True
        elif self._connected and not state:
            logging.error(self._lost_connection_msg)
            state_changed = True

        self._connected = state
        return state_changed
