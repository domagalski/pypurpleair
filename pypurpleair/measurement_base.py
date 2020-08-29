#!/usr/bin/env python3

import abc
from typing import Any, Dict


class MeasurementBase(abc.ABC):
    @abc.abstractmethod
    def __init__(self, sensor_data: Dict[str, Any]):
        ...

    @property
    def data(self) -> Dict[str, Any]:
        """Return the internal data dictionary"""
        return self._data

    @abc.abstractmethod
    def prepare_for_influxdb(self) -> Dict[str, Any]:
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
    def uptime(self) -> int:
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
