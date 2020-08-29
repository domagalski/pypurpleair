#!/usr/bin/env python3

"""Simple wrapper around the InfluxDB client for writing time series"""

import json
import logging
from typing import Any, Dict, List, Optional

import influxdb
from influxdb import exceptions as influx_err
from requests import exceptions as rq_err

from pypurpleair import measurement_base

DEFAULT_DATABASE = "purpleair"


class PurpleAirDb(influxdb.InfluxDBClient):
    _time_precision = "ms"

    def __init__(self, **kwargs):
        self._db_name = kwargs.get("database") or DEFAULT_DATABASE
        kwargs["database"] = self._db_name
        super().__init__(**kwargs)

        self._connected = True

    def _get_database_names(self) -> Optional[List[str]]:
        """Get a list of database names in InfluxDB."""
        db_dict_list = self._run_influx_request(self.get_list_database, default_return_value=None)
        if db_dict_list is None:
            logging.error("Cannot fetch database names.")
            return None

        db_name_list = [db["name"] for db in db_dict_list]
        return db_name_list

    def init_database(self, database_name: Optional[str] = None) -> bool:
        """Initialize a database in InfluxDB."""
        database_name = database_name or self._db_name
        db_name_list = self._get_database_names()
        if db_name_list is None:
            return False

        if database_name not in db_name_list:
            logging.info(f"Creating database: {database_name!r}")
            if self._run_influx_request(
                self.create_database, database_name, default_return_value=True
            ):
                logging.error(f"Cannot create database: {database_name}")
                return False

        logging.info(f"Using database: {database_name!r}")
        self.switch_database(database_name)
        self._db_name = database_name
        return True

    @staticmethod
    def _pop_none_from_dict(influx_point: Dict[str, Any], category: str) -> Dict[str, Any]:
        keys = list(influx_point[category].keys())
        for key in keys:
            if influx_point[category][key] is None:
                influx_point[category].pop(key)
        return influx_point

    def write_sensor_measurement(
        self, sensor_measurement: measurement_base.MeasurementBase, influx_measurement: str
    ):
        """Write a sensor measurement to InfluxDB

        Args:
            sensor_measurement: A sensor measurement from either a LAN or web sensor.
            influx_measurement: (str) Name of the influx measurement/table to write to.
        """
        influx_point = sensor_measurement.prepare_for_influxdb()
        influx_point["measurement"] = influx_measurement

        if "tags" in influx_point:
            influx_point = self._pop_none_from_dict(influx_point, "tags")
        if "fields" in influx_point:
            influx_point = self._pop_none_from_dict(influx_point, "fields")

        success = self._run_influx_request(
            self.write_points,
            [influx_point],
            time_precision=self._time_precision,
            database=self._db_name,
            default_return_value=False,
        )

        if not success:
            logging.info("Failed to write sensor measurement to InfluxDB.")
        return success

    def _run_influx_request(self, func, *args, default_return_value: Any, **kwargs) -> bool:
        """Run a function that makes an InfluxDB request and handle any errors"""
        retval = default_return_value
        try:
            retval = func(*args, **kwargs)
            self._set_connection_state(True)
        except rq_err.ConnectionError as err:
            if self._set_connection_state(False):
                logging.error("Requests Connection Error:")
                logging.error(str(err))
        except influx_err.InfluxDBClientError as err:
            self._set_connection_state(True)
            msg = "InfluxDB Client Error:"
            if err.code is not None:
                msg = f"{msg} (code: {err.code})"
            logging.error(msg)

            try:
                content_dict = json.loads(err.content)
                content = content_dict.get("error")
                if content:
                    logging.error(f"{content}")
            except (TypeError, json.JSONDecodeError):
                pass
        except influx_err.InfluxDBServerError as err:
            if self._set_connection_state(False):
                logging.error("InfluxDB Server Error:")
                logging.error(str(err))

        return retval

    def _set_connection_state(self, state: bool) -> bool:
        """Set the connection state to InfluxDB and report any changes"""
        state_changed = False
        if state and not self._connected:
            logging.info("Regained connection to InfluxDB.")
            state_changed = True
        elif self._connected and not state:
            logging.error("Lost connection to InfluxDB.")
            state_changed = True

        self._connected = state
        return state_changed
