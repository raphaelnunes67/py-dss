__author__ = 'Raphael Nunes'

import opendssdirect as dss
import random
from tools import *
from plotter import Plotter
from drpdrc import DrpDrc

def execute_ckt_case_study_1(logger, target_file, folder, percentage=0, volt_var_control=False, random_phase=False):
    dss.Text.Command('Redirect {}'.format(target_file))

    if percentage:
        n_loads = round(26 * percentage / 100)  # calculate loads quantity
        target_loads = random.sample(list(range(1, 27)), n_loads)  # select randomly where EV charger will be applied
        ev_shapes = random.sample(list(range(1, 5000)), n_loads)  # select randomly a specific shape

        logger.debug(f'Quantidade de cargas com EV + PV: {n_loads}')
        logger.debug(f'Cargas selecionadas aleatoriamente: {target_loads}')
        logger.debug(f'Colunas selecionadas aleatoriamente do arquivo de ev_shapes.csv: {ev_shapes}')

        for i in range(1, n_loads + 1):
            phase = 2

            if random_phase:
                phase = random.randint(1, 3)

            dss.Text.Command(f'new Loadshape.shapev{i} npts=1440 minterval=1 mult=(file=ev_shapes.csv, col={ev_shapes[i-1]})')

            dss.Text.Command(
                f'new load.ev{i} phases=1 bus1=CA746RES{target_loads[i - 1]}.{phase} kV=0.220  kW=3.6 pf=0.95 model=1 conn=delta status=variable daily=shapev{i}')
            dss.Text.Command(
                f'new PVsystem.pv{i} phases=3 bus1=CA746RES{target_loads[i - 1]}.{phase} conn=wye kV=4.16 kVA=6000 daily=PVshape5')
            if volt_var_control:
                dss.Text.Command(
                    f'new Invcontrol.Inv{i} Mode=VOLTVAR voltage_curvex_ref=rated vvc_curve1=vv_curve Pvsystemlist="pv1" RefReactivePower=VARMAX_VARS DeltaQ_factor=0.5')

    dss.Text.Command('new monitor.carga1 element=load.carga1 terminal=1 mode=0')
    dss.Text.Command('new monitor.carga14 element=load.carga14 terminal=1 mode=0')
    dss.Text.Command('new monitor.carga17 element=load.carga17 terminal=1 mode=0')
    dss.Text.Command('new monitor.carga26 element=load.carga26 terminal=1 mode=0')

    dss.Text.Command('set voltagebases=[13.8 0.220]')
    dss.Text.Command('calcvoltagebases')
    dss.Text.Command('set mode=daily')
    dss.Text.Command('set stepsize=1m')
    dss.Text.Command('set number=1440')
    # dss.Text.Command('batchedit load..* vminpu=0.3')
    dss.Solution.Solve()

    dss.Text.Command('export monitors carga1')
    dss.Text.Command('export monitors carga14')
    dss.Text.Command('export monitors carga17')
    dss.Text.Command('export monitors carga26')

    plotter = Plotter()
    plotter.set_file(f'{folder}/REDE1_Mon_carga1_1.csv')
    plotter.set_axis(x='hour', y1='V1', y2='V2', y3='V3')
    plotter.set_labels(l1='V1(pu)', l2='V2(pu)', l3='V3(pu)')
    plotter.set_axis_name(x_name='Time (h)', y_name='Tension (pu)')
    plotter.set_title(f'Load 1 - Percentage VE and PV: {percentage}% - VoltVar: {volt_var_control}')
    plotter.handle_csv_time()
    plotter.perform_plot(bases=127.0)
    plotter.show_plot(show_legend=True)

    min_value_load_1_V1 = plotter.get_min_value('V1')
    min_value_load_1_V2 = plotter.get_min_value('V2')
    min_value_load_1_V3 = plotter.get_min_value('V3')

    max_value_load_1_V1 = plotter.get_max_value('V1')
    max_value_load_1_V2 = plotter.get_max_value('V2')
    max_value_load_1_V3 = plotter.get_max_value('V3')

    logger.debug('----------------------CARGA 01-------------------------------')
    logger.debug(f'Valor minimo de tensão V1 (carga 1): {min_value_load_1_V1}')
    logger.debug(f'Valor minimo de tensão V2 (carga 1): {min_value_load_1_V2}')
    logger.debug(f'Valor minimo de tensão V3 (carga 1): {min_value_load_1_V3}')

    logger.debug(f'Valor máximo de tensão V1 (carga 1): {max_value_load_1_V1}')
    logger.debug(f'Valor máximo de tensão V2 (carga 1): {max_value_load_1_V2}')
    logger.debug(f'Valor máximo de tensão V3 (carga 1): {max_value_load_1_V3}')

    plotter.set_file(f'{folder}/REDE1_Mon_carga14_1.csv')
    plotter.set_axis(x='hour', y1='V1', y2='V2', y3='V3')
    plotter.set_labels(l1='V1(pu)', l2='V2(pu)', l3='V3(pu)')
    plotter.set_axis_name(x_name='Time (h)', y_name='Tension (pu)')
    plotter.set_title(f'Load 14 - Percentage VE and PV: {percentage}% - VoltVar: {volt_var_control}')
    plotter.handle_csv_time()
    plotter.perform_plot(bases=127.0)
    plotter.show_plot(show_legend=True)

    min_value_load_14_V1 = plotter.get_min_value('V1')
    min_value_load_14_V2 = plotter.get_min_value('V2')
    min_value_load_14_V3 = plotter.get_min_value('V3')

    max_value_load_14_V1 = plotter.get_max_value('V1')
    max_value_load_14_V2 = plotter.get_max_value('V2')
    max_value_load_14_V3 = plotter.get_max_value('V3')

    logger.debug('----------------------CARGA 14-------------------------------')
    logger.debug(f'Valor minimo de tensão V1 (carga 14): {min_value_load_14_V1}')
    logger.debug(f'Valor minimo de tensão V2 (carga 14): {min_value_load_14_V2}')
    logger.debug(f'Valor minimo de tensão V3 (carga 14): {min_value_load_14_V3}')

    logger.debug(f'Valor máximo de tensão V1 (carga 14): {max_value_load_14_V1}')
    logger.debug(f'Valor máximo de tensão V2 (carga 14): {max_value_load_14_V2}')
    logger.debug(f'Valor máximo de tensão V3 (carga 14): {max_value_load_14_V3}')

    plotter.set_file(f'{folder}/REDE1_Mon_carga17_1.csv')
    plotter.set_axis(x='hour', y1='V1', y2='V2', y3='V3')
    plotter.set_labels(l1='V1(pu)', l2='V2(pu)', l3='V3(pu)')
    plotter.set_axis_name(x_name='Time (h)', y_name='Tension (pu)')
    plotter.set_title(f'Load 17 - Percentage VE and PV: {percentage}% - VoltVar: {volt_var_control}')
    plotter.handle_csv_time()
    plotter.perform_plot(bases=127.0)
    plotter.show_plot(show_legend=True)

    logger.debug('----------------------CARGA 17-------------------------------')
    min_value_load_17_V1 = plotter.get_min_value('V1')
    min_value_load_17_V2 = plotter.get_min_value('V2')
    min_value_load_17_V3 = plotter.get_min_value('V3')

    max_value_load_17_V1 = plotter.get_max_value('V1')
    max_value_load_17_V2 = plotter.get_max_value('V2')
    max_value_load_17_V3 = plotter.get_max_value('V3')

    logger.debug(f'Valor minimo de tensão V1 (carga 17): {min_value_load_17_V1}')
    logger.debug(f'Valor minimo de tensão V2 (carga 17): {min_value_load_17_V2}')
    logger.debug(f'Valor minimo de tensão V3 (carga 17): {min_value_load_17_V3}')

    logger.debug(f'Valor máximo de tensão V1 (carga 17): {max_value_load_17_V1}')
    logger.debug(f'Valor máximo de tensão V2 (carga 17): {max_value_load_17_V2}')
    logger.debug(f'Valor máximo de tensão V3 (carga 17): {max_value_load_17_V3}')

    plotter.set_file(f'{folder}/REDE1_Mon_carga26_1.csv')
    plotter.set_axis(x='hour', y1='V1', y2='V2', y3='V3')
    plotter.set_labels(l1='V1(pu)', l2='V2(pu)', l3='V3(pu)')
    plotter.set_axis_name(x_name='Time (h)', y_name='Tension (pu)')
    plotter.set_title(f'Load 26 - Percentage VE and PV: {percentage}% - VoltVar: {volt_var_control}')
    plotter.handle_csv_time()
    plotter.perform_plot(bases=127.0)
    plotter.show_plot(show_legend=True)

    min_value_load_26_V1 = plotter.get_min_value('V1')
    min_value_load_26_V2 = plotter.get_min_value('V2')
    min_value_load_26_V3 = plotter.get_min_value('V3')

    max_value_load_26_V1 = plotter.get_max_value('V1')
    max_value_load_26_V2 = plotter.get_max_value('V2')
    max_value_load_26_V3 = plotter.get_max_value('V3')

    logger.debug('----------------------CARGA 26-------------------------------')
    logger.debug(f'Valor minimo de tensão V1 (carga 26): {min_value_load_26_V1}')
    logger.debug(f'Valor minimo de tensão V2 (carga 26): {min_value_load_26_V2}')
    logger.debug(f'Valor minimo de tensão V3 (carga 26): {min_value_load_26_V3}')

    logger.debug(f'Valor máximo de tensão V1 (carga 26): {max_value_load_26_V1}')
    logger.debug(f'Valor máximo de tensão V2 (carga 26): {max_value_load_26_V2}')
    logger.debug(f'Valor máximo de tensão V3 (carga 26): {max_value_load_26_V3}')


def execute_ckt_case_study_2(logger, target_file, folder, phase_selected=0):
    target_loads_list = random.sample(range(1, 27), 26)  # list with random load's numbers
    ev_shapes = random.sample(list(range(1, 5000)), 26)  # select randomly a specific shape
    percentages_list = [0, 20, 40, 60, 80, 100]

    Plotter().write_list_in_csv('comp_load_01.csv', '%', percentages_list)
    Plotter().write_list_in_csv('comp_load_14.csv', '%', percentages_list)
    Plotter().write_list_in_csv('comp_load_17.csv', '%', percentages_list)
    Plotter().write_list_in_csv('comp_load_26.csv', '%', percentages_list)

    comp_total_01_list = []
    comp_total_14_list = []
    comp_total_17_list = []
    comp_total_26_list = []

    if not phase_selected:
        phase = random.randint(1, 3)
    else:
        phase = phase_selected

    logger.debug(f'Lista com ordem aleatoria para inserção das cargas: {target_loads_list}')
    logger.debug(f'Lista de indices das curvas de VE com ordem aleatória: {ev_shapes}')

    for percentage in percentages_list:

        n = round(26 * percentage / 100)

        dss.Text.Command('Redirect {}'.format(target_file))

        if n:
            for i in range(1, n+1):
                dss.Text.Command(f'new Loadshape.shapev{i} npts=1440 minterval=1 mult=(file=ev_shapes.csv, col={ev_shapes[i-1]})')
                dss.Text.Command(
                    f'new load.ev{i} phases=1 bus1=CA746RES{target_loads_list[i - 1]}.{phase} kV=0.220  kW=3.6 pf=0.95 model=1 conn=delta status=variable daily=shapev{i}')
                dss.Text.Command(
                    f'new PVsystem.pv{i} phases=3 bus1=CA746RES{target_loads_list[i - 1]}.{phase} conn=wye kV=4.16 kVA=6000 daily=PVshape5')

        dss.Text.Command(f'new monitor.carga1_PV_VE_percentage_{percentage} element=load.carga1 terminal=1 mode=0')
        dss.Text.Command(f'new monitor.carga14_PV_VE_percentage_{percentage} element=load.carga14 terminal=1 mode=0')
        dss.Text.Command(f'new monitor.carga17_PV_VE_percentage_{percentage} element=load.carga17 terminal=1 mode=0')
        dss.Text.Command(f'new monitor.carga26_PV_VE_percentage_{percentage} element=load.carga26 terminal=1 mode=0')

        dss.Text.Command('set voltagebases=[13.8 0.220]')
        dss.Text.Command('calcvoltagebases')
        dss.Text.Command('set mode=daily')
        dss.Text.Command('set stepsize=1m')
        dss.Text.Command('set number=1440')
        # dss.Text.Command('batchedit load..* vminpu=0.3')
        dss.Solution.Solve()

        dss.Text.Command(f'export monitors carga1_PV_VE_percentage_{percentage}')
        dss.Text.Command(f'export monitors carga14_PV_VE_percentage_{percentage}')
        dss.Text.Command(f'export monitors carga17_PV_VE_percentage_{percentage}')
        dss.Text.Command(f'export monitors carga26_PV_VE_percentage_{percentage}')

        logger.debug(f'----------------------CARGA-01-VE-PV={percentage}%-------------------------------')
        plotter = Plotter()
        plotter.set_file(f'{folder}/REDE1_Mon_carga1_PV_VE_percentage_{percentage}_1.csv')
        plotter.set_axis(x='hour', y1='V1', y2='V2', y3='V3')
        plotter.set_labels(l1='V1(pu)', l2='V2(pu)', l3='V3(pu)')
        plotter.set_axis_name(x_name='Time (h)', y_name='Tension (pu)')
        plotter.set_title(f'Load 1 - Percentage VE and PV: {percentage}%')
        plotter.handle_csv_time()
        plotter.perform_plot(bases=127.0)
        # plotter.show_plot(show_legend=True)
        plotter.save_figure(f'/../../results/carga1_PV_VE_percentage_{percentage}.png')

        min_value_load_1_V1 = plotter.get_min_value('V1')
        min_value_load_1_V2 = plotter.get_min_value('V2')
        min_value_load_1_V3 = plotter.get_min_value('V3')

        max_value_load_1_V1 = plotter.get_max_value('V1')
        max_value_load_1_V2 = plotter.get_max_value('V2')
        max_value_load_1_V3 = plotter.get_max_value('V3')

        logger.debug(f'Valor minimo de tensão V1 (carga 1): {min_value_load_1_V1}')
        logger.debug(f'Valor minimo de tensão V2 (carga 1): {min_value_load_1_V2}')
        logger.debug(f'Valor minimo de tensão V3 (carga 1): {min_value_load_1_V3}')

        logger.debug(f'Valor máximo de tensão V1 (carga 1): {max_value_load_1_V1}')
        logger.debug(f'Valor máximo de tensão V2 (carga 1): {max_value_load_1_V2}')
        logger.debug(f'Valor máximo de tensão V3 (carga 1): {max_value_load_1_V3}')

        logger.debug('Fase alvo: V1')

        drp1, drc1, comp1 = DrpDrc(_logger=logger).calculate_from_csv(
            f'{folder}/REDE1_Mon_carga1_PV_VE_percentage_{percentage}_1.csv',
            column_index='V1')

        logger.debug(f'DRP: {drp1}%')
        logger.debug(f'DRC: {drc1}%')
        logger.debug(f'Compensação: R${round(comp1, 2)}')

        logger.debug('Fase alvo: V2')

        drp2, drc2, comp2 = DrpDrc(_logger=logger).calculate_from_csv(
            f'{folder}/REDE1_Mon_carga1_PV_VE_percentage_{percentage}_1.csv',
            column_index='V2')

        logger.debug(f'DRP: {drp2}%')
        logger.debug(f'DRC: {drc2}%')
        logger.debug(f'Compensação: R${round(comp2, 2)}')

        logger.debug('Fase alvo: V3')

        drp3, drc3, comp3 = DrpDrc(_logger=logger).calculate_from_csv(
            f'{folder}/REDE1_Mon_carga1_PV_VE_percentage_{percentage}_1.csv',
            column_index='V3')

        logger.debug(f'DRP: {drp3}%')
        logger.debug(f'DRC: {drc3}%')
        logger.debug(f'Compensação: R${round(comp3, 2)}')
        logger.debug('--------------------------------')
        logger.debug(f'Compensação total: R${round(comp1 + comp2 + comp3, 2)}')

        logger.debug(f'----------------------CARGA-14-VE-PV={percentage}%-------------------------------')
        plotter.set_file(f'{folder}/REDE1_Mon_carga14_PV_VE_percentage_{percentage}_1.csv')
        plotter.set_axis(x='hour', y1='V1', y2='V2', y3='V3')
        plotter.set_labels(l1='V1(pu)', l2='V2(pu)', l3='V3(pu)')
        plotter.set_axis_name(x_name='Time (h)', y_name='Tension (pu)')
        plotter.set_title(f'Load 14 - Percentage VE and PV: {percentage}%')
        plotter.handle_csv_time()
        plotter.perform_plot(bases=127.0)
        # plotter.show_plot(show_legend=True)
        plotter.save_figure(f'/../../results/carga14_PV_VE_percentage_{percentage}.png')

        min_value_load_14_V1 = plotter.get_min_value('V1')
        min_value_load_14_V2 = plotter.get_min_value('V2')
        min_value_load_14_V3 = plotter.get_min_value('V3')

        max_value_load_14_V1 = plotter.get_max_value('V1')
        max_value_load_14_V2 = plotter.get_max_value('V2')
        max_value_load_14_V3 = plotter.get_max_value('V3')

        logger.debug(f'Valor minimo de tensão V1 (carga 14): {min_value_load_14_V1}')
        logger.debug(f'Valor minimo de tensão V2 (carga 14): {min_value_load_14_V2}')
        logger.debug(f'Valor minimo de tensão V3 (carga 14): {min_value_load_14_V3}')

        logger.debug(f'Valor máximo de tensão V1 (carga 14): {max_value_load_14_V1}')
        logger.debug(f'Valor máximo de tensão V2 (carga 14): {max_value_load_14_V2}')
        logger.debug(f'Valor máximo de tensão V3 (carga 14): {max_value_load_14_V3}')

        logger.debug('Fase alvo: V1')

        drp1, drc1, comp1 = DrpDrc(_logger=logger).calculate_from_csv(
            f'{folder}/REDE1_Mon_carga14_PV_VE_percentage_{percentage}_1.csv',
            column_index='V1')

        logger.debug(f'DRP: {drp1}%')
        logger.debug(f'DRC: {drc1}%')
        logger.debug(f'Compensação: R${round(comp1, 2)}')

        logger.debug('Fase alvo: V2')

        drp2, drc2, comp2 = DrpDrc(_logger=logger).calculate_from_csv(
            f'{folder}/REDE1_Mon_carga14_PV_VE_percentage_{percentage}_1.csv',
            column_index='V2')

        logger.debug(f'DRP: {drp2}%')
        logger.debug(f'DRC: {drc2}%')
        logger.debug(f'Compensação: R${round(comp2, 2)}')

        logger.debug('Fase alvo: V3')

        drp3, drc3, comp3 = DrpDrc(_logger=logger).calculate_from_csv(
            f'{folder}/REDE1_Mon_carga14_PV_VE_percentage_{percentage}_1.csv',
            column_index='V3')

        logger.debug(f'DRP: {drp3}%')
        logger.debug(f'DRC: {drc3}%')
        logger.debug(f'Compensação: R${round(comp3, 2)}')
        logger.debug('--------------------------------')
        logger.debug(f'Compensação total: R${round(comp1 + comp2 + comp3, 2)}')

        logger.debug(f'----------------------CARGA-17-VE-PV={percentage}%-------------------------------')
        plotter.set_file(f'{folder}/REDE1_Mon_carga17_PV_VE_percentage_{percentage}_1.csv')
        plotter.set_axis(x='hour', y1='V1', y2='V2', y3='V3')
        plotter.set_labels(l1='V1(pu)', l2='V2(pu)', l3='V3(pu)')
        plotter.set_axis_name(x_name='Time (h)', y_name='Tension (pu)')
        plotter.set_title(f'Load 17 - Percentage VE and PV: {percentage}%')
        plotter.handle_csv_time()
        plotter.perform_plot(bases=127.0)
        # plotter.show_plot(show_legend=True)
        plotter.save_figure(f'/../../results/carga17_PV_VE_percentage_{percentage}.png')

        min_value_load_17_V1 = plotter.get_min_value('V1')
        min_value_load_17_V2 = plotter.get_min_value('V2')
        min_value_load_17_V3 = plotter.get_min_value('V3')

        max_value_load_17_V1 = plotter.get_max_value('V1')
        max_value_load_17_V2 = plotter.get_max_value('V2')
        max_value_load_17_V3 = plotter.get_max_value('V3')

        logger.debug(f'Valor minimo de tensão V1 (carga 17): {min_value_load_17_V1}')
        logger.debug(f'Valor minimo de tensão V2 (carga 17): {min_value_load_17_V2}')
        logger.debug(f'Valor minimo de tensão V3 (carga 17): {min_value_load_17_V3}')

        logger.debug(f'Valor máximo de tensão V1 (carga 17): {max_value_load_17_V1}')
        logger.debug(f'Valor máximo de tensão V2 (carga 17): {max_value_load_17_V2}')
        logger.debug(f'Valor máximo de tensão V3 (carga 17): {max_value_load_17_V3}')

        logger.debug('Fase alvo: V1')

        drp1, drc1, comp1 = DrpDrc(_logger=logger).calculate_from_csv(
            f'{folder}/REDE1_Mon_carga17_PV_VE_percentage_{percentage}_1.csv',
            column_index='V1')

        logger.debug(f'DRP: {drp1}%')
        logger.debug(f'DRC: {drc1}%')
        logger.debug(f'Compensação: R${round(comp1, 2)}')

        logger.debug('Fase alvo: V2')

        drp2, drc2, comp2 = DrpDrc(_logger=logger).calculate_from_csv(
            f'{folder}/REDE1_Mon_carga17_PV_VE_percentage_{percentage}_1.csv',
            column_index='V2')

        logger.debug(f'DRP: {drp2}%')
        logger.debug(f'DRC: {drc2}%')
        logger.debug(f'Compensação: R${round(comp2, 2)}')

        logger.debug('Fase alvo: V3')

        drp3, drc3, comp3 = DrpDrc(_logger=logger).calculate_from_csv(
            f'{folder}/REDE1_Mon_carga17_PV_VE_percentage_{percentage}_1.csv',
            column_index='V3')

        logger.debug(f'DRP: {drp3}%')
        logger.debug(f'DRC: {drc3}%')
        logger.debug(f'Compensação: R${round(comp3, 2)}')
        logger.debug('--------------------------------')
        logger.debug(f'Compensação total: R${round(comp1 + comp2+ comp3, 2)}')

        logger.debug(f'----------------------CARGA-26-VE-PV={percentage}%-------------------------------')
        plotter.set_file(f'{folder}/REDE1_Mon_carga26_PV_VE_percentage_{percentage}_1.csv')
        plotter.set_axis(x='hour', y1='V1', y2='V2', y3='V3')
        plotter.set_labels(l1='V1(pu)', l2='V2(pu)', l3='V3(pu)')
        plotter.set_axis_name(x_name='Time (h)', y_name='Tension (pu)')
        plotter.set_title(f'Load 26 - Percentage VE and PV: {percentage}%')
        plotter.handle_csv_time()
        plotter.perform_plot(bases=127.0)
        # plotter.show_plot(show_legend=True)
        plotter.save_figure(f'/../../results/carga26_PV_VE_percentage_{percentage}.png')

        min_value_load_26_V1 = plotter.get_min_value('V1')
        min_value_load_26_V2 = plotter.get_min_value('V2')
        min_value_load_26_V3 = plotter.get_min_value('V3')

        max_value_load_26_V1 = plotter.get_max_value('V1')
        max_value_load_26_V2 = plotter.get_max_value('V2')
        max_value_load_26_V3 = plotter.get_max_value('V3')

        logger.debug(f'Valor minimo de tensão V1 (carga 26): {min_value_load_26_V1}')
        logger.debug(f'Valor minimo de tensão V2 (carga 26): {min_value_load_26_V2}')
        logger.debug(f'Valor minimo de tensão V3 (carga 26): {min_value_load_26_V3}')

        logger.debug(f'Valor máximo de tensão V1 (carga 26): {max_value_load_26_V1}')
        logger.debug(f'Valor máximo de tensão V2 (carga 26): {max_value_load_26_V2}')
        logger.debug(f'Valor máximo de tensão V3 (carga 26): {max_value_load_26_V3}')

        logger.debug('Fase alvo: V1')

        drp1, drc1, comp1 = DrpDrc(_logger=logger).calculate_from_csv(f'{folder}/REDE1_Mon_carga26_PV_VE_percentage_{percentage}_1.csv',
                                                  column_index='V1')

        logger.debug(f'DRP: {drp1}%')
        logger.debug(f'DRC: {drc1}%')
        logger.debug(f'Compensação: R${round(comp1,2)}')

        logger.debug('Fase alvo: V2')

        drp2, drc2, comp2 = DrpDrc(_logger=logger).calculate_from_csv(
            f'{folder}/REDE1_Mon_carga26_PV_VE_percentage_{percentage}_1.csv',
            column_index='V2')

        logger.debug(f'DRP: {drp2}%')
        logger.debug(f'DRC: {drc2}%')
        logger.debug(f'Compensação: R${round(comp2, 2)}')

        logger.debug('Fase alvo: V3')

        drp3, drc3, comp3 = DrpDrc(_logger=logger).calculate_from_csv(
            f'{folder}/REDE1_Mon_carga26_PV_VE_percentage_{percentage}_1.csv',
            column_index='V3')

        logger.debug(f'DRP: {drp3}%')
        logger.debug(f'DRC: {drc3}%')
        logger.debug(f'Compensação: R${round(comp3, 2)}')
        logger.debug('--------------------------------')
        comp_total_26 = round(comp1 + comp2 + comp3, 2)
        logger.debug(f'Compensação total: R${comp_total_26}')

        comp_total_26_list.append(comp_total_26)

    Plotter().write_list_in_csv('comp_load_01.csv', 'comp_total', comp_total_01_list)
    Plotter().write_list_in_csv('comp_load_14.csv', 'comp_total', comp_total_14_list)
    Plotter().write_list_in_csv('comp_load_17.csv', 'comp_total', comp_total_17_list)
    Plotter().write_list_in_csv('comp_load_26.csv', 'comp_total', comp_total_26_list)



if __name__ == '__main__':
    log = Log()
    logger = log.set_logger_stdout('script01')
    files = HandleFiles()

    logger.debug('OpenDSSDirect.py version: {}'.format(dss.__version__))
    logger.debug('Engine information: {}'.format(dss.Basic.Version()))
    target_file = files.get_target_file_path(folder='networks_article', file='ca746_revista2.dss')
    folder = files.get_target_folder_path()

    dss.Basic.DataPath(folder)

    execute_ckt_case_study_2(logger, target_file, folder, phase_selected=2)

    # execute_ckt_case_study_1(logger, target_file, folder, percentage=0)
    # execute_ckt_case_study_1(logger, target_file, folder, percentage=20, volt_var_control=False)
    # execute_ckt_case_study_1(logger, target_file, folder, percentage=40, volt_var_control=False)
    #
    # execute_ckt_case_study_1(logger, target_file, folder, percentage=60, volt_var_control=False)
    # execute_ckt_case_study_1(logger, target_file, folder, percentage=80, volt_var_control=False)
    # execute_ckt_case_study_1(logger, target_file, folder, percentage=100, volt_var_control=False)
    #
    # execute_ckt_case_study_1(logger, target_file, folder, percentage=20, volt_var_control=True)
    # execute_ckt_case_study_1(logger, target_file, folder, percentage=40, volt_var_control=True)
    # execute_ckt_case_study_1(logger, target_file, folder, percentage=60, volt_var_control=True)
    # execute_ckt_case_study_1(logger, target_file, folder, percentage=80, volt_var_control=True)
    # execute_ckt_case_study_1(logger, target_file, folder, percentage=100, volt_var_control=True)
