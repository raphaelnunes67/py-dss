import opendssdirect as dss
from tools import *
from plotter import Plotter

if __name__ == '__main__':

    log = Log()
    logger = log.set_logger_stdout('template_debug')
    logger.debug('OpenDSSDirect.py version: {}'.format(dss.__version__))
    logger.debug('Engine information: {}'.format(dss.Basic.Version()))

    files = HandleFiles()
    target_file = files.get_target_file_path('13Bus_tests', 'MASTER_RedeTeste13Barras.dss')
    folder = files.get_target_folder_path()

    dss.Basic.DataPath(folder)
    dss.Text.Command('Redirect {}'.format(target_file))

    logger.debug(dss.Circuit.AllBusNames())

    dss.Loads.First()

    while True:
        load_name = dss.Loads.Name()
        load_kw = dss.Loads.kW()
        load_kv = dss.Loads.kV()
        load_kvar = dss.Loads.kvar()
        logger.debug('Load Name: {}, kW: {}, kv: {}, kvar: {}'
                     .format(load_name, load_kw, load_kv, load_kvar))

        if not dss.Loads.Next() > 0:
            break

    dss.Solution.Solve()

    plotter = Plotter()

    plotter.set_file('IEEE13BARRAS_Mon_subestacaop_1.csv')

    plotter.set_axis(x='hour', y1='P1 (kW)',  y2='P2 (kW)', y3='P3 (kW)')
    plotter.set_labels(l1='P1(kW)', l2='P2(kW)', l3='P3(kW)')
    plotter.set_axis_name(x_name='Time (h)', y_name='Power (kW)')
    plotter.set_title('Example')
    plotter.perform_plot()
    plotter.show_plot(show_legend=True)







