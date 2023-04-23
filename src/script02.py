__author__ = 'Raphael Nunes'

import opendssdirect as dss
import random
from tools import *
from plotter import Plotter
from drpdrc import DrpDrc


def execute_ckt_case_study_2(logger, target_file, folder, phase_selected=0):
    target_loads_list = random.sample(range(1, 27), 26)  # list with random load's numbers
    ev_shapes = random.sample(list(range(1, 5000)), 26)  # select randomly a specific shape

    battery_shapes = ev_shapes

    percentages_list = [0, 20, 40, 60, 80, 100]

    logger.debug(f'Lista com ordem aleatoria para inserção das cargas: {target_loads_list}')
    logger.debug(f'Lista de indices das curvas de VE com ordem aleatória: {ev_shapes}')

    Plotter().write_list_in_csv('../../results/drp_drc_load01.csv', '%', percentages_list)
    Plotter().write_list_in_csv('../../results/drp_drc_load14.csv', '%', percentages_list)
    Plotter().write_list_in_csv('../../results/drp_drc_load17.csv', '%', percentages_list)
    Plotter().write_list_in_csv('../../results/drp_drc_load26.csv', '%', percentages_list)
    Plotter().write_list_in_csv('../../results/losses.csv', '%', percentages_list)

    if not phase_selected:
        phase = random.randint(1, 3)
    else:
        phase = phase_selected

    voltvar = 'OFF'

    for _ in range(2):

        comp_total_01_list = []
        comp_total_14_list = []
        comp_total_17_list = []
        comp_total_26_list = []

        load_01_v1_drp_list = []
        load_01_v2_drp_list = []
        load_01_v3_drp_list = []

        load_01_v1_drc_list = []
        load_01_v2_drc_list = []
        load_01_v3_drc_list = []

        load_14_v1_drp_list = []
        load_14_v2_drp_list = []
        load_14_v3_drp_list = []

        load_14_v1_drc_list = []
        load_14_v2_drc_list = []
        load_14_v3_drc_list = []

        load_17_v1_drp_list = []
        load_17_v2_drp_list = []
        load_17_v3_drp_list = []

        load_17_v1_drc_list = []
        load_17_v2_drc_list = []
        load_17_v3_drc_list = []

        load_26_v1_drp_list = []
        load_26_v2_drp_list = []
        load_26_v3_drp_list = []

        load_26_v1_drc_list = []
        load_26_v2_drc_list = []
        load_26_v3_drc_list = []

        losses_list = []

        for percentage in percentages_list:

            if voltvar == 'ON' and percentage == 0:
                comp_total_01_list.append('-')
                comp_total_14_list.append('-')
                comp_total_17_list.append('-')
                comp_total_26_list.append('-')

                load_01_v1_drp_list.append('-')
                load_01_v2_drp_list.append('-')
                load_01_v3_drp_list.append('-')

                load_01_v1_drc_list.append('-')
                load_01_v2_drc_list.append('-')
                load_01_v3_drc_list.append('-')

                load_14_v1_drp_list.append('-')
                load_14_v2_drp_list.append('-')
                load_14_v3_drp_list.append('-')

                load_14_v1_drc_list.append('-')
                load_14_v2_drc_list.append('-')
                load_14_v3_drc_list.append('-')

                load_17_v1_drp_list.append('-')
                load_17_v2_drp_list.append('-')
                load_17_v3_drp_list.append('-')

                load_17_v1_drc_list.append('-')
                load_17_v2_drc_list.append('-')
                load_17_v3_drc_list.append('-')

                load_26_v1_drp_list .append('-')
                load_26_v2_drp_list.append('-')
                load_26_v3_drp_list.append('-')

                load_26_v1_drc_list.append('-')
                load_26_v2_drc_list.append('-')
                load_26_v3_drc_list.append('-')

                losses_list.append('-')
                continue

            n = round(26 * percentage / 100)

            dss.Text.Command('Redirect {}'.format(target_file))
            voltvar_defined = False

            if n:
                for i in range(1, n + 1):
                    
                    dss.Text.Command(f'new Loadshape.shapev{i} npts=1440 minterval=1 mult=(file=ev_shapes.csv, col={ev_shapes[i - 1]})')
                    dss.Text.Command(f'new Loadshape.shapebattery{i} npts=1440 minterval=1 mult=(file=battery_shapes.csv, col={battery_shapes[i - 1]})')
                    dss.Text.Command(f'new load.ev{i} phases=1 bus1=CA746RES{target_loads_list[i - 1]}.{phase} kV=0.127  kW=3.6 pf=0.95 model=1 conn=delta status=variable daily=shapev{i}')
                    dss.Text.Command(f'new PVsystem.pv{i} phases=3 bus1=CA746RES{target_loads_list[i - 1]}.{phase} conn=wye kV=4.16 kVA=6000 daily=PVshape5')

                    if voltvar == 'ON':
                        dss.Text.Command(f'new Storage.VE{i} bus1=CA746RES{target_loads_list[i - 1]}.{phase} phases=1 kV=0.127 kWRated=10 kW=2.6 kWhRated=40 %stored=25 state=idle dispmode=follow model=1 chargeTrigger=0.5 dischargeTrigger=0.5 daily=shapebattery{i}')
                        if not voltvar_defined:
                            dss.Text.Command('new Invcontrol.Inv1 Mode=VOLTVAR voltage_curvex_ref=rated vvc_curve1=vv_curve DeltaQ_factor=0.1  voltagechangetolerance=0.1 varchangetolerance=0.1')
                            voltvar_defined = True

            dss.Text.Command(f'new monitor.carga1_PV_VE_percentage_{percentage}_voltvar_{voltvar} element=load.carga1 terminal=1 mode=0')
            dss.Text.Command(f'new monitor.carga14_PV_VE_percentage_{percentage}_voltvar_{voltvar} element=load.carga14 terminal=1 mode=0')
            dss.Text.Command(f'new monitor.carga17_PV_VE_percentage_{percentage}_voltvar_{voltvar} element=load.carga17 terminal=1 mode=0')
            dss.Text.Command(f'new monitor.carga26_PV_VE_percentage_{percentage}_voltvar_{voltvar} element=load.carga26 terminal=1 mode=0')

            dss.Text.Command(f'new energymeter.busbar_PV_VE_percentage_{percentage}_voltvar_{voltvar} element=transformer.CA746 terminal=1')

            dss.Text.Command('set voltagebases=[13.8 0.220]')
            dss.Text.Command('calcvoltagebases')
            dss.Text.Command('set mode=daily')
            dss.Text.Command('set stepsize=1m')
            dss.Text.Command('set number=1440')
            # dss.Text.Command('batchedit load..* vminpu=0.3')
            dss.Solution.Solve()

            losses_list.append(dss.Meters.RegisterValues()[12])

            dss.Text.Command(f'export monitors carga1_PV_VE_percentage_{percentage}_voltvar_{voltvar}')
            dss.Text.Command(f'export monitors carga14_PV_VE_percentage_{percentage}_voltvar_{voltvar}')
            dss.Text.Command(f'export monitors carga17_PV_VE_percentage_{percentage}_voltvar_{voltvar}')
            dss.Text.Command(f'export monitors carga26_PV_VE_percentage_{percentage}_voltvar_{voltvar}')

            logger.debug(f'----------------------CARGA-01-VE-PV={percentage}%-voltvar={voltvar}-------------------------------')
            plotter = Plotter()
            plotter.set_file(f'{folder}/REDE1_Mon_carga1_PV_VE_percentage_{percentage}_voltvar_{voltvar}_1.csv')
            plotter.set_axis(x='hour', y1='V1', y2='V2', y3='V3')
            plotter.set_labels(l1='V1(pu)', l2='V2(pu)', l3='V3(pu)')
            plotter.set_axis_name(x_name='Time (h)', y_name='Tension (pu)')
            plotter.set_title(f'Load 1 - Percentage VE and PV: {percentage}% - VoltVar: {voltvar}')
            plotter.handle_csv_time()
            plotter.perform_plot(bases=127.0)
            # plotter.show_plot(show_legend=True)
            plotter.save_figure(f'/../../results/carga1_PV_VE_percentage_{percentage}_voltvar_{voltvar}.png')

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
                f'{folder}/REDE1_Mon_carga1_PV_VE_percentage_{percentage}_voltvar_{voltvar}_1.csv',
                column_index='V1')

            logger.debug(f'DRP: {drp1}%')
            logger.debug(f'DRC: {drc1}%')
            logger.debug(f'Compensação: R${round(comp1, 2)}')

            load_01_v1_drp_list.append(drp1)
            load_01_v1_drc_list.append(drc1)

            logger.debug('Fase alvo: V2')

            drp2, drc2, comp2 = DrpDrc(_logger=logger).calculate_from_csv(
                f'{folder}/REDE1_Mon_carga1_PV_VE_percentage_{percentage}_voltvar_{voltvar}_1.csv',
                column_index='V2')

            logger.debug(f'DRP: {drp2}%')
            logger.debug(f'DRC: {drc2}%')
            logger.debug(f'Compensação: R${round(comp2, 2)}')

            load_01_v2_drp_list.append(drp2)
            load_01_v2_drc_list.append(drc2)

            logger.debug('Fase alvo: V3')

            drp3, drc3, comp3 = DrpDrc(_logger=logger).calculate_from_csv(
                f'{folder}/REDE1_Mon_carga1_PV_VE_percentage_{percentage}_voltvar_{voltvar}_1.csv',
                column_index='V3')

            logger.debug(f'DRP: {drp3}%')
            logger.debug(f'DRC: {drc3}%')
            logger.debug(f'Compensação: R${round(comp3, 2)}')

            load_01_v3_drp_list.append(drp3)
            load_01_v3_drc_list.append(drc3)

            logger.debug('--------------------------------')
            comp_total_01 = round(comp1 + comp2 + comp3, 2)
            logger.debug(f'Compensação total: R${comp_total_01}')

            comp_total_01_list.append(comp_total_01)

            logger.debug(f'----------------------CARGA-14-VE-PV={percentage}%-voltvar={voltvar}-------------------------------')
            plotter.set_file(f'{folder}/REDE1_Mon_carga14_PV_VE_percentage_{percentage}_voltvar_{voltvar}_1.csv')
            plotter.set_axis(x='hour', y1='V1', y2='V2', y3='V3')
            plotter.set_labels(l1='V1(pu)', l2='V2(pu)', l3='V3(pu)')
            plotter.set_axis_name(x_name='Time (h)', y_name='Tension (pu)')
            plotter.set_title(f'Load 14 - Percentage VE and PV: {percentage}%-voltvar={voltvar}')
            plotter.handle_csv_time()
            plotter.perform_plot(bases=127.0)
            # plotter.show_plot(show_legend=True)
            plotter.save_figure(f'/../../results/carga14_PV_VE_percentage_{percentage}_voltvar_{voltvar}.png')

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
                f'{folder}/REDE1_Mon_carga14_PV_VE_percentage_{percentage}_voltvar_{voltvar}_1.csv',
                column_index='V1')

            logger.debug(f'DRP: {drp1}%')
            logger.debug(f'DRC: {drc1}%')
            logger.debug(f'Compensação: R${round(comp1, 2)}')

            load_14_v1_drp_list.append(drp1)
            load_14_v1_drc_list.append(drc1)

            logger.debug('Fase alvo: V2')

            drp2, drc2, comp2 = DrpDrc(_logger=logger).calculate_from_csv(
                f'{folder}/REDE1_Mon_carga14_PV_VE_percentage_{percentage}_voltvar_{voltvar}_1.csv',
                column_index='V2')

            logger.debug(f'DRP: {drp2}%')
            logger.debug(f'DRC: {drc2}%')
            logger.debug(f'Compensação: R${round(comp2, 2)}')

            load_14_v2_drp_list.append(drp2)
            load_14_v2_drc_list.append(drc2)

            logger.debug('Fase alvo: V3')

            drp3, drc3, comp3 = DrpDrc(_logger=logger).calculate_from_csv(
                f'{folder}/REDE1_Mon_carga14_PV_VE_percentage_{percentage}_voltvar_{voltvar}_1.csv',
                column_index='V3')

            logger.debug(f'DRP: {drp3}%')
            logger.debug(f'DRC: {drc3}%')
            logger.debug(f'Compensação: R${round(comp3, 2)}')

            load_14_v3_drp_list.append(drp3)
            load_14_v3_drc_list.append(drc3)

            logger.debug('--------------------------------')
            comp_total_14 = round(comp1 + comp2 + comp3, 2)
            logger.debug(f'Compensação total: R${comp_total_14}')

            comp_total_14_list.append(comp_total_14)

            logger.debug(f'----------------------CARGA-17-VE-PV={percentage}%-voltvar={voltvar}-------------------------------')
            plotter.set_file(f'{folder}/REDE1_Mon_carga17_PV_VE_percentage_{percentage}_voltvar_{voltvar}_1.csv')
            plotter.set_axis(x='hour', y1='V1', y2='V2', y3='V3')
            plotter.set_labels(l1='V1(pu)', l2='V2(pu)', l3='V3(pu)')
            plotter.set_axis_name(x_name='Time (h)', y_name='Tension (pu)')
            plotter.set_title(f'Load 17 - Percentage VE and PV: {percentage}% - voltvar={voltvar}')
            plotter.handle_csv_time()
            plotter.perform_plot(bases=127.0)
            # plotter.show_plot(show_legend=True)
            plotter.save_figure(f'/../../results/carga17_PV_VE_percentage_{percentage}_voltvar_{voltvar}.png')

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
                f'{folder}/REDE1_Mon_carga17_PV_VE_percentage_{percentage}_voltvar_{voltvar}_1.csv',
                column_index='V1')

            logger.debug(f'DRP: {drp1}%')
            logger.debug(f'DRC: {drc1}%')
            logger.debug(f'Compensação: R${round(comp1, 2)}')

            load_17_v1_drp_list.append(drp1)
            load_17_v1_drc_list.append(drc1)

            logger.debug('Fase alvo: V2')

            drp2, drc2, comp2 = DrpDrc(_logger=logger).calculate_from_csv(
                f'{folder}/REDE1_Mon_carga17_PV_VE_percentage_{percentage}_voltvar_{voltvar}_1.csv',
                column_index='V2')

            logger.debug(f'DRP: {drp2}%')
            logger.debug(f'DRC: {drc2}%')
            logger.debug(f'Compensação: R${round(comp2, 2)}')
            
            load_17_v2_drp_list.append(drp2)
            load_17_v2_drc_list.append(drc2)

            logger.debug('Fase alvo: V3')

            drp3, drc3, comp3 = DrpDrc(_logger=logger).calculate_from_csv(
                f'{folder}/REDE1_Mon_carga17_PV_VE_percentage_{percentage}_voltvar_{voltvar}_1.csv',
                column_index='V3')

            logger.debug(f'DRP: {drp3}%')
            logger.debug(f'DRC: {drc3}%')
            logger.debug(f'Compensação: R${round(comp3, 2)}')
            logger.debug('--------------------------------')
            comp_total_17 = round(comp1 + comp2 + comp3, 2)
            logger.debug(f'Compensação total: R${comp_total_17}')

            load_17_v3_drp_list.append(drp3)
            load_17_v3_drc_list.append(drc3)

            comp_total_17_list.append(comp_total_17)

            logger.debug(f'----------------------CARGA-26-VE-PV={percentage}%-voltvar={voltvar}-------------------------------')
            plotter.set_file(f'{folder}/REDE1_Mon_carga26_PV_VE_percentage_{percentage}_voltvar_{voltvar}_1.csv')
            plotter.set_axis(x='hour', y1='V1', y2='V2', y3='V3')
            plotter.set_labels(l1='V1(pu)', l2='V2(pu)', l3='V3(pu)')
            plotter.set_axis_name(x_name='Time (h)', y_name='Tension (pu)')
            plotter.set_title(f'Load 26 - Percentage VE and PV: {percentage}% - voltvar={voltvar}')
            plotter.handle_csv_time()
            plotter.perform_plot(bases=127.0)
            # plotter.show_plot(show_legend=True)
            plotter.save_figure(f'/../../results/carga26_PV_VE_percentage_{percentage}_voltvar_{voltvar}.png')

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

            drp1, drc1, comp1 = DrpDrc(_logger=logger).calculate_from_csv(
                f'{folder}/REDE1_Mon_carga26_PV_VE_percentage_{percentage}_voltvar_{voltvar}_1.csv',
                column_index='V1')

            logger.debug(f'DRP: {drp1}%')
            logger.debug(f'DRC: {drc1}%')
            logger.debug(f'Compensação: R${round(comp1, 2)}')

            load_26_v1_drp_list.append(drp1)
            load_26_v1_drc_list.append(drc1)

            logger.debug('Fase alvo: V2')

            drp2, drc2, comp2 = DrpDrc(_logger=logger).calculate_from_csv(
                f'{folder}/REDE1_Mon_carga26_PV_VE_percentage_{percentage}_voltvar_{voltvar}_1.csv',
                column_index='V2')

            logger.debug(f'DRP: {drp2}%')
            logger.debug(f'DRC: {drc2}%')
            logger.debug(f'Compensação: R${round(comp2, 2)}')

            load_26_v2_drp_list.append(drp2)
            load_26_v2_drc_list.append(drc2)

            logger.debug('Fase alvo: V3')

            drp3, drc3, comp3 = DrpDrc(_logger=logger).calculate_from_csv(
                f'{folder}/REDE1_Mon_carga26_PV_VE_percentage_{percentage}_voltvar_{voltvar}_1.csv',
                column_index='V3')

            logger.debug(f'DRP: {drp3}%')
            logger.debug(f'DRC: {drc3}%')
            logger.debug(f'Compensação: R${round(comp3, 2)}')
            logger.debug('--------------------------------')
            comp_total_26 = round(comp1 + comp2 + comp3, 2)
            logger.debug(f'Compensação total: R${comp_total_26}')

            load_26_v3_drp_list.append(drp3)
            load_26_v3_drc_list.append(drc3)

            comp_total_26_list.append(comp_total_26)

        Plotter().write_list_in_csv('../../results/drp_drc_load01.csv', f'compensacao_total_voltvar_{voltvar}', comp_total_01_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load01.csv', f'DRP(V1)_voltvar_{voltvar}', load_01_v1_drp_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load01.csv', f'DRP(V2)_voltvar_{voltvar}', load_01_v2_drp_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load01.csv', f'DRP(V3)_voltvar_{voltvar}', load_01_v3_drp_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load01.csv', f'DRC(V1)_voltvar_{voltvar}', load_01_v1_drc_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load01.csv', f'DRC(V2)_voltvar_{voltvar}', load_01_v2_drc_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load01.csv', f'DRC(V3)_voltvar_{voltvar}', load_01_v3_drc_list)

        Plotter().write_list_in_csv('../../results/drp_drc_load14.csv', f'compensacao_total_voltvar_{voltvar}', comp_total_14_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load14.csv', f'DRP(V1)_voltvar_{voltvar}', load_14_v1_drp_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load14.csv', f'DRP(V2)_voltvar_{voltvar}', load_14_v2_drp_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load14.csv', f'DRP(V3)_voltvar_{voltvar}', load_14_v3_drp_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load14.csv', f'DRC(V1)_voltvar_{voltvar}', load_14_v1_drc_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load14.csv', f'DRC(V2)_voltvar_{voltvar}', load_14_v2_drc_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load14.csv', f'DRC(V3)_voltvar_{voltvar}', load_14_v3_drc_list)

        Plotter().write_list_in_csv('../../results/drp_drc_load17.csv', f'compensacao_total_voltvar_{voltvar}', comp_total_17_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load17.csv', f'DRP(V1)_voltvar_{voltvar}', load_17_v1_drp_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load17.csv', f'DRP(V2)_voltvar_{voltvar}', load_17_v2_drp_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load17.csv', f'DRP(V3)_voltvar_{voltvar}', load_17_v3_drp_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load17.csv', f'DRC(V1)_voltvar_{voltvar}', load_17_v1_drc_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load17.csv', f'DRC(V2)_voltvar_{voltvar}', load_17_v2_drc_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load17.csv', f'DRC(V3)_voltvar_{voltvar}', load_17_v3_drc_list)

        Plotter().write_list_in_csv('../../results/drp_drc_load26.csv', f'compensacao_total_voltvar_{voltvar}', comp_total_26_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load26.csv', f'DRP(V1)_voltvar_{voltvar}', load_26_v1_drp_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load26.csv', f'DRP(V2)_voltvar_{voltvar}', load_26_v2_drp_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load26.csv', f'DRP(V3)_voltvar_{voltvar}', load_26_v3_drp_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load26.csv', f'DRC(V1)_voltvar_{voltvar}', load_26_v1_drc_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load26.csv', f'DRC(V2)_voltvar_{voltvar}', load_26_v2_drc_list)
        Plotter().write_list_in_csv('../../results/drp_drc_load26.csv', f'DRC(V3)_voltvar_{voltvar}', load_26_v3_drc_list)

        Plotter().write_list_in_csv('../../results/losses.csv', f'losses(kV)_voltvar_{voltvar}', losses_list)

        voltvar = 'ON'


if __name__ == '__main__':
    log = Log()
    logger = log.set_logger_stdout('script01')
    files = HandleFiles()

    logger.debug('OpenDSSDirect.py version: {}'.format(dss.__version__))
    logger.debug('Engine information: {}'.format(dss.Basic.Version()))
    target_file = files.get_target_file_path(folder='networks_article', file='ca746_revista2.dss')
    folder = files.get_target_folder_path()

    dss.Basic.DataPath(folder)

    execute_ckt_case_study_2(logger, target_file, folder, phase_selected=1)
