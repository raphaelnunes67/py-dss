import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


class Plotter:
    def __init__(self):
        self.x = None
        self.y = None
        self.title = None
        self.target_file = None
        self.axis_name_x = None
        self.axis_name_y = None
        self.x_values = None
        self.y_values = None
        self.data = None

    def set_file(self, file: str):
        self.target_file = pd.read_csv(Path(file))

    def set_axis(self, y, x):
        self.x = x
        self.y = y
        self.x_values = self.target_file[x]
        self.y_values = self.target_file[y]

    def set_title(self, title: str = 'title'):
        self.title = title

    def set_axis_name(self, y_name: str = 'y', x_name: str = 'x'):
        self.axis_name_x = x_name
        self.axis_name_y = y_name

    def perform_plot(self):
        plt.plot(self.target_file[self.x], self.target_file[self.y])
        plt.title(self.title)
        plt.xlabel(self.x)
        plt.ylabel(self.y)
        plt.show()


if __name__ == '__main__':
    plotter = Plotter()

    plotter.set_file(file=str(Path('../results/LM_1.15_PEN_0.0_Mon_medidor_trafo_conexao_potencia_1.csv')))
    plotter.set_axis(x='t(sec)', y='P1 (kW)')
    plotter.set_axis_name(x_name='Time', y_name='V1')
    plotter.set_title('Exemplo')
    plotter.perform_plot()
