from ca744_simulation import CA744Simulation
from ca744_eusd import CA744Eusd
from ca744_prodist import CA744Prodist
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
    logger = log.set_logger_stdout('CA744_script')
    simulation = CA744Simulation(logger)
    simulation.execute_case_study('ca744.dss')

    CA744Eusd(logger).calculate_eusd_data('ca744.dss')

    CA744Prodist().calculate_drp_drc_for_each_load('./results/voltvar_off')
    CA744Prodist().calculate_drp_drc_for_each_load('./results/voltvar_on')
    CA744Prodist().calculate_comp_total('./results/')
