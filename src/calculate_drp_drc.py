import pandas as pd
from tools import HandleFiles
from pathlib import Path

if __name__ == '__main__':
    files = HandleFiles()
    target_file = files.get_target_file_path(folder='networks_article', file='REDE1_Mon_carga26_1.csv')
    tr = 127.0
    # 0,92 V ≤ Vm ≤ 1,047 V - adequada
    #0,86V ≤ Vm < 0,91V ou 1,04V≤ Vm≤ 1,06V - precária
    # Vm < 0,86 V or Vm > 1,05V - crítica
    data = pd.read_csv(Path(target_file))

    voltages = data['V2']
    print(voltages)
    nlp = 0
    nlc = 0

    j = 0
    for i in range(1008):
        if j == 23:
            j = 0
        target_voltage = voltages[j]
        print(target_voltage)

        # if (0.91*tr) <= target_voltage <= (1.04*tr):
        #     pass

        if ((0.86*tr) <= target_voltage < (0.92*tr)) or ((1.047*tr) <= target_voltage <= (1.06*tr)):
            nlp = nlp + 1
        if (target_voltage < 0.86*tr) or (target_voltage > 1.06*tr):
            nlc = nlc + 1

        j = j + 1

    DRP = round((nlp / 1008) * 100, 2)
    DRC = round((nlc / 1008) * 100, 2)
    print(f'DRP: {DRP}%')
    print(f'DRC: {DRC}%')


