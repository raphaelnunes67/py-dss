__author__ = 'Raphael Nunes'

import random
import shutil
import csv
import opendssdirect as dss
from tools import *


def execute_ckt_case_study(logger, target_file: str) -> None:
    target_loads_list = random.sample(range(1, 27), 26)  # list with random load's numbers
    ev_shapes = random.sample(list(range(1, 5000)), 26)  # select randomly a specific shape

    battery_shapes = ev_shapes

    percentages_list = [0, 20, 40, 60, 80, 100]

    logger.debug(f'Lista com ordem aleatoria para inserção das cargas: {target_loads_list}')
    logger.debug(f'Lista de indices das curvas de VE com ordem aleatória: {ev_shapes}')

    voltvar = 'OFF'
    logger.debug('---- Starting LOOP -----')
    for _ in range(2):

        for percentage in percentages_list:

            if voltvar == 'ON' and percentage == 0:
                continue

            logger.debug(f'Solving for {percentage}% and VoltVar Control {voltvar}...')
            n = round(26 * percentage / 100)

            dss.Text.Command('Redirect {}'.format(target_file))
            voltvar_defined = False

            if n:
                for i in range(1, n + 1):

                    dss.Text.Command(f'new Loadshape.shapev{i} npts=1440 minterval=1 '
                                     f'mult=(file=ev_shapes.csv, col={ev_shapes[i - 1]})')

                    dss.Text.Command(f'new Loadshape.shapebattery{i} npts=1440 minterval=1 '
                                     f'mult=(file=battery_shapes.csv, col={battery_shapes[i - 1]})')

                    phase_a, phase_b = random.choice([(1, 2,), (2, 3), (1, 3)])

                    dss.Text.Command(f'new load.ev{i} phases=1 '
                                     f'bus1=CA746RES{target_loads_list[i - 1]}.{phase_a}.{phase_b} '
                                     f'kV=0.220  kW=3.6 pf=0.95 model=1 conn=delta  status=variable daily=shapev{i}')
                    dss.Text.Command(f'new PVsystem.pv{i} phases=1 '
                                     f'bus1=CA746RES{target_loads_list[i - 1]}.{phase_a}.{phase_b} '
                                     f'conn=wye kV=4.16 kVA=6000 daily=PVshape5')

                    if voltvar == 'ON':
                        # dss.Text.Command(f'new Storage.VE{i} bus1=CA746RES{target_loads_list[i - 1]}.{phaseA}.{phaseB} '
                        #                  f'phases=1 kV=0.220 conn=delta kWRated=10 kW=2.6 kWhRated=40 %stored=25 '
                        #                  f'state=idle dispmode=follow model=1 chargeTrigger=0.5 dischargeTrigger=0.5 '
                        #                  f'daily=shapebattery{i}')
                        if not voltvar_defined:
                            dss.Text.Command('new Invcontrol.Inv1 Mode=VOLTVAR voltage_curvex_ref=rated'
                                             ' vvc_curve1=vv_curve DeltaQ_factor=0.1  voltagechangetolerance=0.1'
                                             ' varchangetolerance=0.1')
                            voltvar_defined = True
            for i in range(1, 27):
                dss.Text.Command(f'new monitor.carga{i}_PV_VE_percentage_{percentage}_voltvar_{voltvar} '
                                 f'element=load.carga{i} terminal=1 mode=0')

            dss.Text.Command(f'new energymeter.busbar_PV_VE_percentage_{percentage}_voltvar_{voltvar} '
                             f'element=transformer.CA746 terminal=1')

            dss.Text.Command('set voltagebases=[13.8 0.220]')
            dss.Text.Command('calcvoltagebases')
            dss.Text.Command('set mode=daily')
            dss.Text.Command('set stepsize=1m')
            dss.Text.Command('set number=1440')
            # dss.Text.Command('batchedit load..* vminpu=0.3')
            dss.Solution.Solve()

            data = [[percentage, dss.Meters.RegisterValues()[12]]]
            with open(f'losses_voltvar_{voltvar}.csv', 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(data)

            for i in range(1, 27):
                dss.Text.Command(f'export monitors carga{i}_PV_VE_percentage_{percentage}_voltvar_{voltvar}')

        voltvar = 'ON'

    logger.debug('---- Simulation Done -----')


def create_results_folder() -> None:
    for word in ('_20', '_40', '_60', '_80', '_100'):
        if not os.path.exists(Path(f'../../results/CA744_results/voltvar_off/pv_ev{word}').resolve()):
            os.makedirs(Path(f'../../results/CA744_results/voltvar_off/pv_ev{word}').resolve())

    for word in ('_20', '_40', '_60', '_80', '_100'):
        if not os.path.exists(Path(f'../../results/CA744_results/voltvar_on/pv_ev{word}').resolve()):
            os.makedirs(Path(f'../../results/CA744_results/voltvar_on/pv_ev{word}').resolve())


def move_files_results(_folder: str) -> None:

    _files = os.listdir(_folder)

    for file in _files:
        source = Path(_folder + '/' + file).resolve()
        destination = '../../results/CA744_results'
        if file.find('.csv') != -1 and file.find('REDE1_Mon_') != - 1:
            if file.find('voltvar_off') != -1:
                destination = destination + '/voltvar_off'
                for word in ('_20', '_40', '_60', '_80', '_100'):
                    if file.find(word) != -1:
                        destination = destination + '/pv_ev' + word
                        shutil.copy(source, destination)

            elif file.find('voltvar_on') != -1:
                destination = destination + '/voltvar_on'
                for word in ('_20', '_40', '_60', '_80', '_100'):
                    if file.find(word) != -1:
                        destination = destination + '/pv_ev' + word
                        shutil.copy(source, destination)

    shutil.copy(Path(_folder + '/losses_voltvar_OFF.csv').resolve(),
                Path('../../results/CA744_results/voltvar_off').resolve())

    shutil.copy(Path(_folder + '/losses_voltvar_ON.csv').resolve(),
                Path('../../results/CA744_results/voltvar_on').resolve())


if __name__ == '__main__':
    log = Log()
    logger = log.set_logger_stdout('script01')
    files = HandleFiles()

    logger.debug('OpenDSSDirect.py version: {}'.format(dss.__version__))
    logger.debug('Engine information: {}'.format(dss.Basic.Version()))
    target_file = files.get_target_file_path(folder='CA746', file='ca746_revista2.dss')
    folder = files.get_target_folder_path()

    dss.Basic.DataPath(folder)

    execute_ckt_case_study(logger, target_file)
    create_results_folder()
    move_files_results(folder)
