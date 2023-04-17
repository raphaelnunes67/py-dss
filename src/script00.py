__author__ = 'Raphael Nunes'

import opendssdirect as dss
from tools import *
from plotter import Plotter

log = Log()
logger = log.set_logger_stdout('article_script')
files = HandleFiles()


def circuit_default():
    dss.Text.Command('Redirect {}'.format(target_file))
    dss.Text.Command('Redirect voltage_base.dss')
    dss.Text.Command('Redirect monitor_sub.dss')
    dss.Text.Command('Redirect solve_daily.dss')
    dss.Text.Command('Transformer.RegFaseA.Taps = [1.0 1.0]')
    dss.Text.Command('Transformer.RegFaseB.Taps = [1.0 1.0]')
    dss.Text.Command('Transformer.RegFaseC.Taps = [1.0 1.0]')
    dss.Text.Command('Transformer.RegFaseC.Taps = [1.0 1.0]')

    dss.Text.Command('Set Controlmode = OFF')

    dss.Text.Command('Redirect command_monitor_sub.dss')


def plot_circuit_default_results(folder):
    plotter = Plotter()
    plotter.set_file(f'{folder}/IEEE13BARRAS_Mon_subestacaop_1.csv')

    plotter.set_axis(x='hour', y1='P1 (kW)', y2='P2 (kW)', y3='P3 (kW)')
    plotter.set_labels(l1='P1(kW)', l2='P2(kW)', l3='P3(kW)')
    plotter.set_axis_name(x_name='Time (h)', y_name='Power (kW)')
    plotter.set_title('Substation with Circuit Default')
    plotter.perform_plot()
    plotter.show_plot(show_legend=True)


def circuit_with_pv_and_storage():
    dss.Text.Command('Redirect {}'.format(target_file))

    dss.Text.Command('Redirect pvsystemexample.dss')
    dss.Text.Command('Redirect storage_power.dss')

    dss.Text.Command('Redirect voltage_base.dss')

    dss.Text.Command('Redirect monitor_sub.dss')

    dss.Text.Command('Redirect monitor_pv.dss')
    dss.Text.Command('Redirect solve_daily.dss')
    dss.Text.Command('Transformer.RegFaseA.Taps = [1.0 1.0]')
    dss.Text.Command('Transformer.RegFaseB.Taps = [1.0 1.0]')
    dss.Text.Command('Transformer.RegFaseC.Taps = [1.0 1.0]')
    dss.Text.Command('Transformer.RegFaseC.Taps = [1.0 1.0]')

    dss.Text.Command('Set Controlmode = OFF')

    dss.Text.Command('Redirect command_monitor_sub.dss')
    dss.Text.Command('Redirect command_monitor_pv.dss')


def plot_circuit_with_pv_and_storage(folder):
    plotter = Plotter()

    plotter.set_file(f'{folder}/IEEE13BARRAS_Mon_subestacaop_1.csv')

    plotter.set_axis(x='hour', y1='P1 (kW)', y2='P2 (kW)', y3='P3 (kW)')
    plotter.set_labels(l1='P1(kW)', l2='P2(kW)', l3='P3(kW)')
    plotter.set_axis_name(x_name='Time (h)', y_name='Power (kW)')
    plotter.set_title('Substation with PV and Storage')
    plotter.perform_plot()
    plotter.show_plot(show_legend=True)

    plotter = Plotter()

    plotter.set_file(f'{folder}/IEEE13BARRAS_Mon_solar_power_1.csv')

    plotter.set_axis(x='hour', y1='P1 (kW)', y2='P2 (kW)', y3='P3 (kW)')
    plotter.set_labels(l1='P1(kW)', l2='P2(kW)', l3='P3(kW)')
    plotter.set_axis_name(x_name='Time (h)', y_name='Power (kW)')
    plotter.set_title('Solar Power (kW)')
    plotter.perform_plot()
    plotter.show_plot(show_legend=True)


def circuit_with_pv_and_storage_and_volt_var():
    dss.Text.Command('Redirect {}'.format(target_file))

    dss.Text.Command('Redirect pvsystemexample.dss')
    dss.Text.Command('Redirect volt_var_pv.dss')
    dss.Text.Command('Redirect storage_power.dss')

    dss.Text.Command('Redirect voltage_base.dss')

    dss.Text.Command('Redirect monitor_sub.dss')
    dss.Text.Command('Redirect solve_daily.dss')
    dss.Text.Command('Transformer.RegFaseA.Taps = [1.0 1.0]')
    dss.Text.Command('Transformer.RegFaseB.Taps = [1.0 1.0]')
    dss.Text.Command('Transformer.RegFaseC.Taps = [1.0 1.0]')
    dss.Text.Command('Transformer.RegFaseC.Taps = [1.0 1.0]')

    dss.Text.Command('Set Controlmode = OFF')

    dss.Text.Command('Redirect command_monitor_sub.dss')


def plot_circuit_with_pv_and_storage_and_volt_var(folder):
    plotter = Plotter()

    plotter.set_file(f'{folder}/IEEE13BARRAS_Mon_subestacaop_1.csv')

    plotter.set_axis(x='hour', y1='P1 (kW)', y2='P2 (kW)', y3='P3 (kW)')
    plotter.set_labels(l1='P1(kW)', l2='P2(kW)', l3='P3(kW)')
    plotter.set_axis_name(x_name='Time (h)', y_name='Power (kW)')
    plotter.set_title('Substation with PV, Storage and VoltVar')
    plotter.perform_plot()
    plotter.show_plot(show_legend=True)


if __name__ == '__main__':

    logger.debug('OpenDSSDirect.py version: {}'.format(dss.__version__))
    logger.debug('Engine information: {}'.format(dss.Basic.Version()))
    target_file = files.get_target_file_path(folder='13Bus_tests', file='MASTER_default_IEEE13.dss')
    folder = files.get_target_folder_path()

    dss.Basic.DataPath(folder)

    circuit_default()
    plot_circuit_default_results(folder)

    circuit_with_pv_and_storage()
    plot_circuit_with_pv_and_storage(folder)

    circuit_with_pv_and_storage_and_volt_var()
    plot_circuit_with_pv_and_storage_and_volt_var(folder)
