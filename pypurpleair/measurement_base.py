#!/usr/bin/env python3

import abc
from typing import Any, Dict, Optional


class MeasurementBase(abc.ABC):
    @abc.abstractmethod
    def __init__(self, sensor_data: Dict[str, Any]):
        ...

    @property
    def data(self) -> Dict[str, Any]:
        """Return the internal data dictionary"""
        return self._data

    @staticmethod
    def get_aqi(pm_2_5: float) -> float:
        """Convert a pm 2.5 value to an AQI"""
        # NOTE: since the table on wikipedia is ambiguous to what happens at
        # jump points if there is more than a decimal of precision. Therefore,
        # we multiplying pm2.5 by 10 and convert to and int for detecting the
        # concentration limits of the pm2.5 value.
        pm_2_5 = int(pm_2_5 * 10)

        # Taken from wikipedia: https://en.wikipedia.org/wiki/Air_quality_index
        concentration_limits = [
            (0, 120),
            (121, 354),
            (355, 554),
            (555, 1504),
            (1505, 2504),
            (2505, 3504),
            (3505, 5004),
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
        for ii, (low, high) in enumerate(concentration_limits):
            if low <= pm_2_5 <= high:
                break
        pm_2_5 /= 10
        limit = (low / 10, high / 10)
        index_breakpoints = aqi_limits[ii]

        c_low, c_high = limit
        i_low, i_high = index_breakpoints
        aqi = (i_high - i_low) * (pm_2_5 - c_low) / (c_high - c_low) + i_low
        return aqi

    @staticmethod
    def get_epa_correction(
        pm2_5_cf_1_a: Optional[float], pm2_5_cf_1_b: Optional[float], humidity: Optional[float]
    ) -> Optional[float]:
        """Run the EPA correction on purpleair sensors

        Ref:
            - https://cfpub.epa.gov/si/si_public_record_report.cfm?Lab=CEMM&dirEntryId=349513

        Note:
            This doesn't run the 1-hour averages that are recommended as the
            measurement class only deals with current readings.

        Note:
            The web sensor has the possibility of null-values.

        Args:
            pm2_5_cf_1_a: (float) Channel A reading of pm2.5 concentration with CF 1
            pm2_5_cf_1_b: (float) Channel B reading of pm2.5 concentration with CF 1
            humidity: (float) Current humidity measured by the sensor.

        Returns:
            corrected pm2.5 value
        """
        if None in [pm2_5_cf_1_a, pm2_5_cf_1_b, humidity]:
            return None

        # Using the equation on page 25 of the EPA report pdf
        # constants on that page are different than at page 8 for some reason.
        pm2_5_mean = (pm2_5_cf_1_a + pm2_5_cf_1_b) / 2
        # It's possible when pm2_5 is near zero and the humidty is high that pm2.5
        # could go negative after correction. Assume anything less than zero is zero.
        return max(0.0, 0.534 * pm2_5_mean - 0.0844 * humidity + 5.604)

    @property
    def pm2_5_epa_correction(self) -> Optional[float]:
        return self.get_epa_correction(self.pm2_5_cf_1, self.pm2_5_cf_1_b, self.humidity)

    @property
    def pm2_5_aqi_epa(self) -> Optional[float]:
        pm2_5_epa = self.pm2_5_epa_correction
        if pm2_5_epa is None:
            return None

        return self.get_aqi(pm2_5_epa)

    #
    # Data fields as properties
    #

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
