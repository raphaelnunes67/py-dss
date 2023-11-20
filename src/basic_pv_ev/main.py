from pathlib import Path
import opendssdirect as dss


if __name__ == '__main__':
    target_file = Path('./basic_pv_ve.dss').resolve()
    dss.Text.Command('Redirect {}'.format(target_file))
    dss.Text.Command(f'new monitor.res{1} element=load.LoadRes terminal=1 mode=0')
    dss.Text.Command('solve')
    dss.Text.Command(f'export monitors res{1}')
    dss.Text.Command('plot monitor object=res channels=(1 3 5)')