import opendssdirect as dss
from tools import *


if __name__ == '__main__':
    log = Log()

    logger = log.set_logger_stdout('template_debug')

    logger.debug('OpenDSSDirect.py version: {}'.format(dss.__version__))

    logger.debug('Engine information: {}'.format(dss.Basic.Version()))

    files = HandleFiles()

    target_file = files.get_target_file_path('13Bus', 'IEEE13Nodeckt.dss')

    dss.Text.Command('Redirect {}'.format(target_file))

    print(dss.Circuit.AllBusNames())

    dss.Solution.Solve()