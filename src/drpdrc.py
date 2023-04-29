import pandas as pd
from pathlib import Path
from typing import Tuple


class DrpDrc:
    def __init__(self, voltage_nominal=127.0, voltage_adequate_max=133.0,  voltage_adequate_min=117.0,
                 voltage_precarious_bottom_min=110.0, voltage_precarious_bottom_max=117.0,
                 voltage_precarious_top_min=133.0,  voltage_precarious_top_max=135.0, voltage_critical_max=135.0,
                 voltage_critical_min=110.0, eusd=1.0, _logger=None):

        self.logger = _logger
        self.voltage_nominal = voltage_nominal
        self.eusd=eusd

        self.voltage_adequate_max = voltage_adequate_max
        self.voltage_adequate_min = voltage_adequate_min

        self.voltage_precarious_bottom_min = voltage_precarious_bottom_min
        self.voltage_precarious_bottom_max = voltage_precarious_bottom_max
        self.voltage_precarious_top_min = voltage_precarious_top_min
        self.voltage_precarious_top_max = voltage_precarious_top_max

        self.voltage_critical_max = voltage_critical_max
        self.voltage_critical_min = voltage_critical_min

        self.voltage_adequate_max_pu = round(voltage_adequate_max / voltage_nominal, 3)
        self.voltage_adequate_min_pu = round(voltage_adequate_min / voltage_nominal, 3)

        self.voltage_precarious_bottom_min_pu = round(voltage_precarious_bottom_min / voltage_nominal, 3)
        self.voltage_precarious_bottom_max_pu = round(voltage_precarious_bottom_max / voltage_nominal, 3)
        self.voltage_precarious_top_min_pu = round(voltage_precarious_top_min / voltage_nominal, 3)
        self.voltage_precarious_top_max_pu = round(voltage_precarious_top_max / voltage_nominal, 3)

        self.voltage_critical_max_pu = round(voltage_critical_max / voltage_nominal, 3)
        self.voltage_critical_min_pu = round(voltage_critical_min / voltage_nominal, 3)

        self.drp_limit = 3 / 100
        self.drc_limit = 0.5 / 100
        self.total_measures = 1008

    def calculate_from_csv(self, file_path, column_index: str) -> Tuple[float, float, float]:

        data = pd.read_csv(Path(file_path))
        voltages = data[column_index]

        nlp = 0
        nlc = 0

        measure_time = 0
        for measure in range(self.total_measures):
            if measure_time == 1440:
                measure_time = 0
            target_voltage = voltages[measure_time]
            if (self.voltage_precarious_bottom_min <= target_voltage < self.voltage_precarious_bottom_max) \
                    or (self.voltage_precarious_top_min <= target_voltage <= self.voltage_precarious_top_max):
                nlp = nlp + 1

            if (target_voltage < self.voltage_critical_min) or (target_voltage > self.voltage_critical_max):
                nlc = nlc + 1

            measure_time = measure_time + 10

        drp = round((nlp / 1008) * 100, 4)
        drc = round((nlc / 1008) * 100, 4)

        # self.logger.debug(f'Fase alvo: {column_index}')
        # self.logger.debug(f'DRP: {drp}%')
        # self.logger.debug(f'DRC: {drc}%')

        if drp <= self.drp_limit:
            k1 = 0
        else:
            k1 = 3

        if drc < self.drc_limit:
            k2 = 0
        elif (drc > self.drc_limit) and (self.voltage_nominal < 2.3 * 10 ** 3):
            k2 = 7
        elif (drc > self.drc_limit) and (2.3 * 10 ** 3 <= self.voltage_nominal < 69 * 10 ** 3):
            k2 = 5
        else:
            k2 = 3

        comp = abs(((((drp - self.drp_limit)/100) * k1) + (((drc - self.drc_limit)/100) * k2)) * self.eusd)

        # self.logger.debug(f'Compensação: R${round(comp,2)}')

        return drp, drc, comp

