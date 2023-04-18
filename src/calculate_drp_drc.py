import pandas as pd
from tools import HandleFiles
from pathlib import Path

if __name__ == '__main__':
    files = HandleFiles()
    target_file = files.get_target_file_path(folder='networks_article', file='REDE1_Mon_carga1_1.csv')
    tr = 127
    # 0,91 V ≤ Vm ≤ 1,04 V - adequada
    #0,86V ≤ Vm < 0,91V ou 1,04V≤ Vm≤ 1,06V - precária
    # Vm < 0,86 V or Vm > 1,05V - crítica
    data = pd.read_csv(Path(target_file))

    voltages = data['V1']
    print(voltages)

    j = 0
    for i in range(1008):
        target_voltage = voltages[j]

        if (0.91*tr) <= target_voltage <= (1.04*tr):
            pass

        # if


