import opendssdirect as dss
from tools import Log, HandleFiles
import csv

if __name__ == '__main__':
    log = Log()
    logger = log.set_logger_stdout('script01')
    files = HandleFiles()

    logger.debug('OpenDSSDirect.py version: {}'.format(dss.__version__))
    logger.debug('Engine information: {}'.format(dss.Basic.Version()))
    target_file = files.get_target_file_path(folder='CA746', file='ca746_revista2.dss')
    folder = files.get_target_folder_path()

    dss.Basic.DataPath(folder)

    dss.Text.Command('Redirect {}'.format(target_file))

    all_residential_loads = dss.Loads.AllNames()[23:49]
    dss.Loads.First()
    residential_loads_kw = []
    daily_shapes = []
    while True:
        load = dss.Loads.Name()
        if load in all_residential_loads:
            residential_loads_kw.append(dss.Loads.kW())
            daily_shapes.append(dss.Loads.Daily())

        if not dss.Loads.Next() > 0:
            break

    eusd = []

    for kw in residential_loads_kw:
        eusd_component = 0
        with open('dados2.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                eusd_component = eusd_component + (float(row[0]) * kw) / 60

        eusd.append(eusd_component * 30 * 0.275)

    eusd_data_list = [[value] for value in eusd]
    with open('eusd_loads.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for row in eusd_data_list:
            writer.writerow(row)


