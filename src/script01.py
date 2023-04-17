__author__ = 'Raphael Nunes'

import opendssdirect as dss
from tools import *
from plotter import Plotter

if __name__ == '__main__':
    log = Log()
    logger = log.set_logger_stdout('script01')
    files = HandleFiles()

    logger.debug('OpenDSSDirect.py version: {}'.format(dss.__version__))
    logger.debug('Engine information: {}'.format(dss.Basic.Version()))
    target_file = files.get_target_file_path(folder='networks_article', file='ca746_revista2.dss')
    folder = files.get_target_folder_path()

    dss.Basic.DataPath(folder)

    dss.Text.Command('Redirect {}'.format(target_file))

    dss.Text.Command('new monitor.carga1 element=load.carga1 terminal=1 mode=0')
    dss.Text.Command('new monitor.carga14 element=load.carga14 terminal=1 mode=0')
    dss.Text.Command('new monitor.carga17 element=load.carga17 terminal=1 mode=0')
    dss.Text.Command('new monitor.carga26 element=load.carga26 terminal=1 mode=0')

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
    plotter_load_1.set_title('Load 1')
    plotter_load_1.perform_plot(bases=127)
    plotter_load_1.show_plot(show_legend=True)

    min_value_load_1_V1 = plotter_load_1.get_min_value('V1')
    min_value_load_1_V2 = plotter_load_1.get_min_value('V2')
    min_value_load_1_V3 = plotter_load_1.get_min_value('V3')

    max_value_load_1_V1 = plotter_load_1.get_max_value('V1')
    max_value_load_1_V2 = plotter_load_1.get_max_value('V2')
    max_value_load_1_V3 = plotter_load_1.get_max_value('V3')

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
    plotter_load_14.set_title('Load 14')
    plotter_load_14.perform_plot(bases=127)
    plotter_load_14.show_plot(show_legend=True)

    min_value_load_14_V1 = plotter_load_14.get_min_value('V1')
    min_value_load_14_V2 = plotter_load_14.get_min_value('V2')
    min_value_load_14_V3 = plotter_load_14.get_min_value('V3')

    max_value_load_14_V1 = plotter_load_14.get_max_value('V1')
    max_value_load_14_V2 = plotter_load_14.get_max_value('V2')
    max_value_load_14_V3 = plotter_load_14.get_max_value('V3')

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
    plotter_load_17.set_title('Load 17')
    plotter_load_17.perform_plot(bases=127)
    plotter_load_17.show_plot(show_legend=True)

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
    plotter_load_26.set_title('Load 26')
    plotter_load_26.perform_plot(bases=127)
    plotter_load_26.show_plot(show_legend=True)

    min_value_load_26_V1 = plotter_load_26.get_min_value('V1')
    min_value_load_26_V2 = plotter_load_26.get_min_value('V2')
    min_value_load_26_V3 = plotter_load_26.get_min_value('V3')

    max_value_load_26_V1 = plotter_load_26.get_max_value('V1')
    max_value_load_26_V2 = plotter_load_26.get_max_value('V2')
    max_value_load_26_V3 = plotter_load_26.get_max_value('V3')

    logger.debug(f'Valor minimo de tensão V1 (carga 26): {min_value_load_26_V1}')
    logger.debug(f'Valor minimo de tensão V2 (carga 26): {min_value_load_26_V2}')
    logger.debug(f'Valor minimo de tensão V3 (carga 26): {min_value_load_26_V3}')

    logger.debug(f'Valor máximo de tensão V1 (carga 26): {max_value_load_26_V1}')
    logger.debug(f'Valor máximo de tensão V2 (carga 26): {max_value_load_26_V2}')
    logger.debug(f'Valor máximo de tensão V3 (carga 26): {max_value_load_26_V3}')


