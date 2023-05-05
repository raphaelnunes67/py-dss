import opendssdirect as dss
from tools import *
from plotter import Plotter
from ast import literal_eval


def get_all_loads() -> list:
    loads_list = []
    dss.Loads.First()
    while True:
        load = dict()
        load['Name'] = dss.Loads.Name()
        load['kvar'] = dss.Loads.kvar()
        load['kV'] = dss.Loads.kV()
        load['kW'] = dss.Loads.kW()
        load['kWh'] = dss.Loads.kWh()
        load['kVABase'] = dss.Loads.kVABase()
        load['kWhDays'] = dss.Loads.kWhDays()
        load['Daily'] = dss.Loads.Daily()
        load['PF'] = dss.Loads.PF()
        load['Phases'] = dss.Loads.Phases()

        loads_list.append(load)

        if not dss.Loads.Next() > 0:
            break

    return loads_list


def get_load_by_name(name: str) -> dict:
    dss.Loads.First()
    load = dict()
    while True:
        if name == dss.Loads.Name():
            load['Name'] = dss.Loads.Name()
            load['kvar'] = dss.Loads.kvar()
            load['kV'] = dss.Loads.kV()
            load['kW'] = dss.Loads.kW()
            load['kWh'] = dss.Loads.kWh()
            load['kVABase'] = dss.Loads.kVABase()
            load['kWhDays'] = dss.Loads.kWhDays()
            load['Daily'] = dss.Loads.Daily()
            load['PF'] = dss.Loads.PF()
            load['Phases'] = dss.Loads.Phases()
            break

        if not dss.Loads.Next() > 0:
            break

    return load


def set_load_property_by_name(name: str, property: str, value: Union[int, list]) -> bool:
    methods = [method for method in dir(dss.Loads) if callable(getattr(dss.Loads, method))]
    dss.Loads.First()
    result = False
    while True:
        if dss.Loads.Name() == name:
            if property in methods:
                eval(f'dss.Loads.{property}({value})')
                result = True
            break

        if not dss.Loads.Next() > 0:
            break

    return result


def get_all_load_shapes() -> list:
    loads_shapes_list = []
    dss.LoadShape.First()
    while True:
        load_shape = dict()
        load_shape['Name'] = dss.LoadShape.Name()
        load_shape['MinInterval'] = dss.LoadShape.MinInterval()
        load_shape['HrInterval'] = dss.LoadShape.HrInterval()
        load_shape['PMult'] = dss.LoadShape.PMult()
        load_shape['QMult'] = dss.LoadShape.QMult()
        load_shape['PBase'] = dss.LoadShape.PBase()
        load_shape['QBase'] = dss.LoadShape.QBase()
        load_shape['TimeArray'] = dss.LoadShape.TimeArray()
        load_shape['Npts'] = dss.LoadShape.Npts()
        load_shape['SInterval'] = dss.LoadShape.SInterval()
        loads_shapes_list.append(load_shape)

        if not dss.LoadShape.Next() > 0:
            break

    return loads_shapes_list


def get_load_shape_by_name(name: str) -> dict:
    dss.LoadShape.First()
    load_shape = dict()
    while True:
        if name == dss.LoadShape.Name():
            load_shape['Name'] = dss.LoadShape.Name()
            load_shape['MinInterval'] = dss.LoadShape.MinInterval()
            load_shape['HrInterval'] = dss.LoadShape.HrInterval()
            load_shape['PMult'] = dss.LoadShape.PMult()
            load_shape['QMult'] = dss.LoadShape.QMult()
            load_shape['PBase'] = dss.LoadShape.PBase()
            load_shape['QBase'] = dss.LoadShape.QBase()
            load_shape['TimeArray'] = dss.LoadShape.TimeArray()
            load_shape['Npts'] = dss.LoadShape.Npts()
            load_shape['SInterval'] = dss.LoadShape.SInterval()
            break

        if not dss.LoadShape.Next() > 0:
            break

    return load_shape


def set_load_shape_property_by_name(name: str, property: str, value: Union[int, list]) -> bool:
    methods = [method for method in dir(dss.LoadShape) if callable(getattr(dss.LoadShape, method))]
    dss.LoadShape.First()
    result = False
    while True:
        if dss.LoadShape.Name() == name:
            if property in methods:
                eval(f'dss.Loads.{property}({value})')
                result = True
            break

        if not dss.LoadShape.Next() > 0:
            break

    return result


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

    loads = get_all_loads()
    set_load_property_by_name(name='634a', property='kV', value=125)
    load = get_load_by_name('634a')

    loads_shapes = get_all_load_shapes()
    load_shape = get_load_shape_by_name('default')

    logger.debug(f'All loads: {loads}')
    logger.debug(f'Specific load: {load}')

    logger.debug(f'All load shapes: {loads_shapes}')
    logger.debug(f'Specific load shape: {load_shape}')

    dss.Solution.Solve()

    plotter = Plotter()

    plotter.set_file('IEEE13BARRAS_Mon_subestacaop_1.csv')

    plotter.set_axis(x='hour', y1='P1 (kW)', y2='P2 (kW)', y3='P3 (kW)')
    plotter.set_labels(l1='P1(kW)', l2='P2(kW)', l3='P3(kW)')
    plotter.set_axis_name(x_name='Time (h)', y_name='Power (kW)')
    plotter.set_title('Example')
    plotter.perform_plot()
    plotter.show_plot(show_legend=True)
