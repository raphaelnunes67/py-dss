from ca746_simulation import CA746Simulation
from ca746_eusd import CA746Eusd
from ca746_prodist import CA746Prodist
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


if __name__ == '__main__':
    log = Log()
    logger = log.set_logger_stdout('CA746_script')
    simulation = CA746Simulation(logger)
    simulation.execute_case_study('ca746.dss')

    CA746Eusd(logger).calculate_eusd_data('ca746.dss')

    CA746Prodist().calculate_drp_drc_for_each_load('./results/voltvar_off')
    CA746Prodist().calculate_drp_drc_for_each_load('./results/voltvar_on')
    CA746Prodist().calculate_comp_total('./results/')
    logger.debug('Operation finished')
