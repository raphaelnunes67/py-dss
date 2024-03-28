import os.path
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


class Plotter:
    def __init__(self):
        self.target_file_path_folder = None
        self.target_file_path = None
        self.plt = plt
        self.title = ''
        self.target_file = None
        self.axis_name_x = ''
        self.axis_name_y = ''
        self.x_values = None
        self.y_values = []
        self.data = None
        self.labels = dict()

    def set_file(self, file: str):
        self.target_file_path = Path(file)
        self.target_file_path_folder = str(Path(str(self.target_file_path) + '/../'))
        self.target_file = pd.read_csv(Path(file))

    def handle_csv_time(self):
        pd.options.mode.chained_assignment = None
        self.target_file['hour'][1:] = self.target_file['hour'][1:] + self.target_file['t(sec)'][1:] / 3600
        self.target_file.to_csv(self.target_file_path, index=False)

    def set_axis(self, **kwargs):
        self.x_values = self.target_file[kwargs.get('x')]
        for value in list(kwargs.values())[1:]:
            self.y_values.append(self.target_file[value])

    def set_labels(self, **kwargs):
        self.labels = kwargs

    def set_title(self, title: str = 'title'):
        self.title = title

    def set_axis_name(self, y_name: str = 'y', x_name: str = 'x'):
        self.axis_name_x = x_name
        self.axis_name_y = y_name

    def perform_plot(self, bases: float = 1.00):
        for value, label in zip(self.y_values, list(self.labels.values())):
            self.plt.plot(self.x_values, value / bases, label=label)

    def show_plot(self, show_legend=True):
        self.plt.title(self.title)
        self.plt.xlabel(self.axis_name_x)
        self.plt.ylabel(self.axis_name_y)
        if show_legend:
            self.plt.legend(loc="upper left")
        self.plt.show()
        self.plt.close()

    def get_min_value(self, column_name: str) -> int:
        df = pd.read_csv(str(self.target_file_path))
        min_value = df[column_name].min()

        return min_value

    def get_max_value(self, column_name: str) -> int:
        df = pd.read_csv(str(self.target_file_path))
        max_value = df[column_name].max()

        return max_value

    def save_figure(self, figure_name, dpi=300, show_legend=True):
        self.plt.title(self.title)
        self.plt.xlabel(self.axis_name_x)
        self.plt.ylabel(self.axis_name_y)
        if show_legend:
            self.plt.legend(loc="upper left")
        self.plt.savefig(Path(self.target_file_path_folder + figure_name), dpi=dpi)
        self.plt.close()

    def __del__(self):
        pass

    @staticmethod
    def write_list_in_csv(file_name, index, values_list):
        if os.path.exists(Path(file_name)):
            df = pd.read_csv(Path(file_name))
            df[index] = values_list
        else:
            df = pd.DataFrame({index: values_list})

        df.to_csv(Path(file_name), index=False)


if __name__ == '__main__':
    plotter = Plotter()

    plotter.set_file('../dss/13Bus_tests/IEEE13BARRAS_Mon_subestacaop_1.csv')

    plotter.set_axis(x='hour', y1=' P1 (kW)', y2=' P2 (kW)', y3=' P3 (kW)')
    plotter.set_labels(l1='1', l2='2', l3='3')
    plotter.set_axis_name(x_name='Time (h)', y_name='Power (kW)')
    plotter.set_title('Example')
    plotter.perform_plot()
    plotter.show_plot(show_legend=True)
