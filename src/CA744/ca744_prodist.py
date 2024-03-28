import os
import pandas as pd
from pathlib import Path
from prodist.drpdrc import DrpDrc


class CA744Prodist:
    @staticmethod
    def calculate_drp_drc_for_each_load(voltvar_folder_path):
        df = pd.read_csv(Path(voltvar_folder_path + '/../eusd_loads.csv'), header=None)

        eusd_data_list = df.iloc[:, 0].tolist()

        phases = ['V1', 'V2', 'V3']

        voltvar_folder = voltvar_folder_path

        folders = os.listdir(Path(voltvar_folder).resolve())

        sheet_content_default = {
            'DRP(%)': [],
            'DRC(%)': [],
            'COMP(R$)': [],
        }

        for folder in folders:
            folder_path = voltvar_folder + '/' + str(folder)
            files = os.listdir(Path(folder_path).resolve())
            i = 0
            for file in files:
                if file.find('drp_drc') == -1 and file.find('_voltage_') != -1:
                    sheet_content = sheet_content_default.copy()
                    eusd = eusd_data_list[i]
                    ckt_drp_drc = DrpDrc(eusd=eusd)
                    drp, drc, comp = ckt_drp_drc.calculate_from_csv(folder_path + '/' + str(file), phases)
                    sheet_content[f'DRP(%)'] = [drp]
                    sheet_content[f'DRC(%)'] = [drc]
                    sheet_content[f'COMP(R$)'] = [comp]
                    df = pd.DataFrame(sheet_content)
                    df.to_excel(Path(folder_path + f'/drp_drc_{str(file)}.xlsx').resolve(), index=False)
                    sheet_content.clear()
                    i = i + 1

    @staticmethod
    def calculate_comp_total(ckt_results_folder):
        for voltvar_mode_folder in ('voltvar_off', 'voltvar_on'):
            sheet_content_default = {
                '0%': [],
                '20%': [],
                '40%': [],
                '60%': [],
                '80%': [],
                '100%': []
            }

            folders = os.listdir(Path(ckt_results_folder + voltvar_mode_folder).resolve())
            sheet_content = sheet_content_default.copy()

            if voltvar_mode_folder == 'voltvar_on':
                sheet_content['0%'] = ['-']

            for folder in folders:
                comp_total = 0
                files = os.listdir(Path(ckt_results_folder + voltvar_mode_folder + '/' + str(folder)).resolve())
                for file in files:
                    if str(file).find('drp_drc') != -1:
                        df = pd.read_excel(
                            Path(ckt_results_folder + voltvar_mode_folder + '/' + str(folder) + '/' + str(
                                file)).resolve())
                        comp_total = comp_total + df['COMP(R$)'][0]

                if str(folder).find('_0') != -1:
                    sheet_content['0%'] = [comp_total]

                elif str(folder).find('20') != -1:
                    sheet_content['20%'] = [comp_total]

                elif str(folder).find('40') != -1:
                    sheet_content['40%'] = [comp_total]

                elif str(folder).find('60') != -1:
                    sheet_content['60%'] = [comp_total]

                elif str(folder).find('80') != -1:
                    sheet_content['80%'] = [comp_total]

                elif str(folder).find('100') != -1:
                    sheet_content['100%'] = [comp_total]

            df = pd.DataFrame(sheet_content)

            if not os.path.exists(ckt_results_folder + '/comp_total.xlsx'):
                with pd.ExcelWriter(Path(ckt_results_folder + '/comp_total.xlsx').resolve(), mode='w') as writer:
                    df.to_excel(writer, sheet_name=voltvar_mode_folder, index=False)
            else:
                with pd.ExcelWriter(Path(ckt_results_folder + '/comp_total.xlsx').resolve(), mode='a',
                                    if_sheet_exists='replace') as writer:
                    df.to_excel(writer, sheet_name=voltvar_mode_folder, index=False)

            sheet_content.clear()


if __name__ == '__main__':
    CA744Prodist().calculate_drp_drc_for_each_load('./results/voltvar_off')
    CA744Prodist().calculate_drp_drc_for_each_load('./results/voltvar_on')
    CA744Prodist().calculate_comp_total('./results/')
