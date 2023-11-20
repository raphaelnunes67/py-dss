import opendssdirect as dss
import csv
import logging
import sys


class Log:
    @staticmethod
    def set_logger_stdout(name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        return logger


class CA744Eusd:
    def __init__(self, logger):
        self.logger = logger
        self.logger.debug('OpenDSSDirect.py version: {}'.format(dss.__version__))
        self.logger.debug('Engine information: {}'.format(dss.Basic.Version()))

    @staticmethod
    def save_file(eusd_data_list):
        with open('results/eusd_loads.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for row in eusd_data_list:
                writer.writerow(row)

    def calculate_eusd_data(self, target_file: str):
        dss.Text.Command('Redirect {}'.format(target_file))
        all_residential_loads = dss.Loads.AllNames()[17:64]

        loads_infos = dict()

        dss.Loads.First()
        residential_loads_kw = []
        daily_shapes = []
        while True:
            load = dss.Loads.Name()
            if load in all_residential_loads:
                loads_infos[load] = dict()
                loads_infos[load]['kw'] = dss.Loads.kW()
                loads_infos[load]['load_shape'] = dss.Loads.Daily()

                dss.LoadShape.First()
                while True:
                    load_shape = dss.LoadShape.Name()
                    if load_shape == loads_infos[load]['load_shape']:
                        loads_infos[load]['PMult'] = dss.LoadShape.PMult()
                        break

                    if not dss.LoadShape.Next() > 0:
                        break
                residential_loads_kw.append(dss.Loads.kW())
                daily_shapes.append(dss.Loads.Daily())

            if not dss.Loads.Next() > 0:
                break

        # self.logger.debug('Loads infos: {}'.format(loads_infos))
        eusd = []

        for load in list(loads_infos.keys()):
            eusd_component = 0

            for element in loads_infos[load]['PMult']:
                eusd_component = eusd_component + (element * loads_infos[load]['kw']) / 60

            eusd.append(eusd_component * 30 * 0.275)

        eusd_data_list = [[value] for value in eusd]
        self.logger.debug('EUSD data calculated')

        self.save_file(eusd_data_list)

        self.logger.debug('EUSD file saved')


if __name__ == '__main__':
    log = Log()
    logger = log.set_logger_stdout('CA744_eusd')
    simulation = CA744Eusd(logger)
    simulation.calculate_eusd_data('ca744.dss')
