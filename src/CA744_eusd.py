import opendssdirect as dss
from tools import Log, HandleFiles
import csv

if __name__ == '__main__':
    log = Log()
    logger = log.set_logger_stdout('script01')
    files = HandleFiles()

    logger.debug('OpenDSSDirect.py version: {}'.format(dss.__version__))
    logger.debug('Engine information: {}'.format(dss.Basic.Version()))
    target_file = files.get_target_file_path(folder='ca744', file='ca744.dss')
    folder = files.get_target_folder_path()

    dss.Basic.DataPath(folder)

    dss.Text.Command('Redirect {}'.format(target_file))

    all_residential_loads = dss.Loads.AllNames()[17:64]

    loads_infos = dict()

    dss.Loads.First()
    residential_loads_kw = []
    daily_shapes = []
    while True:
        load = dss.Loads.Name()
        if load in all_residential_loads:
            loads_infos[load] = dict()
            loads_infos[load]['kw'] = dss.Loads.kW()
            loads_infos[load]['load_shape'] = dss.Loads.Daily()

            dss.LoadShape.First()
            while True:
                load_shape = dss.LoadShape.Name()
                if load_shape == loads_infos[load]['load_shape']:
                    loads_infos[load]['PMult'] = dss.LoadShape.PMult()
                    break

                if not dss.LoadShape.Next() > 0:
                    break
            residential_loads_kw.append(dss.Loads.kW())
            daily_shapes.append(dss.Loads.Daily())

        if not dss.Loads.Next() > 0:
            break

    logger.debug('Loads infos: {}'.format(loads_infos))
    eusd = []

    for load in list(loads_infos.keys()):
        eusd_component = 0

        for element in loads_infos[load]['PMult']:
            eusd_component = eusd_component + (element * loads_infos[load]['kw']) / 60

        eusd.append(eusd_component * 30 * 0.275)

    eusd_data_list = [[value] for value in eusd]
    with open('eusd_loads.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for row in eusd_data_list:
            writer.writerow(row)
