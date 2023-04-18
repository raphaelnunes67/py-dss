__author__ = 'Raphael Nunes'

import opendssdirect as dss
import random
from tools import *
from plotter import Plotter


def execute_ckt_case_study(logger, target_file, folder, percentage=0, volt_var_control=False, random_phase=False):
    dss.Text.Command('Redirect {}'.format(target_file))

    if percentage:
        n_loads = round(26 * percentage / 100)

        drawn_loads = random.sample(list(range(1, 27)), n_loads)

        logger.debug(f'Cargas selecionadas aleatoriamente: {drawn_loads}')

        for i in range(1, n_loads+1):
            phase = 2

            if random_phase:
                phase = random.randint(1, 3)

            dss.Text.Command(f'new load.ev{i} phases=1 bus1=CA746RES{drawn_loads[i-1]}.{phase} kV=0.220  kW=3.6 pf=0.95 model=1 conn=delta status=variable daily=shapev1')
            dss.Text.Command(f'new PVsystem.pv{i} phases=3 bus1=CA746RES{drawn_loads[i-1]}.{phase} conn=wye kV=4.16 kVA=6000 daily=PVshape5')
            if volt_var_control:
                dss.Text.Command(f'new Invcontrol.Inv{i} Mode=VOLTVAR voltage_curvex_ref=rated vvc_curve1=vv_curve Pvsystemlist="pv1" RefReactivePower=VARMAX_VARS DeltaQ_factor=0.1')



    dss.Text.Command('new monitor.carga1 element=load.carga1 terminal=1 mode=0')
    dss.Text.Command('new monitor.carga14 element=load.carga14 terminal=1 mode=0')
    dss.Text.Command('new monitor.carga17 element=load.carga17 terminal=1 mode=0')
    dss.Text.Command('new monitor.carga26 element=load.carga26 terminal=1 mode=0')

    dss.Text.Command('set voltagebases=[13.8 0.220]')
    dss.Text.Command('calcvoltagebases')
    dss.Text.Command('set mode=daily')
    dss.Text.Command('set stepsize=1h')
    dss.Text.Command('set number=24')
    # dss.Text.Command('batchedit load..* vminpu=0.3')
    dss.Text.Command('solve')

    dss.Text.Command('export monitors carga1')
    dss.Text.Command('export monitors carga14')
    dss.Text.Command('export monitors carga17')
    dss.Text.Command('export monitors carga26')


    plotter_load_1 = Plotter()
    plotter_load_1.set_file(f'{folder}/REDE1_Mon_carga1_1.csv')
    plotter_load_1.set_axis(x='hour', y1='V1', y2='V2', y3='V3')
    plotter_load_1.set_labels(l1='V1(pu)', l2='V2(pu)', l3='V3(pu)')
    plotter_load_1.set_axis_name(x_name='Time (h)', y_name='Tension (pu)')
    plotter_load_1.set_title(f'Load 1 - Percentage VE and PV: {percentage}% - VoltVar: {volt_var_control}')
    plotter_load_1.perform_plot(bases=127)
    plotter_load_1.show_plot(show_legend=True)

    min_value_load_1_V1 = plotter_load_1.get_min_value('V1')
    min_value_load_1_V2 = plotter_load_1.get_min_value('V2')
    min_value_load_1_V3 = plotter_load_1.get_min_value('V3')

    max_value_load_1_V1 = plotter_load_1.get_max_value('V1')
    max_value_load_1_V2 = plotter_load_1.get_max_value('V2')
    max_value_load_1_V3 = plotter_load_1.get_max_value('V3')

    logger.debug('----------------------CARGA 01-------------------------------')
    logger.debug(f'Valor minimo de tensão V1 (carga 1): {min_value_load_1_V1}')
    logger.debug(f'Valor minimo de tensão V2 (carga 1): {min_value_load_1_V2}')
    logger.debug(f'Valor minimo de tensão V3 (carga 1): {min_value_load_1_V3}')

    logger.debug(f'Valor máximo de tensão V1 (carga 1): {max_value_load_1_V1}')
    logger.debug(f'Valor máximo de tensão V2 (carga 1): {max_value_load_1_V2}')
    logger.debug(f'Valor máximo de tensão V3 (carga 1): {max_value_load_1_V3}')

    plotter_load_14 = Plotter()
    plotter_load_14.set_file(f'{folder}/REDE1_Mon_carga14_1.csv')
    plotter_load_14.set_axis(x='hour', y1='V1', y2='V2', y3='V3')
    plotter_load_14.set_labels(l1='V1(pu)', l2='V2(pu)', l3='V3(pu)')
    plotter_load_14.set_axis_name(x_name='Time (h)', y_name='Tension (pu)')
    plotter_load_14.set_title(f'Load 14 - Percentage VE and PV: {percentage}% - VoltVar: {volt_var_control}')
    plotter_load_14.perform_plot(bases=127)
    plotter_load_14.show_plot(show_legend=True)

    min_value_load_14_V1 = plotter_load_14.get_min_value('V1')
    min_value_load_14_V2 = plotter_load_14.get_min_value('V2')
    min_value_load_14_V3 = plotter_load_14.get_min_value('V3')

    max_value_load_14_V1 = plotter_load_14.get_max_value('V1')
    max_value_load_14_V2 = plotter_load_14.get_max_value('V2')
    max_value_load_14_V3 = plotter_load_14.get_max_value('V3')

    logger.debug('----------------------CARGA 14-------------------------------')
    logger.debug(f'Valor minimo de tensão V1 (carga 14): {min_value_load_14_V1}')
    logger.debug(f'Valor minimo de tensão V2 (carga 14): {min_value_load_14_V2}')
    logger.debug(f'Valor minimo de tensão V3 (carga 14): {min_value_load_14_V3}')

    logger.debug(f'Valor máximo de tensão V1 (carga 14): {max_value_load_14_V1}')
    logger.debug(f'Valor máximo de tensão V2 (carga 14): {max_value_load_14_V2}')
    logger.debug(f'Valor máximo de tensão V3 (carga 14): {max_value_load_14_V3}')

    plotter_load_17 = Plotter()
    plotter_load_17.set_file(f'{folder}/REDE1_Mon_carga17_1.csv')
    plotter_load_17.set_axis(x='hour', y1='V1', y2='V2', y3='V3')
    plotter_load_17.set_labels(l1='V1(pu)', l2='V2(pu)', l3='V3(pu)')
    plotter_load_17.set_axis_name(x_name='Time (h)', y_name='Tension (pu)')
    plotter_load_17.set_title(f'Load 17 - Percentage VE and PV: {percentage}% - VoltVar: {volt_var_control}')
    plotter_load_17.perform_plot(bases=127)
    plotter_load_17.show_plot(show_legend=True)

    logger.debug('----------------------CARGA 17-------------------------------')
    min_value_load_17_V1 = plotter_load_17.get_min_value('V1')
    min_value_load_17_V2 = plotter_load_17.get_min_value('V2')
    min_value_load_17_V3 = plotter_load_17.get_min_value('V3')

    max_value_load_17_V1 = plotter_load_17.get_max_value('V1')
    max_value_load_17_V2 = plotter_load_17.get_max_value('V2')
    max_value_load_17_V3 = plotter_load_17.get_max_value('V3')

    logger.debug(f'Valor minimo de tensão V1 (carga 17): {min_value_load_17_V1}')
    logger.debug(f'Valor minimo de tensão V2 (carga 17): {min_value_load_17_V2}')
    logger.debug(f'Valor minimo de tensão V3 (carga 17): {min_value_load_17_V3}')

    logger.debug(f'Valor máximo de tensão V1 (carga 17): {max_value_load_17_V1}')
    logger.debug(f'Valor máximo de tensão V2 (carga 17): {max_value_load_17_V2}')
    logger.debug(f'Valor máximo de tensão V3 (carga 17): {max_value_load_17_V3}')

    plotter_load_26 = Plotter()
    plotter_load_26.set_file(f'{folder}/REDE1_Mon_carga26_1.csv')
    plotter_load_26.set_axis(x='hour', y1='V1', y2='V2', y3='V3')
    plotter_load_26.set_labels(l1='V1(pu)', l2='V2(pu)', l3='V3(pu)')
    plotter_load_26.set_axis_name(x_name='Time (h)', y_name='Tension (pu)')
    plotter_load_26.set_title(f'Load 26 - Percentage VE and PV: {percentage}% - VoltVar: {volt_var_control}')
    plotter_load_26.perform_plot(bases=127)
    plotter_load_26.show_plot(show_legend=True)

    min_value_load_26_V1 = plotter_load_26.get_min_value('V1')
    min_value_load_26_V2 = plotter_load_26.get_min_value('V2')
    min_value_load_26_V3 = plotter_load_26.get_min_value('V3')

    max_value_load_26_V1 = plotter_load_26.get_max_value('V1')
    max_value_load_26_V2 = plotter_load_26.get_max_value('V2')
    max_value_load_26_V3 = plotter_load_26.get_max_value('V3')

    logger.debug('----------------------CARGA 26-------------------------------')
    logger.debug(f'Valor minimo de tensão V1 (carga 26): {min_value_load_26_V1}')
    logger.debug(f'Valor minimo de tensão V2 (carga 26): {min_value_load_26_V2}')
    logger.debug(f'Valor minimo de tensão V3 (carga 26): {min_value_load_26_V3}')

    logger.debug(f'Valor máximo de tensão V1 (carga 26): {max_value_load_26_V1}')
    logger.debug(f'Valor máximo de tensão V2 (carga 26): {max_value_load_26_V2}')
    logger.debug(f'Valor máximo de tensão V3 (carga 26): {max_value_load_26_V3}')


if __name__ == '__main__':
    log = Log()
    logger = log.set_logger_stdout('script01')
    files = HandleFiles()

    logger.debug('OpenDSSDirect.py version: {}'.format(dss.__version__))
    logger.debug('Engine information: {}'.format(dss.Basic.Version()))
    target_file = files.get_target_file_path(folder='networks_article', file='ca746_revista2.dss')
    folder = files.get_target_folder_path()

    dss.Basic.DataPath(folder)

    # execute_ckt_case_study(logger, target_file, folder, percentage=0)
    # execute_ckt_case_study(logger, target_file, folder, percentage=20, volt_var_control=False)
    # execute_ckt_case_study(logger, target_file, folder, percentage=40, volt_var_control=False)

    #execute_ckt_case_study(logger, target_file, folder, percentage=60, volt_var_control=False)
    # execute_ckt_case_study(logger, target_file, folder, percentage=80, volt_var_control=False)
    # execute_ckt_case_study(logger, target_file, folder, percentage=100, volt_var_control=False)

    # execute_ckt_case_study(logger, target_file, folder, percentage=20, volt_var_control=True)
    # execute_ckt_case_study(logger, target_file, folder, percentage=40, volt_var_control=True)
    # execute_ckt_case_study(logger, target_file, folder, percentage=60, volt_var_control=True)
    # execute_ckt_case_study(logger, target_file, folder, percentage=80, volt_var_control=True)
    execute_ckt_case_study(logger, target_file, folder, percentage=100, volt_var_control=True)


