__author__ = 'Raphael Nunes'

import random
import csv
import os
import opendssdirect as dss
import logging
import sys
import shutil
from pathlib import Path


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


class CA746Simulation:
    def __init__(self, logger):
        self.percentages_list = [0, 20, 40, 60, 80, 100]
        self.ev_shapes = random.sample(list(range(1, 5001)), 46)
        self.target_loads_list = random.sample(range(1, 27), 26)  # list with random load's numbers
        self.logger = logger

        self.logger.debug('OpenDSSDirect.py version: {}'.format(dss.__version__))
        self.logger.debug('Engine information: {}'.format(dss.Basic.Version()))

    @staticmethod
    def create_results_folders() -> None:
        if not os.path.exists('./results'):
            os.mkdir('./results')

        for word in ('_0', '_20', '_40', '_60', '_80', '_100'):
            if not os.path.exists(Path(f'./results/voltvar_off/pv_ev{word}').resolve()):
                os.makedirs(Path(f'./results/voltvar_off/pv_ev{word}').resolve())

        for word in ('_20', '_40', '_60', '_80', '_100'):
            if not os.path.exists(Path(f'./results/voltvar_on/pv_ev{word}').resolve()):
                os.makedirs(Path(f'./results/voltvar_on/pv_ev{word}').resolve())

    @staticmethod
    def organize_files_results() -> None:
        _files = os.listdir('./')

        for file in _files:
            source = Path(f'./{file}').resolve()
            destination = './results'
            if file.find('.csv') != -1 and file.find('REDE1_Mon_') != - 1:
                if file.find('voltvar_off') != -1:
                    destination = destination + '/voltvar_off'
                    for word in ('_0', '_20', '_40', '_60', '_80', '_100'):
                        if file.find(word) != -1:
                            destination = destination + '/pv_ev' + word
                            if os.path.exists(f'{destination}/{file}'):
                                os.remove(f'{destination}/{file}')

                            shutil.move(source, destination)

                elif file.find('voltvar_on') != -1:
                    destination = destination + '/voltvar_on'
                    for word in ('_20', '_40', '_60', '_80', '_100'):
                        if file.find(word) != -1:
                            destination = destination + '/pv_ev' + word
                            if os.path.exists(f'{destination}/{file}'):
                                os.remove(f'{destination}/{file}')
                            shutil.move(source, destination)

        if os.path.exists(Path(f'./results/losses_voltvar_OFF.csv').resolve()):
            os.remove(Path(f'./results/losses_voltvar_OFF.csv').resolve())

        shutil.move(Path(f'./losses_voltvar_OFF.csv').resolve(),
                    Path('./results').resolve())

        if os.path.exists(Path(f'./results/losses_voltvar_ON.csv').resolve()):
            os.remove(Path(f'./results/losses_voltvar_ON.csv').resolve())

        shutil.move(Path(f'./losses_voltvar_ON.csv').resolve(),
                    Path('./results').resolve())

    def execute_case_study(self, target_file: str):
        self.logger.debug(f'Lista com ordem aleatoria para inserção das cargas: {self.target_loads_list}')
        self.logger.debug(f'Lista de indices das curvas de VE com ordem aleatória: {self.ev_shapes}')

        first_write: bool = True
        self.logger.debug('---- Starting Simulation LOOP ----')
        dss.Basic.DataPath('./')

        for voltvar in ('OFF', 'ON'):
            for percentage in self.percentages_list:
                if voltvar == 'ON' and percentage == 0:
                    first_write = True
                    continue

                self.logger.debug(f'Solving for {percentage}% and Voltvar Control {voltvar}...')
                n = round(26 * percentage / 100)
                dss.Text.Command('Redirect {}'.format(target_file))

                voltvar_defined = False

                if n:
                    for i in range(1, n + 1):

                        dss.Text.Command(f'new Loadshape.shapev{i} npts=1440 minterval=1 '
                                         f'mult=(file=data/ev_shapes.csv, col={self.ev_shapes[i - 1]})')

                        phase_a, phase_b = random.choice([(1, 2,), (2, 3), (1, 3)])

                        dss.Text.Command(f'new load.ev{i} phases=1 '
                                         f'bus1=CA746RES{self.target_loads_list[i - 1]}.{phase_a}.{phase_b} '
                                         f'kV=0.220  kW=3.6 pf=0.95 model=1 conn=delta  status=variable daily=shapev{i}')

                        phase_a, phase_b = random.choice([(1, 2,), (2, 3), (1, 3)])

                        dss.Text.Command(f'new PVsystem.pv{i} phases=1 '
                                         f'bus1=CA746RES{self.target_loads_list[i - 1]}.{phase_a}.{phase_b} '
                                         f'conn=wye kV=4.16 kVA=6000 daily=PVshape5')

                        if voltvar == 'ON':
                            if not voltvar_defined:
                                dss.Text.Command('new Invcontrol.Inv1 Mode=VOLTVAR voltage_curvex_ref=rated'
                                                 ' vvc_curve1=vv_curve DeltaQ_factor=0.1  voltagechangetolerance=0.1'
                                                 ' varchangetolerance=0.1')
                                voltvar_defined = True
                for i in range(1, 27):
                    dss.Text.Command(f'new monitor.carga{i}_PV_VE_percentage_{percentage}_voltvar_{voltvar}_voltage '
                                     f'element=load.carga{i} terminal=1 mode=0')
                    dss.Text.Command(f'new monitor.carga{i}_PV_VE_percentage_{percentage}_voltvar_{voltvar}_power '
                                     f'element=load.carga{i} terminal=1 mode=1 ppolar=no')

                dss.Text.Command(f'new energymeter.busbar_PV_VE_percentage_{percentage}_voltvar_{voltvar} '
                                 f'element=transformer.ca746 terminal=1')

                dss.Text.Command('set voltagebases=[13.8 0.220]')
                dss.Text.Command('calcvoltagebases')
                dss.Text.Command('set mode=daily')
                dss.Text.Command('set stepsize=1m')
                dss.Text.Command('set number=1440')
                dss.Solution.Solve()

                data = [[percentage, dss.Meters.RegisterValues()[12]]]

                if first_write:
                    with open(f'losses_voltvar_{voltvar}.csv', 'w', newline='') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerows(data)
                    first_write = False
                else:
                    with open(f'losses_voltvar_{voltvar}.csv', 'a', newline='') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerows(data)

                for i in range(1, 27):
                    dss.Text.Command(
                        f'export monitors carga{i}_PV_VE_percentage_{percentage}_voltvar_{voltvar}_voltage')
                    dss.Text.Command(f'export monitors carga{i}_PV_VE_percentage_{percentage}_voltvar_{voltvar}_power')

        self.logger.debug('---- Simulation Done -----')
        self.create_results_folders()
        self.organize_files_results()
        self.logger.debug('---- Files organized successfully -----')


if __name__ == '__main__':
    log = Log()
    logger = log.set_logger_stdout('CA746_simulation')
    simulation = CA746Simulation(logger)
    simulation.execute_case_study('ca746.dss')

